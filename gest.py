import cv2
import imutils
import numpy as np

bg= None

def run_avg(image,wt):
    global bg

    if bg is None:
        bg=image.copy().astype('float')
        return

    cv2.accumulate(image,bg,wt)

def segment(image,threshold=25):
    global bg


    diff =  cv2.absdiff(bg.astype('uint8'),image)
    thresholded=cv2.threshold(
        diff,
        threshold,
        255,
        cv2.THRESH_BINARY
    )[1]

    (_,cont,_)=cv2.findContours(
        thresholded.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    if len(cont) == 0:
        return
    else:
        segmented=max(cont,key=cv2.contourArea)
        return (thresholded,segmented)

if __name__ == '__main__':

    wt=0.5

    camera = cv2.VideoCapture(0)

    top,right,bottom,left = 10,350,225,590

    count_frame=0

    while(True):
        (grabbed,frame)=camera.read()
        print frame
        break
        frame=imutils.resize(frame,width=700)
        frame=cv2.flip(frame,1)
        clone=frame.copy()
        (height,width)=frame.shape[:2]

        roi=frame[top:bottom , right:left]

        gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        gray= cv2.GaussianBlur(gray,(7,7),0)

        if count_frame <0 :
            run_avg(gray,wt)
        else:
            hand=segment(gray)
            if hand is not None :
                (thresholded,segmented)=hand
