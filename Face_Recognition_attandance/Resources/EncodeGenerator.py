import cv2
import face_recognition
import pickle
import os 
import firebase_admin 
from firebase_admin import credentials , db, storage

cred = credentials.Certificate("Resources\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendance-51b81-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendance-51b81.appspot.com"
})

folderpath = "Images"

modepathlist = os.listdir(folderpath)
imglist = []
studids = []

# Read images from modepath and append them to modelist
for path in modepathlist:

    imglist.append(cv2.imread(os.path.join(folderpath, path)))
    #print(f"Failed to read image at {os.path.join(folderpath, path)}")
    studids.append(os.path.splitext(path)[0])
    #print(len(imglist))

    fileName = f'{folderpath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


print(studids)


def findencodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode= face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


print("Encoding Started")
encodinglistknown = findencodings(imglist)
encodelistknownwithids = [encodinglistknown, studids]

print("Encoding Complete")

file = open("EncodeFile.p",'wb')
pickle.dump(encodelistknownwithids, file)
file.close()
