import cv2
import urllib2
import numpy as np
import sys

host = "192.168.31.116:8080"
if len(sys.argv) > 1:
    host = sys.argv[1]

host_str = 'http://' + host + '/videofeed'
print 'Streaming ' + host_str

stream = urllib2.urlopen(host_str)

bytes_str = b''
while True:
    bytes_str += stream.read(1024)
    a = bytes_str.find('\xff\xd8')
    b = bytes_str.find('\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes_str[a:b + 2]
        bytes_str = bytes_str[b + 2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow(host_str, i)
        if cv2.waitKey(1) == 27:
            exit(0)
