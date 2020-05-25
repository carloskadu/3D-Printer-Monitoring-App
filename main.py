import numpy as np
import datetime
import cv2
import json
import requests

def changeDataInServer(key, new_value):
    while True:    
        # URL the Server
        url = input('Insert the server link: ')

        # Buscando o URL do WebAPI
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

    with open('comunication.json','w') as arquivo: # Converting string for json
        json_acceptable = str(json_data).replace("'","\"")
        arquivo.write(json_acceptable)
        arquivo.close()

def main():
    changeDataInServer('codigo', 'ligado')
    Carlos=datetime.datetime.now()
    print(Carlos)
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
    Thaisa = "Não acabou"

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
        if count <= 500 :
            if s != "Movimento":
                t=i
                t1=datetime.datetime.now()
                i=int(t1.second)
                if t!=i and Thaisa != "Acabou" :
                    z+=1
                    if z==20 and Thaisa == "Não acabou":
                        Nono=datetime.datetime.now()
                        Mafe=Nono-Carlos
                        print('A impressão durou:{}'.format(Mafe))
                        print("Acabou a impressão")
                        changeDataInServer('estado', 'desligado')
                        f=0
                        i=0 
                        z=0
                        Thaisa = "Acabou"
                
        else:
            z=0
            Thaisa = "Não acabou"
            if s != "Parado":
                changeDataInServer('estado', 'ligado')
                print(s)
                s = "Parado"
                Thaisa = "Não acabou"

        cv2.imshow('Frame', resizedFrame)
        cv2.imshow('Mask', fgmask)
        
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    capture.release()
    changeDataInServer('estado', 'ligado')
    cv2.destroyAllWindows()

main()