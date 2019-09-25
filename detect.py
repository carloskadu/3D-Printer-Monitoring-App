import cv2
import numpy as np
import datetime
import time
# Video Capture 
# capture = cv2.VideoCapture(0)
capture = cv2.VideoCapture("Nada.mp4")
# History, Threshold, DetectShadows 
# fgbg = cv2.createBackgroundSubtractorMOG2(50, 200, True)
fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

# Keeps track of what frame we're on
frameCount = 0
s = "Inicio da impressão!"

while(1):
	# Return Value and the current frame
    ret, frame = capture.read()

	#  Check if a current frame actually exist
    if not ret:
        break

    # frameCount += 1
	# Resize the frame
    resizedFrame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

	# Get the foreground mask
    fgmask = fgbg.apply(resizedFrame)

	# Count all the non zero pixels within the mask
    count = np.count_nonzero(fgmask)


	# Determine how many pixels do you want to detect to be considered "movement"
	# if (frameCount > 1 and count > 5000):
    x=np.count_nonzero(fgmask)
   
    if count > 500:
        if s != "Parado":
            print(s)
            s = "Parado"
    else:
        if s != "Movimento":
            time.sleep(10)
            if count<500:
                print(s)
                s = "Movimento"


            
    cv2.imshow('Frame', resizedFrame)
    cv2.imshow('Mask', fgmask)


    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
capture.release()
cv2.destroyAllWindows()
