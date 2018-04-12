import cv2
import yaml


with open("config.yaml", "r") as f:
    config = yaml.load(f)

# time.sleep(2)


def get_frame(cam):
    # print "hi"
    
    img = cam.read()[1]
    img = cv2.flip(img, 1)
    cv2.imshow("Cam Frames", img)
    cv2.waitKey(50)
    return img
