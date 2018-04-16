# reading multiple videos together

import numpy as np
import cv2
import imutils

names = ['correct.mp4'];
window_titles = ['first']


cap = [cv2.VideoCapture(i) for i in names] # from video file
camera = cv2.VideoCapture(0) # webcam

frames = [None] * len(names);
hsv = [None] * len(names);
ret = [None] * len(names);

while True:

    for i,c in enumerate(cap):
        if c is not None:
            ret[i], frames[i] = c.read();

        


    for i,f in enumerate(frames):
        if ret[i] is True:
            f = imutils.resize(f, width=600) 
            hsv[i] = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
            cv2.imshow(window_titles[i], hsv[i]);

    
    (grabbed, frame) = camera.read()
    frame = imutils.resize(frame, width=600)  # take the frame and resize
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)  # blur it
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # convert to hsv
    cv2.imshow("Frames",frame)
       
          
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break


for c in cap:
    if c is not None:
        c.release();

cv2.destroyAllWindows()