import numpy as np
import datetime
import cv2

# Video Capture 
# capture = cv2.VideoCapture(0)
capture = cv2.VideoCapture(0)

# History, Threshold, DetectShadows 
# fgbg = cv2.createBackgroundSubtractorMOG2(50, 200, True)
fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

# Keeps track of what frame we're on
frameCount = 0
s = "Iniciou a impressão!"
i=0
f=0
z=0
Thaisa = "Não acabou" #Oi
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
    if count <= 500 and Thaisa == "Não acabou":
        if s != "Movimento":
            t=i
            t1=datetime.datetime.now()
            i=int(t1.second)
            if t!=i and Thaisa == "Não acabou":
                print(i)
                z+=1
                if z==1:
                    f=i
            if i-f==20 or i-f==-39:
                print("Acabou a impressão")
                Thaisa = "Fim"   
                s="Movimento"
                z=0
                f=0
                i=0       
    else:
        if s != "Parado":
            print(s)
            s = "Parado"
    if Thaisa == "Fim":

    cv2.imshow('Frame', resizedFrame)
    cv2.imshow('Mask', fgmask)
    
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
capture.release()
cv2.destroyAllWindows()