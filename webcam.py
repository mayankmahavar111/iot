import cv2
import urllib2
import numpy as np
import sys




host = "10.100.55.37:8080"
if len(sys.argv)>1:
    host = sys.argv[1]

hoststr = 'http://' + host + '/video'
print 'Streaming ' + hoststr
"""
username = 'mayank'
password = 'mayank'
p = urllib2.HTTPPasswordMgrWithDefaultRealm()

p.add_password(None, hoststr, username, password)

handler = urllib2.HTTPBasicAuthHandler(p)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)
"""
stream=urllib2.urlopen(hoststr)

bytes=''
while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
        #cv2.imshow(hoststr,i)
        print "Hello World",
        #print i
        print len(i)
        print len(i[0])
        break
        if cv2.waitKey(1) ==27:
            exit(0)