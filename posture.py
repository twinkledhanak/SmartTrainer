import cv2
import numpy as np
from firebase import firebase
import json

def extractCoordinates(a, b, c, d):
    print(a)
    print(b)
    print(c)
    print(d)

    print("Extracting coordinates now!!!")
    return calculateSlope(a, b, c, d)


# details: type, what to detect (G1,B1 as per LH,RH), measurements
def obtainExcerciseDetails():
    f = firebase.FirebaseApplication('https://smarttrainer-49e2a.firebaseio.com/', None)
    lh = "green"
    rh = "blue"
    try:
        value = json.dumps(f.get('/Exercises/Tadasana/type/-L9AC-9LZ69FpEnQeEr1', None))
        print(value)
    except IndexError:
        print("cant fetch values")
   # print("Exercise details:",value)
    #for i in range(0,5):
     #   print(value[i])

    handLeg = 26  # obtain exact measure
    return lh, rh


def calculateSlope(a, b, c, d):
    # calculate posture
    print("Calculating posture")
    angle = 0 # initial value
    try:
       # if (a > 0) & (b > 0) & (c > 0) & (d > 0):
            slope = ((d-b) / (c-a))
            angle = np.degrees(np.arctan(slope))
            return angle
     #   else:
      #      slope = 0
       #     angle = np.degrees(np.arctan(slope))
        #    return angle
    except IndexError:
        print()
        return 999


obtainExcerciseDetails()