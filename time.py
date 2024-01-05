import cv2
import time

video = cv2.VideoCapture(0); # argument is 0 because we want ref to webcam
num_frames = 300 # no of frames control the time, more frames, more time
# if we want to wait for 10 secs in live video, we give num_frames as 300
start = time.time()
elapsed = 0
if elapsed == 0:
    print(elapsed)

for i in range(0, num_frames):
    ret, frame = video.read()

end = time.time()

#elapsed = end-start
print (elapsed)