# import the necessary packages
from collections import deque  # for the buffer
import numpy as np
import argparse    # for parsing the arguments provided in command line
import imutils     # has range-detector script to find hsv values for colours
import cv2
import time

# -------------------------------------------------------------------------------------------------------

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

# --video : indicates video switch , if present , opencv will grab pointer to our recorded video file
ap.add_argument("-v","--video",help="path to the (optional) video file")

# we add a default buffer size for object
# buffer holds all prev x,y cords of obj
# it is used to print path (tail) on the screen
# maximum size of buffer , longer is the tail of ball on the screen
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")

args = vars(ap.parse_args())

# -------------------------------------------------------------------------------------------------------

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# greenLower = (29, 80, 6)
# greenUpper = (64, 255, 255)

greenLower = (70,50,50) # contains value for red
greenUpper = (92,255,255)

pts = deque(maxlen=args["buffer"])

# -------------------------------------------------------------------------------------------------------


# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
    # keep looping
    start = time.time() # start the timer only once, cannot be inside while loop
while True:
        # grab the current frame
        # camera.read() returns 2 tuples, a boolean variable that indicates whether frame was read or not
        # and the actual video, frame
        (grabbed, frame) = camera.read()

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if args.get("video") and not grabbed:
            break

        # Take the frame,resize it, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)    # take the frame and resize
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)  # blur it
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    # convert to hsv

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        # mask is a small region created within the image
        # mask = cv2.inRange(src, lower bound , upper bound)

        mask = cv2.inRange(hsv,greenLower,greenUpper)
        mask = cv2.erode(mask, None, iterations=2)  # erode and dilate the mask twice
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        # contour is a continuous curve joining all the points along the object boundary

        # MASK DENOTES THE SMALL REGION WHERE OUR OBJECT LIES
        # CONTOUR DETERMINES THE OUTLINE OF OUR OBJECT WITHIN THE MASK
        # findContours(source , retrieval mode of opencv, contour approximation method)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)  # find maximum of the contour and
            ((x, y), radius) = cv2.minEnclosingCircle(c)    # minimum enclosing circle
            M = cv2.moments(c) # finding centroid of the circle
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (255, 255, 0), 2)
                cv2.circle(frame, center, 5, (255, 255,0), -1)
                # update the points queue
                pts.appendleft(center)

# ----------------------------------------------------------------------------------------------------
    # TRACKING CODE

        # loop over the set of tracked points
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        end = time.time() # end the timer
        elapsed = end-start # calculate elapsed time for each frame
        #print (elapsed)
        if elapsed > 4.0: # num_frames will be >300 for bigger video, hence elapsed time>10 secs
            print("5 seconds elapsed")


        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

    # cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()