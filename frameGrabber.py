import cv2



cam = cv2.VideoCapture(0)

def getFrame():
    #print "hi"
    img = cam.read()[1]
    img = cv2.flip(img, 1)
    cv2.imshow("Window",img)
    cv2.waitKey(50)
    return img
        




   

