import cv2

import urllib2
import numpy as np
import yaml
import time 
with open("config.yaml", "r") as f:
    config = yaml.load(f)

#from base_camera import BaseCamera

'''

#if len(sys.argv)>1:
 #   host = sys.argv[1]


print 'Streaming ' + hoststr

stream = urllib2.urlopen(hoststr)
'''

cam = cv2.VideoCapture('http://' + config["IPcam"]["hostIP"] + '/videofeed')
#time.sleep(2)



def getFrame():
    #print "hi"
    '''
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
        cv2.imshow(hoststr,i)
        print type(i)
        return i
    '''

    img = cam.read()[1]
    img = cv2.flip(img, 1) 
    cv2.imshow("Window",img)
    cv2.waitKey(50)
    return img



    
        




   

