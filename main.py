import numpy as np
import datetime
import cv2
import json
import requests
import os

def changeDataInServer(key, new_value):
    while True:    
        # URL the Server
        url = input('Insert the server link: ') + os.getcwd() + '/comunication.json'

        # Searching the URL of WebAPI
        req = requests.get(url)

        # Try to access
        try:
            # Reading WebAPI
            json_data = req.json()
            break

        except json.decoder.JSONDecodeError:
            continue

    # Replacing for a new key value
    json_data[key] = new_value

    # Converting string to json
    with open('comunication.json','w') as archive:
        json_acceptable = str(json_data).replace("'","\"")
        archive.write(json_acceptable)
        archive.close()

def main():
    changeDataInServer('Code', 'On')
    # Video Capture 
    capture = cv2.VideoCapture(0)

    # History, Threshold, DetectShadows 
    fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

    # Keeps track of what frame we're on
    frameCount = 0

    #status variables 
    situation = "The impression has started!" # shows the current impression status

    #time variables
    initTime=0 #indicates the time the time counting started
    deltaTime=0 #indicates the delta 

    end = "Not over" #Variable T indicates the stage of the impression

    while(1):
        # Return Value and the current frame
        ret, frame = capture.read()

        #  Check if a current frame actually exist
        if not ret:
            break

        # Resize the frame
        resizedFrame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

        # Get the foreground mask
        fgmask = fgbg.apply(resizedFrame)

        # Count all the non zero pixels within the mask
        count = np.count_nonzero(fgmask)


        # Determine how many pixels do you want to detect to be considered "movement"
        if count <= 500 and end == "Not over": #The end variable looks for a time of no movement to detect if the impression is over
            if situation != "Moving":
                t=initTime
                currentTime=datetime.datetime.now() #get the current time 
                initTime=int(currentTime.second) #extract oly seconds from the current time
                if t!=initTime and end == "Not over":
                    deltaTime+=1
                    if deltaTime==10 and end =="Not over":
                        
                        print("Done!!!")
                        
                        changeDataInServer('Status', 'Off')

                        initTime=0 
                        deltaTime=0
                        end = "End"
                
        else:
            deltaTime=0
            end = "Not over"
            if situation != "Stoped":
                changeDataInServer('Status', 'On')
                print(s)
                situation = "Stoped"
                end = "Not over"

        cv2.imshow('Frame', resizedFrame)
        cv2.imshow('Mask', fgmask)
        
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    capture.release()
    changeDataInServer('Status', 'On')
    cv2.destroyAllWindows()

main()
