from cvapi import get_objects
import cv2
from WindowManager import WindowManager
from datetime import datetime
import EmailSender
from multiprocessing import Process
import yaml
from azure.storage.blob import BlockBlobService
import MySQLdb
import re

with open("config.yaml", "r") as f:
    config = yaml.load(f)



def object_detector(frame_queue, watchlist, user):

    block_blob_service = BlockBlobService(account_name=config['azure-blob']['account_name'],
                                                   account_key=config['azure-blob']['account_key'],)

    sql = config['mysql']
    db = MySQLdb.connect(sql['server'], sql['username'], sql['password'], sql['database'])
    cursor = db.cursor()


    windowManager = WindowManager("Sent Frame")
    while True:
        if frame_queue.empty():
            continue
        img = frame_queue.get()
        frame_bytes = cv2.imencode('.jpg', img)[1].tostring()
        response = get_objects(frame_bytes)
        windowManager.put(img)
        tags = []
        for tag in response['tags']:
            tags.append(tag['name'])

        timestamp = str(datetime.now())
        filename = re.sub(r' ', '_', timestamp)
        for tag in tags:
            if tag in watchlist:
                image_file = open ('unAuthObjects/{}.jpg'.format(filename), 'w')
                block_blob_service.create_blob_from_bytes('objects', filename + '.jpg', frame_bytes)
                print tag + ' detected'
                image_file.write (frame_bytes)
                image_file.close()
                url = "https://watchdogsok.blob.core.windows.net/objects/%s.jpg" % filename
                EmailSender.send(user.email, url)
              #  print (user.username, filename, url, tag, timestamp, user.camID, user.camLocation)
                object_cursor = db.cursor()
                query_object = """insert into UnauthObjects(username, image_filename, image_path, object_class, timestamp, cameraID, cameraLocation)
values('%s', '%s', '%s' ,'%s', '%s', '%s', '%s')""" % (user.username, filename, url, tag, timestamp, user.camID, user.camLocation)
                object_cursor.execute(query_object)
                db.commit()
