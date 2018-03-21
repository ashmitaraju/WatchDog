import cv2
from datetime import datetime
import dlib
from multiprocessing import Process, Queue
import signal
import time

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


detector = dlib.get_frontal_face_detector()

def detect_faces(image):
    # Create a face detector

    start_time = datetime.now()

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # make low res image for detection
    frame_width, frame_height = image.shape[:2]
    ratio = frame_height//300
    lowres_image = cv2.resize(image, (0, 0), fx=1.0/ratio, fy=1.0/ratio)
    # Run detector and get bounding boxes of the faces on image.
    detected_faces = detector(lowres_image, 1)

    face_frames = [(x.left()*ratio, x.top()*ratio,
                    x.right()*ratio, x.bottom()*ratio) for x in detected_faces]

    end_time = datetime.now()
    micro_sec = (end_time - start_time).total_seconds()
    print "dlib time/frame: " + str(micro_sec) + " | fps: " + str(1 / micro_sec)

    return face_frames


def face_detector(frame_queue, face_queue, display=False, save=False):
    while True:
        if frame_queue.empty():
            continue

        frame = frame_queue.get()
        face_coordinates = detect_faces(frame)

        for n, face_coordinates in enumerate(face_coordinates):
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
        print "delay: "+str(delay)
        if frames.full():
            delay = delay*2
            time.sleep(delay)
            continue
        delay = delay/2
        ret, frame = cam.read()
        print frame.shape
        frames.put(frame)


if __name__ == '__main__':
    print "main"
    frames = Queue(10)
    faces = Queue()
    frame_getter_process = Process(target=face_detector, args=(frames, faces, True))
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

