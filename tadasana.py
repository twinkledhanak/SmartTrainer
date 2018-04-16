# this file consists of code for tadasana only
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import posture
import os

# ALWAYS FOLLOW B-G-R FORMAT IN ANY CV2 FUNCTION

# argument parsing
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())


names = ['righttadasana.mp4'];
window_titles = ['first']


# body-part details
# green1 = left leg     green2 = right leg
# blue1 = left hand   blue2 = right hand
# green = hip         

# colour details

# left hand
blue1Lower = np.array([80, 150, 10], np.uint8)
blue1Upper = np.array([170, 255, 255], np.uint8)

# hip: green
greenLower = np.array([40, 80, 6], np.uint8)
greenUpper = np.array([80, 255, 255], np.uint8)


# right hand
blue2Lower = np.array([80, 150, 10], np.uint8)
blue2Upper = np.array([170, 255, 255], np.uint8)


# 2 pts, to have count for 2 different buffers
ptsb1 = deque(maxlen=args["buffer"])  # b1
ptsb2 = deque(maxlen=args["buffer"])  # b2
ptsg = deque(maxlen=args["buffer"]) # green : hip

gap = 30

# calling it in the start
etype, epair, emeasure = posture.getExerciseDetails("tadasana")
print("Type:::", etype)
print("pairs::", epair)
print("measure::", emeasure)

cap = [cv2.VideoCapture(i) for i in names] 
Rframes = [None] * len(names);
hsv = [None] * len(names);
ret = [None] * len(names);

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

#----------------------------------
# FOR RECORDED VIDEO
    for i,c in enumerate(cap):
        if c is not None:
            ret[i], Rframes[i] = c.read();        


    for i,f in enumerate(Rframes):
        if ret[i] is True:
            f = imutils.resize(f, width=600) 
           # hsv[i] = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
            cv2.imshow(window_titles[i], f)    
    #----------------------------------------------           
    # FOR LIVE VIDEO

    frame = imutils.resize(frame, width=600)  # take the frame and resize
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)  # blur it
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # convert to hsv



    maskBlue1 = cv2.inRange(hsv, blue1Lower, blue1Upper)
    maskBlue1 = cv2.erode(maskBlue1, None, iterations=5)
    maskBlue1 = cv2.dilate(maskBlue1, None, iterations=3)

    maskGreen = cv2.inRange(hsv, greenLower, greenUpper)
    maskGreen = cv2.erode(maskGreen, None, iterations=5)
    maskGreen = cv2.dilate(maskGreen, None, iterations=3)

    maskBlue2 = cv2.inRange(hsv, blue2Lower, blue2Upper)
    maskBlue2 = cv2.erode(maskBlue2, None, iterations=5)
    maskBlue2 = cv2.dilate(maskBlue2, None, iterations=3)

    contGreen = cv2.findContours(maskGreen.copy(), cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_SIMPLE)[-2]
    contBlue1 = cv2.findContours(maskBlue1.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)[-2]

    contBlue2 = cv2.findContours(maskBlue2.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)[-2]

    centerB1 = None
    centerB1x = None
    centerB1y = None
    
    centerG = None
    centerGx = None
    centerGy = None

    centerB2 = None
    centerB2x = None
    centerB2y = None

    
    flagBlue1 = 0
    flagBlue2 = 0
    flagGreen = 0

    # -------------------------------------------------------------------------------------------

    

    if (len(contGreen)) > 0:
        cG = max(contGreen, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cG)  # minimum enclosing circle
        M = cv2.moments(cG)  # finding centroid of the circle
        centerG = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        centerGx = int(M["m10"] / M["m00"])
        centerGy = int(M["m01"] / M["m00"])
        if radius > 10:
            flagGreen = 1  # flag set true, indicates object was detected
            print("......G")
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.circle(frame, centerG, 5, (0, 255, 0), -1)
            ptsg.appendleft(centerG)        

    if (len(contBlue1)) > 0:
        cB1 = max(contBlue1, key=cv2.contourArea)
        #  for cB2 in max(contBlue2, key=cv2.contourArea):
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

 

    for i in range(1, len(ptsg)):  # green
        if ptsg[i - 1] is None or ptsg[i] is None:
            continue
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 1.5)
        cv2.line(frame, ptsg[i - 1], ptsg[i], (0, 255, 0), thickness)
     
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
        print("30 seconds elapsed")
        try:
            print("hello")

            # IN THE BEGINNING
            # 1. exercise details to be fetched
            # 2. know which co-ordinates have to be extracted
            ########   VALUE IN PARENTHESIS HAS TO BE PASSED ON ONCLICK
           

            # KNOW WHICH COORDS HAVE TO BE EXTRACTED

            # example of pair: N-RH#RH-RL

            listBands = posture.getBandName(epair)  # from the pair , get individual band name
            # list returned is: G, G2 , G2 , B2
            # list can also be returned as having multiple values,
            # but hardcoding, assume , only 4 bands returned

            print("listBands::",listBands[0])
            print("listBands::",listBands[1])
            print("listBands::",listBands[2])
           # only 3 bands present , 
            print("listBands::",listBands[3])
            # method is present in the same file, not inside posture.py
            list1 = getCoordinates(listBands[0])
            list2 = getCoordinates(listBands[1])

            
            x1 = list1[0]
            y1 = list1[1] 

            x2 = list2[0]
            y2 = list2[1]

           
            # FIRST 2 BANDS
            print("Firstarrayofcords",x1,y1,x2,y2)    

            # calculate the first measurement
            try:
                a1 = posture.calculateSlope(x1, y1, x2, y2)
                a1 = 0
                os.system('python speechtotext.py')
            except IndexError:
                os.system('python speechtotext.py')    
            angle1 = int(a1)

            list3 = getCoordinates(listBands[2])
            list4 = getCoordinates(listBands[3])

            x3 = list3[0]
            y3 = list3[1]
            x4 = list4[0]
            y4 = list4[1]

            print("Secondarrayofcords",x1,y1,x2,y2)   
            try:
                a2 = posture.calculateSlope(x3, y3, x4, y4)
                a2 = 0
                os.system('python speechtotext.py')
            except IndexError:
                os.system('python speechtotext.py')    
            angle2 = int(a2)

            # combine these two for the user measurements
            # may be 2 or 3 , put different values in different files
            umeasure = []
            umeasure.append(angle1)
            umeasure.append(angle2)

            print("First angle ", angle1)
            print("Second angle ", angle2)

            result = emeasure.split('#')
            Trainerangle1 = result[0]
            Trainerangle2 = result[1]

            print("Trainerangle1",Trainerangle1)
            print("Trainerangle2",Trainerangle2)

            first = 0
            second = 0
             # 1 is true , 0 is false   
            if angle1 in range(int(Trainerangle1) - 50,int(Trainerangle1) + 50):
                first = 1  
            if angle2 in range(int(Trainerangle2) - 50,int(Trainerangle2) + 50 ):
                second = 1

            if first==1 or second==1:
                print("Correct Posture!!")
            else:
                os.system('python speechtotext.py')
                print("Wrong Posture!!")  
                print("Check position of your hands")            



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
        if listBands == "B1":
            listCoords.append(centerB1x)
            listCoords.append(centerB1y)
               

        elif listBands == "B2":
            listCoords.append(centerB2x)
            listCoords.append(centerB2y)

        elif listBands == "G":  # HIP
            listCoords.append(centerGx)
            listCoords.append(centerGy)

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
