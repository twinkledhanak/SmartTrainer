import cv2
import numpy as np

red = np.uint8([[[251,120,100]]])  # bgr format

tobgr = cv2.cvtColor(red,cv2.COLOR_RGB2BGR)
print('bgr:: ',tobgr)
tohsv = cv2.cvtColor(tobgr,cv2.COLOR_BGR2HSV)
print('hsv::  ',tohsv)

BGR_red = cv2.cvtColor(red,cv2.COLOR_HSV2BGR)
print(BGR_red)

RGB_red = cv2.cvtColor(BGR_red,cv2.COLOR_BGR2RGB)
print (RGB_red)