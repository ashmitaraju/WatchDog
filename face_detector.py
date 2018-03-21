<<<<<<< HEAD
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
=======
import cv2
from datetime import datetime
import dlib
from multiprocessing import Process, Queue
import signal

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
    detector = dlib.get_frontal_face_detector()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Run detector and get bounding boxes of the faces on image.
    start_time = datetime.now()
    detected_faces = detector(image, 1)
    end_time = datetime.now()
    micro_sec = (end_time - start_time).total_seconds()
    print "dlib time/frame: " + str(micro_sec) + " | fps: " + str(1/micro_sec)

    face_frames = [(x.left(), x.top(),
                    x.right(), x.bottom()) for x in detected_faces]
    return face_frames


def face_detector(frame_queue, face_queue, display=False, save=False):
    while True:
        if frame_queue.empty():
            continue
        frame = frame_queue.get()
        datetime.now
        face_coordinates = detect_faces(frame)
        print face_coordinates
        for n, face_coordinates in enumerate(face_coordinates):
            (x, y, w, h) = rect_to_bb(face_coordinates)
            face = frame[y:h, x:w]
            if True:
                frame_scanned = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.imshow("Face Detector", frame_scanned)
                cv2.waitKey(5)
            if save:
                img_path = save + str(datetime.now()) + "-" + str(n) + ".jpg"
                cv2.imwrite(img_path, face)
            face_queue.put(face)


def read_cam(frames):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print "Getting cam failed"
        exit(0)
    while True:
        if frames.full():
            continue
        ret, frame = cam.read()
        print frame.shape
        frames.put(frame)


if __name__ == '__main__':
    print "main"
    frames = Queue(10)
    faces = Queue()
    frame_getter_process = Process(target=face_detector, args=(frames, faces))
    face_detector_process = Process(target=read_cam, args=(frames,))

    frame_getter_process.daemon = True
    face_detector_process.daemon = True
    original_signal_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    frame_getter_process.start()
    face_detector_process.start()
    signal.signal(signal.SIGINT, original_signal_handler)
    try:
        frame_getter_process.join()
        face_detector_process.join()
        cv2.destroyAllWindows()
        exit(1)
    except Exception, e:
        print e
        frame_getter_process.terminate()
        face_detector_process.terminate()
        frame_getter_process.join()
        face_detector_process.join()
        if e is KeyboardInterrupt:
            cv2.destroyAllWindows()
            exit(1)
        else:
            raise e
            exit(2)

>>>>>>> 826c804010a63a44cd8a4eb2ae65ce066ea2c20f
