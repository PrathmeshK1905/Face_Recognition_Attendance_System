import cv2
import os
import cvzone
import numpy as np
import pickle
import face_recognition

import firebase_admin 
from firebase_admin import credentials , db, storage

cred = credentials.Certificate("Resources\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendance-51b81-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendance-51b81.appspot.com"
})


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 360)

imgbk = cv2.imread("Resources/Background_img.png")
modepath = "Resources/Modes"

modepathlist = os.listdir(modepath)
modelist = []

# Read images from modepath and append them to modelist
for path in modepathlist:
    img = cv2.imread(os.path.join(modepath, path))
    
    # Check if the image is successfully read
    if img is not None:
        modelist.append(img)
    else:
        print(f"Failed to read image at {os.path.join(modepath, path)}")

#load encoding file
print("Loading File....")
file = open("EncodeFile.p",'rb')
encodelistknownwithids = pickle.load(file)
file.close()
print("Loaded File successfully....")
encodelistknow , studids = encodelistknownwithids
print(studids)

modetype = 0
counter = 0
id = -1

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    facecurframe = face_recognition.face_locations(imgS)

    encodecurframe = face_recognition.face_encodings(img, facecurframe)

    # Resize img to match the dimensions of the slice you want to replace
    img = cv2.resize(img, (640, 480))

    # Replace the slice with the image from modelist[3] (or adjust the index as needed)
    imgbk[162:162+480, 55:55+640] = img
    imgbk[44:44+633, 808:808+414] = modelist[modetype]   # Use 0 if modelist is empty

    for encodeFace, faceLoc in zip(encodecurframe, facecurframe):
        matches = face_recognition.compare_faces(encodelistknow, encodeFace)
        faceDist = face_recognition.face_distance(encodelistknow, encodeFace)
        #print("Matches:", matches)
        #print("Distance:", faceDist)

        matchIndex = np.argmin(faceDist)

        #if matches[matchIndex]:
            #print("Face Detected")
            #print(studids[matchIndex])

        y1 ,x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        bbox = 55+x1, 162+y2, x2-x1 , y2-y1
        imgbk = cvzone.cornerRect(imgbk,bbox, rt=0)

        id = studids[matchIndex]
        if counter == 0:
            counter = 1
            modetype = 1

        if counter!= 0:
            if counter ==1:
                studentinfo = db.reference(f'Students/{id}').get()
                print(studentinfo) 

                cv2.putText(imgbk, str(studentinfo['Total Attendence']),(861,125),
                        cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                counter += 1

        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #  # Use the Haar Cascade classifier for face detection
        # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # for (x, y, w, h) in faces:
        # # Draw rectangle around the face
        #     cv2.rectangle(imgbk, (x, y), (x + w, y + h), (255, 0, 0), 2)



    cv2.imshow("Face attendance", imgbk)
    cv2.waitKey(1)

