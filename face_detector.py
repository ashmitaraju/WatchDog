import cv2
from datetime import datetime
import dlib
from multiprocessing import Queue

def rect_to_bb(rect):
    # take a bounding predicted by dlib and convert it
    # to the format (x, y, w, h) as we would normally do
    # with OpenCV
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y

    # return a tuple of (x, y, w, h)
    return (x, y, w, h)


def detect_faces(image):
    # Create a face detector
   # print "hey1"
    detector = dlib.get_frontal_face_detector()
    # Run detector and get bounding boxes of the faces on image.
    detected_faces = detector(image, 1)
    face_frames = [(x.left(), x.top(),
                    x.right(), x.bottom()) for x in detected_faces]
    return face_frames




def face_detector(frame_queue, face_queue, display=False, save=False):
    while True:
        print frame_queue
        frame = frame_queue.get(block=True)
        face_coordinates = detect_faces(frame)
        print face_coordinates
        # print "78u"
        for n, face_coordinates in enumerate(face_coordinates):
           # print "hi"
            (x, y, w, h) = rect_to_bb(face_coordinates)
            face = frame[y:h, x:w]
            if display:
                frame_scanned = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.imshow("Face Detector", frame_scanned)
                cv2.waitKey(5)
            if save:
                img_path = save + str(datetime.now()) + "-" + str(n) + ".jpg"
                cv2.imwrite(img_path, face)
            face_queue.put(face)
