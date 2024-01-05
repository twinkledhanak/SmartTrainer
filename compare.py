from collections import deque
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help= "path to the file")
ap.add_argument("-b","--buffer", type=int, default=128,help="max buffer size")
args = vars(ap.parse_args())

# colour details
greenLower = np.array([29, 80, 6],np.uint8)
greenUpper = np.array([64, 255, 255],np.uint8)

pts1 = deque(maxlen=args["buffer"])

if not args.get("video", False):
    camera = cv2.VideoCapture(0)

else:
    camera = cv2.VideoCapture(args["video"])

while True:
             (grabbed, frame) = camera.read()
             if args.get("video") and not grabbed:
                 break

             frame = imutils.resize(frame, width=600)  # take the frame and resize
             blurred = cv2.GaussianBlur(frame, (11, 11), 0)  # blur it
             hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # convert to hsv

             maskGreen = cv2.inRange(hsv, greenLower, greenUpper)
             maskGreen = cv2.erode(maskGreen, None, iterations=5)
             maskGreen = cv2.dilate(maskGreen, None, iterations=3)
             contGreen = cv2.findContours(maskGreen.copy(), cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)[-2]
             centerGreen = None
             if (len(contGreen) ) > 0:
                 cG = max(contGreen, key=cv2.contourArea)
                 ((x, y), radius) = cv2.minEnclosingCircle(cG)  # minimum enclosing circle
                 M = cv2.moments(cG)  # finding centroid of the circle
                 centerG = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                 if radius > 10: # radius of circle (which is drawn to fit an object)
                     cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255,0), 2)
                     cv2.circle(frame,centerG,5,(0,255,0),-1)
                     pts1.appendleft(centerG)
                     print("Appended")


             for i in range(1, len(pts1)):  # green
                     if pts1[i - 1] is None or pts1[i] is None:
                         continue
                     thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 1.5)
                     cv2.line(frame, pts1[i - 1], pts1[i], (0, 255, 0), thickness)

             cv2.imshow("Frame", frame)
             key = cv2.waitKey(1) & 0xFF

                     # if the 'q' key is pressed, stop the loop
             if key == ord("q"):
               break

                         # cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
