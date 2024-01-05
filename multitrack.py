from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import posture

# ALWAYS FOLLOW B-G-R FORMAT IN ANY CV2 FUNCTION

# argument parsing
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the file")
ap.add_argument("-b", "--buffer", type=int, default=128, help="max buffer size")
args = vars(ap.parse_args())

# colour details
green1Lower = np.array([40, 80, 6], np.uint8)
green1Upper = np.array([80, 255, 255], np.uint8)

green2Lower = np.array([40, 80, 6], np.uint8)
green2Upper = np.array([80, 255, 255], np.uint8)

#redLower = np.array([100,200,200], np.uint8)
#redUpper = np.array([169, 200 ,200], np.uint8)

blue1Lower = np.array([80,150,10], np.uint8)
blue1Upper = np.array([170, 255 ,255], np.uint8)

blue2Lower = np.array([80,150,10], np.uint8)
blue2Upper = np.array([170, 255 ,255], np.uint8)

#orangeLower = np.array([4,153,251], np.uint8)
#orangeUpper = np.array([4,153,251], np.uint8)
#yellowLower = np.array([25, 146 , 190], np.uint8)
#yellowUpper = np.array([62, 174, 250], np.uint8)

# 2 pts, to have count for 2 different buffers
ptsg1 = deque(maxlen=args["buffer"]) # g1
ptsg2 = deque(maxlen=args["buffer"]) # g2
ptsb1 = deque(maxlen=args["buffer"]) # b1
ptsb2 = deque(maxlen=args["buffer"]) # b2

gap = 9

# trying to grab the camera ref
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
    start = time.time()
    elapsed = 0

else:
    camera = cv2.VideoCapture(args["video"])
    start = time.time()
    elapsed = 0
