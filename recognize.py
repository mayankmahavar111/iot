import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise
#from webcam import camRead
from thing import post


bg = None




def filter(finger_list):
    temp=[]
    temp.append(finger_list[0])
    for i in range(1,len(finger_list)):
        if temp[-1] !=finger_list[i] and finger_list[i] !=0:
            temp.append(finger_list[i])
    test=temp
    temp=[]

    for i in range(len(test)-2):
        flag=0
        if test[i] == test[i+2] :
            flag=1
            temp.append(str(test[i])+str(test[i+1]) + str(test[i+2]))
            i=i+2
        else:
            temp.append(test[i])

    if flag == 0 :
        temp.append(test[-2])
        temp.append(test[-1])

    return temp


def run_avg(image, accumWeight):
    global bg

    if bg is None:
        bg = image.copy().astype("float")
        return

    cv2.accumulateWeighted(image, bg, accumWeight)


def segment(image, threshold=25):
    global bg
    diff = cv2.absdiff(bg.astype("uint8"), image)

    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    (_, cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) == 0:
        return
    else:
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)


def count(thresholded, segmented):
    chull = cv2.convexHull(segmented)

    extreme_top = tuple(chull[chull[:, :, 1].argmin()][0])
    extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
    extreme_left = tuple(chull[chull[:, :, 0].argmin()][0])
    extreme_right = tuple(chull[chull[:, :, 0].argmax()][0])

    cX = (extreme_left[0] + extreme_right[0]) / 2
    cY = (extreme_top[1] + extreme_bottom[1]) / 2

    distance = pairwise.euclidean_distances([(cX, cY)], Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
    maximum_distance = distance[distance.argmax()]

    radius = int(0.8 * maximum_distance)

    circumference = (2 * np.pi * radius)

    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")


    cv2.circle(circular_roi, (cX, cY), radius, 255, 1)

    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)

    (_, cnts, _) = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    count = 0

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)

        if ((cY + (cY * 0.25)) > (y + h)) and ((circumference * 0.25) > c.shape[0]):
            count += 1

    return count


if __name__ == "__main__":

    finger_list=[]

    accumWeight = 0.5

    camera = cv2.VideoCapture(0)

    top, right, bottom, left = 10, 350, 225, 590

    num_frames = 0

    calibrated = False

    bytes=''
    while (True):
        (grabbed, frame) = camera.read()
        """
        try:
            frame,bytes=camRead(bytes)
        except :
            (grabbed, frame) = camera.read()
        """

        frame = imutils.resize(frame, width=700)

        frame = cv2.flip(frame, 1)

        clone = frame.copy()

        (height, width) = frame.shape[:2]

        roi = frame[top:bottom, right:left]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if num_frames < 30:
            run_avg(gray, accumWeight)
            if num_frames == 1:
                print "[STATUS] please wait! calibrating..."
            elif num_frames == 29:
                print "[STATUS] calibration successfull..."
        else:
            #print "inside else"q
            hand = segment(gray)
            #print gray
            if hand is not None:
                (thresholded, segmented) = hand

                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))

                fingers = count(thresholded, segmented)
                #print fingers
                #post(fingers)
                finger_list.append(fingers)
                cv2.putText(clone, str(fingers), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                #print "show image"
                cv2.imshow("Thesholded", thresholded)
                #print "image is working"

        cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)

        num_frames += 1

        cv2.imshow("Video Feed", clone)

        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    finger_list=filter(finger_list)
    for finger in finger_list :
        print" {} finger is getting addded to cloud ".format(finger)
        post(finger)

