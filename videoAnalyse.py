from multiprocessing import Process, Queue
from frameGrabber import getFrame
from faceDetectAzure import getFace
from faceVerify import verifyFace
from personDetect import getPerson
from datetime import datetime
import os
import signal
import json
import cv2
import urllib2
import numpy as np

import MySQLdb

db = MySQLdb.connect("watchdogserver.mysql.database.azure.com","aravindbs@watchdogserver","Watchdog123","watchdog" )
cursor = db.cursor()

query = """select azure_id, person_name from Persons, AuthImageGallery
         where Persons.person_id=AuthImageGallery.person_id 
         and Persons.person_id=current_user.username"""

results = cursor.fetchall()

database = {}
for result in results:
    database[result[0]] = result[1]


    
#database = { '1d826b9b-747c-40b5-90fc-cb3087b03554' : 'kondu' , '0fe14084-9aea-4724-86c4-366d093b2980': 'ashmita'} 
def sendFrames(sendQueue, responseQueue):

    while True:
        while sendQueue.empty():
            pass  
        img = sendQueue.get()    
       # print type (img)
        cv2.imshow("Sent Frame",img)
        cv2.waitKey(5)
        frameBytes = cv2.imencode('.jpg', img )[1].tostring()    
        response = getPerson (frameBytes)
       # print response
        responseQueue.put([response , img])
    


def analyseResponses(sendQueue, responseQueue): 
    while True:
        while responseQueue.empty():
            pass  
        response = responseQueue.get()

        faceList = [] # index 0 is the JSON Response & index 1 is the img in numpy array 
       # print response
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
        #print type (img)
        cv2.imshow("Sent Face",img)
        cv2.waitKey(5)
        frameBytes = cv2.imencode('.jpg', img )[1].tostring()    
        response = getFace(frameBytes)
       # print response
        responseFaceQueue.put(response)


def analyseFaces (sendFaceQueue, responseFaceQueue):
    while True:
        while responseFaceQueue.empty():
            pass  
        response = responseFaceQueue.get()
        faceIds = []
        if response:
            for face in response:
                fid = str (face["faceId"])
                faceIds.append(fid)
                verified = json.loads (verifyFace(faceIds , '02'))
               # print type ( verified )
                
                if verified:
                    for verifiedFace in verified:
                        #print type (verifiedFace)
                        if verifiedFace["candidates"]:
                            for candidate in verifiedFace["candidates"]:
                                found = candidate["personId"]
                            if found in database:
                                print database[found]

                        else :
                            print "face not authorized"

        else :
            print "No faces in frame"



       
        
if __name__ == '__main__':
    sendQueue = Queue()
    responseQueue = Queue()
    sendFaceQueue = Queue()
    responseFaceQueue = Queue()
    try:
        sendProcess = Process( target = sendFrames, args =(sendQueue, responseQueue,))
        analyseProcess = Process ( target = analyseResponses, args = (sendQueue, responseQueue,))
        sendFacesProcess = Process( target = sendFaces, args =(sendFaceQueue, responseFaceQueue,))
        analyseFacesProcess = Process( target = analyseFaces, args =(sendFaceQueue, responseFaceQueue,))
        parent = os.getpid()
        sendProcess.start()
        analyseProcess.start()
        sendFacesProcess.start()
        analyseFacesProcess.start()
        
        ''' start ipStream'''
    
        host = "192.168.31.116:8080"
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
                if  count % 20 == 0 :
                    sendQueue.put(i) 
                    print 'sent'
                
                if cv2.waitKey(5) ==27:
                    exit(0)
                count += 1
                #print count
        

        '''end ip stream'''
        





        '''
        count = 0
        while True:
           # print count
            img = getFrame()
            if  count % 60 == 0 :
                sendQueue.put(img)  
            count += 1
        '''







        sendProcess.join()
    except KeyboardInterrupt:
        sendProcess.join()
        analyseProcess.join()
        os.kill(parent, signal.SIGTERM)


        

    

    

        

    
    
