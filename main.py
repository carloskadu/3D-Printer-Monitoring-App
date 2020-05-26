import numpy as np
import datetime
import cv2
import json
import requests

def changeDataInServer(key, new_value):
    while True:    
        # URL the Server
        url = input('Insert the server link: ')

        # Searching the URL WebAPI
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

    with open('comunication.json','w') as arquivo: # Converting string to json
        json_acceptable = str(json_data).replace("'","\"")
        arquivo.write(json_acceptable)
        arquivo.close()

def main():
    changeDataInServer('code', 'on')
    time = datetime.datetime.now() # Your local time
    print(time)
    # Video Capture 
    capture = cv2.VideoCapture(0)

    # History, Threshold, DetectShadows 
    fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

    status = "The impression has started!" # Says if it is moving or not
    i=0
    f=0
    z=0
    end = "Not over" # Say the progress of the impression

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
        if count <= 500 : # Condition to see if the movement has stopped and start the countdown
            if status != "Moving":
                t=i
                t1=datetime.datetime.now()
                i=int(t1.second)
                if t!=i and end != "End" :
                    z+=1
                    if z==20 and end == "Not over":
                        finalTime = datetime.datetime.now()
                        deltaTime = finalTime - time
                        print("Printing is done!")
                        print('Time:{}'.format(deltaTime))
                        changeDataInServer('switch', 'off')
                        f=0
                        i=0 
                        z=0
                        end = "End"
                
        else:
            z=0
            end = "Not over"
            if status != "Stopped":
                changeDataInServer('switch', 'on')
                print(status)
                status = "Stopped"
                end = "Not over"

        cv2.imshow('Frame', resizedFrame)
        cv2.imshow('Mask', fgmask)
        
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    capture.release()
    changeDataInServer('switch', 'on')
    cv2.destroyAllWindows()

main()
