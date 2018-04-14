from multiprocessing import Process, Queue
import os
import cv2
import MySQLdb
import yaml
import sys
from motionDetector import motion_detector
from face_detector import face_detector
from send_faces import send_faces
from FaceAnalyser import FaceAnalyser, analyser
from object_detector import object_detector

with open("config.yaml", "r") as f:
    config = yaml.load(f)

userName = sys.argv[1]

# database = { '1d826b9b-747c-40b5-90fc-cb3087b03554' : 'kondu' , '0fe14084-9aea-4724-86c4-366d093b2980': 'ashmita'}

if __name__ == '__main__':
    query = """select * from camera where username = "%s" """ % userName
    sql = config['mysql']
    db = MySQLdb.connect(sql['server'], sql['username'], sql['password'], sql['database'])
    cursor = db.cursor()
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

    if sys.argv[2] == '-i':
        cam_host = 'http://' + config["IPcam"]["hostIP"] + '/videofeed'
    elif sys.argv[2] == '-w':
        cam_host = 0
    

    sendQueue = Queue()
    responseQueue = Queue()
    responseFaceQueue = Queue()
    objectQueue = Queue()
    processList = []
    watchlist = ['people_', 'text_']
    host = config["IPcam"]["hostIP"]
    host_str = 'http://' + host + '/videofeed'
    host_str = 0
    try:
        motionDetect = Process(target=motion_detector, args=(sendQueue, objectQueue, cam_host))
        sendProcess = Process(target=face_detector, args=(sendQueue, responseQueue, True, '../images/detect_images/'))
        sendFacesProcess = Process(target=send_faces, args=(responseQueue, responseFaceQueue,))
        analyserProcess = Process(target=analyser, args=(responseFaceQueue, userName, camID, cameraLocation))
        objectDetectProcess = Process(target=object_detector, args=(objectQueue, watchlist))

        processList.extend([motionDetect, sendProcess, sendFacesProcess, analyserProcess, objectDetectProcess])

        for proc in processList:
            proc.daemon = True

        parent = os.getpid()

        for proc in processList:
            proc.start()
        # faceAnalyser.start()
        while True:
            pass

    except KeyboardInterrupt as e:
        print "\n\n" + str(e) + "\n\n"
        for proc in processList:
            proc.terminate()
        cv2.destroyAllWindows()
        exit(0)

