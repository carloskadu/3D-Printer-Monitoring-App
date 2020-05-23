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
s = "The impression has started!"
i=0
f=0
z=0
<<<<<<< HEAD
T = "Not over" #Variable T indicates the stage of the impression
=======
T = "Not over"
>>>>>>> master
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
	# if (frameCount > 1 and count > 500):
    if count <= 500 and T == "Not over": #The T variable looks for a time of no movement to detect if the impression is over
        if s != "Moving":
            t=i
            t1=datetime.datetime.now()
            i=int(t1.second)
            if t!=i and T == "Not over":
                print(i)
                z+=1

                if i-f==20 or i-f==-19:
                    print("Done!")
                    T = "End"   
                    s="Moving"
                    f=0
                    i=0       
    else:
        z=0
        if s != "Stopped":
            print(s)
            s = "Stopped"


    cv2.imshow('Frame', resizedFrame)
    cv2.imshow('Mask', fgmask)
    
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
capture.release()
cv2.destroyAllWindows()
