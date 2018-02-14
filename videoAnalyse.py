from multiprocessing import Process, Queue
from frameGrabber import getFrame
from faceDetectAzure import getFace
from faceVerify import verifyFace
import os
import signal
import json
import cv2


database = { '1d826b9b-747c-40b5-90fc-cb3087b03554' : 'kondu' , '0fe14084-9aea-4724-86c4-366d093b2980': 'ashmita'} 
def sendFrames(sendQueue, responseQueue):

    while True:
        while sendQueue.empty():
            pass  
        img = sendQueue.get()    
       # print type (img)
        cv2.imshow("Sent Frame",img)
        cv2.waitKey(5)
        frameBytes = cv2.imencode('.jpg', img )[1].tostring()    
        response = getFace (frameBytes)
       # print response
        responseQueue.put(response)
    


def analyseResponses(sendQueue, responseQueue): 
    while True:
        while responseQueue.empty():
            pass  
        response = responseQueue.get()

        faceIds =[]
       # print response
        if response:
            for face in response:
                fid = str (face["faceId"])
                faceIds.append(fid)
                verified = json.loads (verifyFace(faceIds))
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
    try:
        sendProcess = Process( target = sendFrames, args =(sendQueue, responseQueue,))
        analyseProcess = Process ( target = analyseResponses, args = (sendQueue, responseQueue,))
        parent = os.getpid()
        sendProcess.start()
        analyseProcess.start()
        count = 0
        while True:
           # print count
            img = getFrame()
            if  count % 60 == 0 :
                sendQueue.put(img)  
            count += 1
        sendProcess.join()

    except KeyboardInterrupt:
        sendProcess.join()
        analyseProcess.join()
        os.kill(parent, signal.SIGTERM)


        

    

    

        

    
    
