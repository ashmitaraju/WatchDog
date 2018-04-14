import cv2

nextPosList = [
    [0, 0],
    [400, 0],
    [0, 400],
    [400, 400]
]

_nextPosIter = 0


def next_pos():
    global _nextPosIter
    pos = nextPosList[_nextPosIter]
    _nextPosIter = (_nextPosIter+1)%4
    return pos


class WindowManager(object):
    def __init__(self, name, size=(400, 400), pos=next_pos()):
        self.name = name
        self.size = size
        self.window = cv2.namedWindow(name, cv2.WINDOW_NORMAL | cv2.WINDOW_AUTOSIZE)
        cv2.resizeWindow(name, *size)
        # cv2.moveWindow(name, *pos)

    def put(self, img):
        img = cv2.resize(src=img, dsize=tuple(self.size))
        if img is None:
            print "\n\nNONENONENONE\n\n"
        cv2.imshow(self.name, img)

        cv2.waitKey(5)
