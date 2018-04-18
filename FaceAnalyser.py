from faceVerify import face_verify
import re
from datetime import datetime
from azure.storage.blob import BlockBlobService
import MySQLdb
import yaml
from multiprocessing import Process
import csv
import EmailSender

with open("config.yaml", "r") as f:
    config = yaml.load(f)


class FaceAnalyser(object):
    def __init__(self, user_name, cam_ID, cam_location, email):

        self.user_name = user_name
        self.cam_ID = cam_ID
        self.cam_location = cam_location
        self.email = email
        self.block_blob_service = BlockBlobService(account_name=config['azure-blob']['account_name'],
                                                   account_key=config['azure-blob']['account_key'],
                                                   )
        sql = config['mysql']
        self.db = MySQLdb.connect(sql['server'], sql['username'], sql['password'], sql['database'])
        self.cursor = self.db.cursor()

        query = """select azure_id, person_name from Persons, AuthImageGallery
                 where Persons.person_id=AuthImageGallery.person_id
                 and Persons.username= '%s'""" % user_name

        self.cursor.execute(query)

        results = self.cursor.fetchall()

        self.database = {}
        for result in results:
            self.database[result[0]] = result[1]


def analyser(response_face_queue,user_name, cam_ID, cam_location, email):

    face_analyser = FaceAnalyser(user_name, cam_ID, cam_location, email)

    while True:
        while response_face_queue.empty():
            pass
        response = response_face_queue.get()
        face_ids = []
        if response[0]:
            for face in response[0]:
                fid = str(face["faceId"])

                face_ids.append(fid)
                verified = face_verify(face_ids, face_analyser.user_name)
                # print type ( verified )
                found = None
                if verified:
                    for verifiedFace in verified:
                        # print type (verifiedFace)
                        if verifiedFace["candidates"]:
                            for candidate in verifiedFace["candidates"]:
                                found = candidate["personId"]
                            if found in face_analyser.database:
                                print face_analyser.database[found]

                        else:
                            print "Face not authorized"
                            timestamp = str(datetime.now())
                            filename = re.sub(r' ', '_', timestamp)
                            fieldnames = ['faceId', 'timestamp']
                            # print filename
                            image_file = open('unAuthFaces/{}.jpg'.format(filename) , 'wb')
                            csv_file = open('unAuthFaces/data.csv', 'w')
                            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerow({'faceId': face['faceId'], 'timestamp': filename})

                            csv_file.close()
                            image_file.write(response[1])

                            image_file.close()

                            #saves unauthimage in local directory
                            face_analyser.block_blob_service.create_blob_from_bytes('unauthorized', filename, response[1])
                            url = "https://watchdogsok.blob.core.windows.net/unauthorized/%s" % filename
                            query_send_unauth = """
insert into UnauthImageGallery(username, image_filename, image_path, timestamp, cameraID, cameraLocation)
values('%s', '%s', '%s' , '%s', '%s', '%s')""" % (face_analyser.user_name, filename, url, timestamp, face_analyser.cam_ID, face_analyser.cam_location)
                            # query = """select * from Persons"""
                            # print query
                            EmailSender.send(face_analyser.email, url)
                            face_analyser.cursor.execute(query_send_unauth)
                            face_analyser.db.commit()
                            # print cursor.fetchall()

        else:
            pass
            # print "No faces in frame"