while True:
        (grabbed, frame) = camera.read()
        if args.get("video") and not grabbed:
            break

        frame = imutils.resize(frame, width=600)  # take the frame and resize
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)  # blur it
        #blurred = cv2.medianBlur(frame,5)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # convert to hsv

        # determine the no of elifs as per posture
        # this takes care of 3 postures
        if elapsed >= gap:
            print("Upper elapsed for 10 seconds")
            start = time.time()
        elif elapsed == 12:
            print("Upper elapsed for 4 seconds")
            start = time.time()
        elif elapsed == 15:
            print("Upper elapsed for 6 seconds")
            start = time.time()

        maskGreen1 = cv2.inRange(hsv, green1Lower, green1Upper)
        maskGreen1 = cv2.erode(maskGreen1, None, iterations=5)
        maskGreen1 = cv2.dilate(maskGreen1, None, iterations=3)

        maskGreen2 = cv2.inRange(hsv, green2Lower, green2Upper)
        maskGreen2 = cv2.erode(maskGreen2, None, iterations=5)
        maskGreen2 = cv2.dilate(maskGreen2, None, iterations=3)


        maskBlue1 = cv2.inRange(hsv, blue1Lower, blue1Upper)
        maskBlue1 = cv2.erode(maskBlue1, None, iterations=5)
        maskBlue1 = cv2.dilate(maskBlue1, None, iterations=3)

        maskBlue2 = cv2.inRange(hsv, blue2Lower, blue2Upper)
        maskBlue2 = cv2.erode(maskBlue2, None, iterations=5)
        maskBlue2 = cv2.dilate(maskBlue2, None, iterations=3)

        #maskOrange = cv2.inRange(hsv, orangeLower, orangeUpper)
        #maskOrange = cv2.erode(maskOrange, None, iterations=5)
        #maskOrange = cv2.dilate(maskOrange, None, iterations=3)


        contGreen1 = cv2.findContours(maskGreen1.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)[-2]
        contGreen2 = cv2.findContours(maskGreen2.copy(), cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)[-2]

        contBlue1 = cv2.findContours(maskBlue1.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]
        contBlue2 = cv2.findContours(maskBlue2.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]

        centerG1 = None
        centerG1x = None
        centerG1y = None

        centerG2 = None
        centerG2x = None
        centerG2y = None

        centerB1 = None
        centerB1x = None
        centerB1y = None

        centerB2 = None
        centerB2x = None
        centerB2y = None


        flagGreen1 = 0
        flagBlue1 = 0

        flagGreen2 = 0
        flagBlue2 = 0

        # -------------------------------------------------------------------------------------------
        if (len(contGreen1)) > 0:
            cG1 = max(contGreen1, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(cG1)  # minimum enclosing circle
            M = cv2.moments(cG1)  # finding centroid of the circle
            centerG1 = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            centerG1x = int(M["m10"] / M["m00"])
            centerG1y = int(M["m01"] / M["m00"])
            if radius > 10:
                flagGreen1 = 1  # flag set true, indicates object was detected
                print("......G1")
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.circle(frame, centerG1, 5, (0, 255, 0), -1)
                ptsg1.appendleft(centerG1)

        if (len(contGreen2)) > 0:
            cG2 = max(contGreen2, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(cG2)  # minimum enclosing circle
            M = cv2.moments(cG2)  # finding centroid of the circle
            centerG2 = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            centerG2x = int(M["m10"] / M["m00"])
            centerG2y = int(M["m01"] / M["m00"])
            if radius > 10:
                flagGreen2 = 1  # flag set true, indicates object was detected
                print("......G2")
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.circle(frame, centerG2, 5, (0, 255, 0), -1)
                ptsg2.appendleft(centerG2)



        if (len(contBlue1)) > 0:
                cB1 = min(contBlue1, key=cv2.contourArea)
            #for cB1 in max(contBlue1, key=cv2.contourArea):
                ((x, y), radius) = cv2.minEnclosingCircle(cB1)  # minimum enclosing circle
                M = cv2.moments(cB1)  # finding centroid of the circle

                centerB1 = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                centerB1x = int(M["m10"] / M["m00"])
                centerB1y = int(M["m01"] / M["m00"])

                if radius > 10:
                    flagBlue1 = 1
                    print("......B1")
                    cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                    cv2.circle(frame, centerB1, 5, (255, 0, 0), -1)
                    ptsb1.appendleft(centerB1)

        if (len(contBlue2)) > 0:
                cB2 = max(contBlue2, key=cv2.contourArea)
          #  for cB2 in max(contBlue2, key=cv2.contourArea):
                ((x, y), radius) = cv2.minEnclosingCircle(cB2)  # minimum enclosing circle
                M = cv2.moments(cB2)  # finding centroid of the circle

                centerB2 = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                centerB2x = int(M["m10"] / M["m00"])
                centerB2y = int(M["m01"] / M["m00"])

                if radius > 10:
                    flagBlue2 = 1
                    print("......B2")
                    cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                    cv2.circle(frame, centerB2, 5, (255, 0, 0), -1)
                    ptsb2.appendleft(centerB2)

                # -----------------------------------------------------------------------------------------

        for i in range(1, len(ptsg1)):  # green
            if ptsg1[i - 1] is None or ptsg1[i] is None:
                continue
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 1.5)
            cv2.line(frame, ptsg1[i - 1], ptsg1[i], (0, 255, 0), thickness)
            # drawing line from prev pt to current pt

        for i in range(1, len(ptsg2)):  # green
            if ptsg2[i - 1] is None or ptsg2[i] is None:
                continue
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 1.5)
            cv2.line(frame, ptsg2[i - 1], ptsg2[i], (0, 255, 0), thickness)

        for i in range(1, len(ptsb1)):  # blue
            if ptsb1[i - 1] is None or ptsb1[i] is None:
                continue
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 0.5)
            cv2.line(frame, ptsb1[i - 1], ptsb1[i], (255, 0, 0), thickness)

        for i in range(1, len(ptsb2)):  # blue
            if ptsb2[i - 1] is None or ptsb2[i] is None:
                continue
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 0.5)
            cv2.line(frame, ptsb2[i - 1], ptsb2[i], (255, 0, 0), thickness)
        # ------------------------------------------------------------------------------------------------


        end = time.time()  # end the timer
        elapsed = int(end - start)  # calculate elapsed time for each frame
        #print(elapsed)

        # elapsed time has to be as per set as per posture time in video
        if elapsed == gap:  # num_frames will be >300 for bigger video, hence elapsed time>10 secs
            print("5 seconds elapsed")
            try:
                  print("hello")
                  posture.obtainExcerciseDetails()
                  #if (centerBx > 0)
                  #slope1 = posture.calculateSlope(centerBx, centerBy, centerGx, centerGy)
                  #print("S1:",slope1,end=",")

            except IndexError:
                 continue

#        for angle in np.arange(0, 360, 15):
#            rotated = imutils.rotate_bound(frame, angle)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

            # cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
