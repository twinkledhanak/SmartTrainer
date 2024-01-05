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

# body-part details
# blue1 = left leg     blue2 = right leg
# green1 = left hand   green2 = right hand
# blue/green = neck , hip

# colour details
# left hand
green1Lower = np.array([40, 80, 6], np.uint8)
green1Upper = np.array([80, 255, 255], np.uint8)

# right hand
green2Lower = np.array([40, 80, 6], np.uint8)
green2Upper = np.array([80, 255, 255], np.uint8)

# left leg
blue1Lower = np.array([80, 150, 10], np.uint8)
blue1Upper = np.array([170, 255, 255], np.uint8)

# right leg
blue2Lower = np.array([80, 150, 10], np.uint8)
blue2Upper = np.array([170, 255, 255], np.uint8)

# 2 pts, to have count for 2 different buffers
ptsg1 = deque(maxlen=args["buffer"])  # g1
ptsg2 = deque(maxlen=args["buffer"])  # g2
ptsb1 = deque(maxlen=args["buffer"])  # b1
ptsb2 = deque(maxlen=args["buffer"])  # b2

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
        # for cB1 in max(contBlue1, key=cv2.contourArea):
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
    # print(elapsed)

    # elapsed time has to be as per set as per posture time in video
    if elapsed == gap:  # num_frames will be >300 for bigger video, hence elapsed time>10 secs
        print("5 seconds elapsed")
        try:
            print("hello")

            # IN THE BEGINNING
            # 1. exercise details to be fetched
            # 2. know which co-ordinates have to be extracted
            ########   VALUE IN PARENTHESIS HAS TO BE PASSED ON ONCLICK
            etype, epair, emeasure = posture.getExerciseDetails("tadasana")
            print("Type:::", etype)
            print("pairs::", epair)
            print("measure::", emeasure)

            # KNOW WHICH COORDS HAVE TO BE EXTRACTED

            # example of pair: N-RH#RH-RL

            listBands = posture.getBandName(epair)  # from the pair , get individual band name
            # list returned is: B, G2 , G2 , B2
            # list can also be returned as having multiple values,
            # but hardcoding, assume , only 4 bands returned

            # method is present in the same file, not inside posture.py
            x1, y1 = getCoordinates(listBands[0])
            x2, y2 = getCoordinates(listBands[1])

            # calculate the first measurement
            angle1 = posture.calculateSlope(x1, y1, x2, y2)

            x1, y1 = getCoordinates(listBands[2])
            x2, y2 = getCoordinates(listBands[3])

            angle2 = posture.calculateSlope(x1, y1, x2, y2)

            # combine these two for the user measurements
            umeasure = []
            umeasure.append(angle1, angle2)

            print("First angle ", angle1)
            print("Second angle ", angle2)

            # LATER
            # 1. extract co-ordinates
            # 2. calculate slope
            # 3. compare with database details and calculate percent error


            # posture.obtainExcerciseDetails()
            # if (centerBx > 0)
            # slope1 = posture.calculateSlope(centerBx, centerBy, centerGx, centerGy)
            # print("S1:",slope1,end=",")

        except IndexError:
            continue


    def getCoordinates(listBands):  # TRY TO KEEP THE LENGTH HERE AS 2 ONLY , EASY FOR MANIPULATION
        listCoords = []

        # FOR EACH BAND , RETURN 2 CORDINATES, APPENDING TO THE SAME ARRAY
        # LEFT TO MANIPULATE FOR NECK AND HIP
        if listBands == "G1":
            listCoords.append(centerG1x, centerG1y)
        if listBands == "G2":
            listCoords.append(centerG2x, centerG2y)
        if listBands == "B1":
            listCoords.append(centerB1x, centerB1y)
        if listBands == "B2":
            listCoords.append(centerB2x, centerB2y)

        if listBands == "":  # neck
            listCoords.append()

        if listBands == "":  # hip
            listCoords.append()

        return listCoords





        # because the window is displayed in horizontal format instead of vertical
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
