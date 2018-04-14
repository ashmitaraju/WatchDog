from cvapi import get_objects
import cv2
from WindowManager import WindowManager


def object_detector(frame_queue, watchlist):
    windowManager = WindowManager("Sent Frame")
    while True:
        if frame_queue.empty():
            continue
        img = frame_queue.get()
        frame_bytes = cv2.imencode('.jpg', img)[1].tostring()
        response = get_objects(frame_bytes)
        detected_objects = []
        windowManager.put(img)
        for category in response['categories'] :
            detected_objects.append(category['name'])
        
        for obj in watchlist:
            if obj in detected_objects:
              print '{} was detected!'.format(obj)
        tags = ''
        for tag in response['tags']:
            tags = tags + tag['name'] +  ', '

        print tags
            


        
