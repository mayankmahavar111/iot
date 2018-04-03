import cv2
import os


camera_port = 0
ramp_frames = 60
camera = cv2.VideoCapture(camera_port)


def get_image():
    retval, im = camera.read()
    return im

def folder():
    try:
        os.mkdir('screenshot')
    except:
        pass

if __name__ == '__main__':
    for i in xrange(ramp_frames):
        temp = get_image()
    print("Taking image...")
    camera_capture = get_image()
    folder()
    file = "screenshot//mage.png"
    cv2.imwrite(file, camera_capture)

    del (camera)