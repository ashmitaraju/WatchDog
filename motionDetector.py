from frameGrabber import get_frame
import imutils
import cv2


def motion_detector(send_queue, cam_host=0):
    prev_frame = None

    # loop over the frames of the video
    count = 0

    cam = cv2.VideoCapture(cam_host)

    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        frame = get_frame(cam)

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        # if not grabbed:
        #   break

        # resize the frame, convert it to gray scale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if prev_frame is None:
            prev_frame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frame_delta = cv2.absdiff(prev_frame, gray)
        if count % 5 == 0:
            prev_frame = gray
            count = 1
        count += 1
        thresh = cv2.threshold(frame_delta, 127, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if cnts:
            # print "occupied"
            send_queue.put(frame)