import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL' : "https://attendancesystemrtcv-default-rtdb.firebaseio.com/",
                                  'storageBucket' : "attendancesystemrtcv.appspot.com"
                              })


# Importing the student images into a list
folderPath = "Images"
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    # print(path)
    # print(os.path.splitext(path)[0])
    # split the image name and get the first index i.e ID
    studentIds.append(os.path.splitext(path)[0])
    fileName = f"{folderPath}/{path}"
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    # print(fileName)

print(studentIds)

def findEncodings(images):
    encodelist = []
    for IMAGES in images:
        IMAGES = cv2.cvtColor(IMAGES,cv2.COLOR_BGR2RGB)
        faceEnc = face_recognition.face_encodings(IMAGES)[0]
        encodelist.append(faceEnc)
    return encodelist


print(imgList)
print("Encodings Started......")
encodeListKnown = findEncodings(imgList)
encodeListKnownIds = [encodeListKnown,studentIds]
# print(encodeListKnown)
print("Encodings complete")
file = open("EncodeFile.p","wb")
pickle.dump(encodeListKnownIds,file)
file.close()
print("File saved")

