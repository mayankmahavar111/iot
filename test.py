import numpy as np
import cv2
import math

capture = cv2.VideoCapture(0)
print len(capture.read()[1])