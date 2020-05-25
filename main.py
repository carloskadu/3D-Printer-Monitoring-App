import numpy as np
import datetime
import cv2
import json
import requests

def changeDataInServer(key, new_value):
    while True:    
        #URL
        url = "http://192.168.0.101:8080/%C3%81rea%20de%20Trabalho/priorities.json"

        #Buscando o URL do WebAPI
        req = requests.get(url)

        #Tentativa de acesso
        try:
            #Leitura da WebAPI
            json_data = req.json()
            break

        except json.decoder.JSONDecodeError:
            continue

    #Substituindo para um novo valor da chave
    json_data[key] = new_value

    with open('priorities.json','w') as arquivo:
        json_acceptable = str(json_data).replace("'","\"")
        arquivo.write(json_acceptable)
        arquivo.close()

changeDataInServer('codigo', 'ligado')
# Video Capture 
# capture = cv2.VideoCapture(0)
capture = cv2.VideoCapture(0)

# History, Threshold, DetectShadows 
# fgbg = cv2.createBackgroundSubtractorMOG2(50, 200, True)
fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

# Keeps track of what frame we're on
frameCount = 0

s = "The impression has started!"

#time variables
i=0 #indicates the time the time counting started
z=0 #indicates the delta time 

T = "Not over" #Variable T indicates the stage of the impression

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
     if count <= 500 and T == "Not over": #The T variable looks for a time of no movement to detect if the impression is over
        if s != "Moving":
            t=i
            t1=datetime.datetime.now() #get the current time 
            i=int(t1.second) #extract oly seconds from the current time
            if t!=i and T == "Not over":
                z+=1
                 if z==10 and T =="Not over":
                    print("Done!!!")
                    changeDataInServer('estado', 'desligado')
                    f=0
                    i=0 
                    z=0
                    T = "End"
            
    else:
        z=0
        T = "Not over"
        if s != "Parado":
            changeDataInServer('estado', 'ligado')
            print(s)
            s = "Stoped"
            T = "Not over"

    cv2.imshow('Frame', resizedFrame)
    cv2.imshow('Mask', fgmask)
    
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
capture.release()
changeDataInServer('estado', 'ligado')
cv2.destroyAllWindows()
