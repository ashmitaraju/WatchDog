from multiprocessing import Process, Queue
from faceVerify import face_verify, get_face
from datetime import datetime
import os
import cv2
from azure.storage.blob import BlockBlobService
import MySQLdb
import yaml
import re
import sys
from motionDetector import motion_detector
from face_detector import face_detector

with open("config.yaml", "r") as f:
    config = yaml.load(f)

userName = sys.argv[1]
block_blob_service = BlockBlobService(account_name=config['azure-blob']['account_name'],
                                      account_key=config['azure-blob']['account_key'],
                                      )

sql = config['mysql']
db = MySQLdb.connect(sql['server'], sql['username'], sql['password'], sql['database'])
cursor = db.cursor()

query = """select azure_id, person_name from Persons, AuthImageGallery
         where Persons.person_id=AuthImageGallery.person_id 
         and Persons.username= '%s'""" % userName

cursor.execute(query)

results = cursor.fetchall()

database = {}
for result in results:
    database[result[0]] = result[1]

camID = ""


# database = { '1d826b9b-747c-40b5-90fc-cb3087b03554' : 'kondu' , '0fe14084-9aea-4724-86c4-366d093b2980': 'ashmita'}
def send_frames(send_queue, response_queue):
    while True:
        while send_queue.empty():
            pass
        img = send_queue.get()

        cv2.imshow("Sent Frame", img)
        print "sent frame"
        cv2.waitKey(5)
        frame_bytes = cv2.imencode('.jpg', img)[1].tostring()
        response = get_person(frame_bytes)
        response_queue.put([response, img])


def send_faces(send_face_queue, response_face_queue):
    while True:
        while send_face_queue.empty():
            pass
        img = send_face_queue.get()
        # window_sent_face = cv2.namedWindow("Sent Face", cv2.WINDOW_NORMAL)
        cv2.imshow("Sent Face", img)
        cv2.waitKey(5)
        frame_bytes = cv2.imencode('.jpg', img)[1].tostring()
        response = get_face(frame_bytes)
        response_face_queue.put([response, frame_bytes])


def analyse_faces(response_face_queue):
    while True:
        while response_face_queue.empty():
            pass
        response = response_face_queue.get()
        face_ids = []
        if response[0]:
            for face in response[0]:
                print face
                fid = str(face["faceId"])
                # print fid
                face_ids.append(fid)
                verified = face_verify(face_ids, userName)
                # print type ( verified )
                found = None
                if verified:
                    for verifiedFace in verified:
                        # print type (verifiedFace)
                        if verifiedFace["candidates"]:
                            for candidate in verifiedFace["candidates"]:
                                found = candidate["personId"]
                            if found in database:
                                print database[found]

                        else:
                            timestamp = str(datetime.now())
                            filename = re.sub(r' ', '_', timestamp)
                            # print filename

                            block_blob_service.create_blob_from_bytes('unauthorized', filename, response[1])
                            url = "https://watchdogsok.blob.core.windows.net/unauthorized/%s" % filename
                            query_send_unauth = """
insert into UnauthImageGallery(username, image_filename, image_path, timestamp, cameraID, cameraLocation) 
values('%s', '%s', '%s' , '%s', '%s', '%s')""" % (userName, filename, url, timestamp, camID, cameraLocation)
                            # query = """select * from Persons"""
                            # print query
                            cursor.execute(query_send_unauth)
                            db.commit()
                            # print cursor.fetchall()
                            print "Face not authorized"
        else:
            pass
            # print "No faces in frame"


if __name__ == '__main__':
    query = """select * from camera where username = "%s" """ % userName
    cursor.execute(query)
    cameras = cursor.fetchall()

    print "ID\tCamera Location"

    camDict = {}
    for camera in cameras:
        print "%s\t%s" % (camera[0], camera[2])
        camDict[camera[0]] = camera[2]

    print camDict
    camID = raw_input("Enter ID : ")

    cameraLocation = camDict[camID]

    cam_host = 0
    # cam_host = 'http://' + config["IPcam"]["hostIP"] + '/videofeed'

    sendQueue = Queue()
    responseQueue = Queue()
    responseFaceQueue = Queue()
    processList = []
    try:
        motionDetect = Process(target=motion_detector, args=(sendQueue, cam_host))
        sendProcess = Process(target=face_detector, args=(sendQueue, responseQueue, True, '../images/detect_images/'))
        sendFacesProcess = Process(target=send_faces, args=(responseQueue, responseFaceQueue,))
        analyseFacesProcess = Process(target=analyse_faces, args=(responseFaceQueue,))

        processList.extend([motionDetect, sendProcess, sendFacesProcess, analyseFacesProcess])

        for proc in processList:
            proc.daemon = True

        parent = os.getpid()

        for proc in processList:
            proc.start()

        host = config["IPcam"]["hostIP"]
        host_str = 'http://' + host + '/videofeed'
        while True:
            pass

    except KeyboardInterrupt as e:
        print "\n\n" + str(e) + "\n\n"
        for proc in processList:
            proc.terminate()
        cv2.destroyAllWindows()
        exit(0)

