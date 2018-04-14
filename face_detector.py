import cv2
from datetime import datetime
import dlib
import time
from WindowManager import WindowManager


def rect_to_bb(rect):
    # take a bounding predicted by dlib and convert it
    # to the format (x, y, w, h) as we would normally do
    # with OpenCV
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y

    # return a tuple of (x, y, w, h)
    return x, y, w, h


detector = dlib.get_frontal_face_detector()


def detect_faces(image):
    # Create a face detector

    start_time = datetime.now()

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # make low res image for detection
    frame_width, frame_height = image.shape[:2]
    ratio = frame_height/480.0
    lowres_image = cv2.resize(image, (0, 0), fx=1.0/ratio, fy=1.0/ratio)
    # Run detector and get bounding boxes of the faces on image.
    detected_faces = detector(lowres_image, 1)

    face_frames = [(int(x.left()*ratio), int(x.top()*ratio),
                    int(x.right()*ratio), int(x.bottom()*ratio)) for x in detected_faces]

    end_time = datetime.now()
    micro_sec = (end_time - start_time).total_seconds()
    # print "dlib time/frame: " + str(micro_sec) + " | fps: " + str(1 / micro_sec)
    print "found2"
    return face_frames


def face_detector(frame_queue, face_queue, display=False, save=False):
    windowManager = WindowManager("Detected Face")
    while True:
        if frame_queue.empty():
            continue
        if face_queue.full():
            continue
        frame = frame_queue.get()
        print "found"
        face_coordinates = detect_faces(frame)
        print face_coordinates
       

        try:
            for n, coordinates in enumerate(face_coordinates):
                print "found3"
                (x, y, w, h) = rect_to_bb(coordinates)
                face = frame[y - 10 :y+h +10, x -10:x+w+10 ]
                if display:
                    frame_scanned = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    #cv2.imshow(window, frame_scanned)
                    #cv2.imshow("faces", face)
                    windowManager.put(face)
                    cv2.waitKey(5)
                if save:
                    img_path = str(save) + str(datetime.now()) + "-" + str(n) + ".jpg"
                    cv2.imwrite(img_path, face)
                face_queue.put(face)
        except Exception, e:
            print e
            continue


def read_cam(frames):
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
    print (
            "Updated Resolution Settings to: " +
            str(cam.get(cv2.CAP_PROP_FRAME_WIDTH)) +
            "x" +
            str(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )
    if not cam.isOpened():
        print "Getting cam failed"
        exit(0)

    delay = 0.001
    while True:
        # print "delay: "+str(delay)
        if frames.full():
            delay = delay*2
            time.sleep(delay)
            continue
        delay = delay/2
        ret, frame = cam.read()
        frames.put(frame)
