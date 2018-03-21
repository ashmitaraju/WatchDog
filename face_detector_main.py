from multiprocessing import Queue, Process
from face_detector import face_detector, read_cam
import signal
import cv2

if __name__ == '__main__':
    print "main"
    frames = Queue(10)
    faces = Queue()
    frame_getter_process = Process(target=face_detector, args=(frames, faces, True, "./faces/"))
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
