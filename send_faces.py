import cv2
from faceVerify import get_face
from WindowManager import WindowManager


def send_faces(send_face_queue, response_face_queue):
    windowManager = WindowManager("Sent Face")
    while True:
        while send_face_queue.empty():
            pass
        img = send_face_queue.get()
        # window_sent_face = cv2.namedWindow("Sent Face", cv2.WINDOW_NORMAL)
        windowManager.put(img)
        frame_bytes = cv2.imencode('.jpg', img)[1].tostring()
        response = get_face(frame_bytes)
        response_face_queue.put([response, frame_bytes])
