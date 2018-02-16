import cv2

import urllib2
import numpy as np



host = "192.168.31.116:8080"
#if len(sys.argv)>1:
 #   host = sys.argv[1]

hoststr = 'http://' + host + '/videofeed'
print 'Streaming ' + hoststr

stream = urllib2.urlopen(hoststr)

cam = cv2.VideoCapture(0)

def getFrame():
    #print "hi"
    
    img = cam.read()[1]
    img = cv2.flip(img, 1)
    cv2.imshow("Window",img)
    cv2.waitKey(50)
    return img
    


    
        




   

