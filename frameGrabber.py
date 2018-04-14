import cv2
import yaml
from WindowManager import WindowManager

with open("config.yaml", "r") as f:
    config = yaml.load(f)

# time.sleep(2)

def get_frame(cam, windowManager):
    # print "hi"
    img = cam.read()[1]
    img = cv2.flip(img, 1)
    windowManager.put(img)
    cv2.waitKey(50)
    return img
