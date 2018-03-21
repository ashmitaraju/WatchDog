from multiprocessing import Process, Queue
from frameGrabber import getFrame
#from faceDetectAzure import getFace
from faceVerify import verifyFace, getFace, getPerson
#from personDetect import getPerson
from datetime import datetime
import os
import signal
import json
import cv2
import urllib2
import numpy as np
from azure.storage.blob import BlockBlobService , ContentSettings
import MySQLdb
import yaml
import re
import sys
import imutils
from face_detector import face_detector

with open("config.yaml", "r") as f:
    config = yaml.load(f)


userName = sys.argv[1]
block_blob_service = BlockBlobService(account_name= config['azure-blob']['account_name'] , account_key= config['azure-blob']['account_key'])

sql = config['mysql']
db = MySQLdb.connect( sql['server'] ,sql['username'] , sql['password'] ,sql['database'] )
cursor = db.cursor()



query = """select azure_id, person_name from Persons, AuthImageGallery
         where Persons.person_id=AuthImageGallery.person_id 
         and Persons.username= '%s'""" %userName

cursor.execute( query )

results = cursor.fetchall()

database = {}
for result in results:
    database[result[0]] = result[1]


camID = ""
    
#database = { '1d826b9b-747c-40b5-90fc-cb3087b03554' : 'kondu' , '0fe14084-9aea-4724-86c4-366d093b2980': 'ashmita'} 
def sendFrames(sendQueue, responseQueue):

    while True:
        while sendQueue.empty():
            pass  
        img = sendQueue.get()    
        cv2.imshow("Sent Frame",img)
        print "sent frame"
        cv2.waitKey(5)
        frameBytes = cv2.imencode('.jpg', img )[1].tostring()    
        response = getPerson (frameBytes)
        responseQueue.put([response , img])
    


def analyseResponses(sendQueue, responseQueue): 
    while True:
        while responseQueue.empty():
            pass  
        response = responseQueue.get()

        if response[0]:
            for face in response[0]["faces"]:
                timeStamp = str(datetime.now())
                faceRectangle = face["faceRectangle"]
                
                y = faceRectangle["top"]
                x = faceRectangle["left"]
                h = faceRectangle["height"]
                w = faceRectangle["width"]
                crop_img = response[1][y:y+h, x:x+w]
                sendFaceQueue.put( crop_img )
                cv2.imwrite( "images/%s.jpg" %timeStamp, crop_img )
        else :
            print "No faces in frame"

def sendFaces (sendFaceQueue, responseFaceQueue):
    while True:
        while sendFaceQueue.empty():
            pass  
        img = sendFaceQueue.get()    
        cv2.imshow("Sent Face",img)
        cv2.waitKey(5)
        frameBytes = cv2.imencode('.jpg', img )[1].tostring()    
        response = getFace(frameBytes)
        responseFaceQueue.put([response , frameBytes])


def analyseFaces (sendFaceQueue, responseFaceQueue):
    while True:
        while responseFaceQueue.empty():
            pass  
        response = responseFaceQueue.get()
        faceIds = []
        if response[0]:
            for face in response[0]:
                #print face
                fid = str (face["faceId"])
                #print fid
                faceIds.append(fid)
                verified = verifyFace(faceIds , userName)
                #print type ( verified )
                
                if verified:
                    for verifiedFace in verified:
                        #print type (verifiedFace)
                        if verifiedFace["candidates"]:
                            for candidate in verifiedFace["candidates"]:
                                found = candidate["personId"]
                            if found in database:
                                print database[found]

                        else :
                            timestamp = str(datetime.now())
                            filename = re.sub(r' ', '_', timestamp)
                            #print filename

                            block_blob_service.create_blob_from_bytes('unauthorized', filename, response[1])
                            url = "https://watchdogsok.blob.core.windows.net/unauthorized/%s" % filename
                            query = """insert into UnauthImageGallery(username, image_filename, image_path,timestamp,cameraID, cameraLocation ) values('%s', '%s', '%s' , '%s', '%s', '%s')"""%( userName, filename, url, timestamp, camID, cameraLocation)
                            #query = """select * from Persons"""
                           # print query
                            cursor.execute( query )
                            db.commit()
                            #print cursor.fetchall()
                            print "face not authorized"

        else :
            print "No faces in frame"
     
if __name__ == '__main__':

    query = """select * from camera where username = "%s" """ %userName
    cursor.execute(query)
    cameras = cursor.fetchall()

    print "ID\tCamera Location"

    camDict = {}
    for camera in cameras :
        print "%s\t%s" %(camera[0],camera[2])
        camDict[ camera[0]] = camera[2]

    print camDict
    camID = raw_input("Enter ID : ")

    cameraLocation = camDict[camID]

    sendQueue = Queue()
    responseQueue = Queue()
    sendFaceQueue = Queue()
    responseFaceQueue = Queue()
    try:
        sendProcess = Process( target = face_detector, args =(sendQueue, responseQueue, True))
       # analyseProcess = Process ( target = analyseResponses, args = (sendQueue, responseQueue,))
        sendFacesProcess = Process( target = sendFaces, args =(responseQueue, responseFaceQueue,))
        analyseFacesProcess = Process( target = analyseFaces, args =(sendFaceQueue, responseFaceQueue,))
        parent = os.getpid()
        sendProcess.start()
        #face_detector.start()
        sendFacesProcess.start()
        analyseFacesProcess.start()
        
        ''' start ipStream'''
        '''
    
        host = config['IPcam']['hostIP']
        #print host
	
      #  if len(sys.argv)>1:
       #     host = sys.argv[1]

        hoststr = 'http://' + host + '/videofeed'
        print 'Streaming ' + hoststr

        stream = urllib2.urlopen(hoststr)

        bytes=''
        count = 0
        while True:
            bytes+=stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
                cv2.imshow(hoststr,i)
                if  count % 10 == 0 :
                    sendQueue.put(i) 
                    print 'sent'
                
                if cv2.waitKey(5) ==27:
                    exit(0)
                count += 1
                #print count
        '''

        '''end ip stream'''
        """
        count = 0
        while True:
           # print count
            img = getFrame()
            if  count % 60 == 0 :
                sendQueue.put(img)  
            count += 1
        """
        prevFrame = None

        # loop over the frames of the video
        count = 0
        while True:
            # grab the current frame and initialize the occupied/unoccupied
            # text
            frame = getFrame()
            
            #(grabbed, frame) = camera.read()
            #text = "Unoccupied"
            #print "unoccupied"

            # if the frame could not be grabbed, then we have reached the end
            # of the video
            #if not grabbed:
             #   break

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            if prevFrame is None:
                prevFrame = gray
                continue

            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(prevFrame, gray)
            if count%5 == 0:
                prevFrame = gray
                count = 1
            count+=1
            thresh = cv2.threshold(frameDelta, 127, 255, cv2.THRESH_BINARY)[1]
            #thresh = cv2.adaptiveThreshold(frameDelta,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)


            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            if cnts: 
                print "occupied"
                sendQueue.put(frame)  
            
       
        sendProcess.join()
    except KeyboardInterrupt:
        sendProcess.join()
       # analyseProcess.join()
        os.kill(parent, signal.SIGTERM)


















