import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL' : "https://attendancesystemrtcv-default-rtdb.firebaseio.com/",
                                  'storageBucket' : "attendancesystemrtcv.appspot.com"
                              })

cap = cv2.VideoCapture(0)
bucket = storage.bucket()
cap.set(3,640)
cap.set(4,480)

imgBackground = cv2.imread("Resources/background.png")

# Importing the mode images into a list
folderModePath = "Resources/Modes"
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
# print(len(imgModeList))

# import/load the encoding file
print("Loaded encoded file")
file = open('EncodeFile.p','rb')
encodeListKnownwithIds = pickle.load(file)
file.close()
encodeListKnown,studentIds = encodeListKnownwithIds
# print(studentIds)
print("encoded file Loaded")

modetype = 0
counter = 0
id = -1
imgStudent = []

while(True):
    sucess,frame = cap.read()
    imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = frame
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                bbox = 55 + x1,162 + y1,x2 - x1,y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"loading",(275,400))
                    cv2.imshow("Face attendence", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modetype = 1
        if counter!= 0:
            if counter == 1:
                # get the data
                studentInfo = db.reference(f'Students/{id}').get()
                # get the image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(),np.uint8)
                imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                # update data of attendence
                datetimeObject = datetime.datetime.strptime(studentInfo["last_attendence_time"],
                                                            "%Y-%m-%d %H:%M:%S")
                secondsElasped = (datetime.datetime.now() - datetimeObject).total_seconds()
                if secondsElasped > 10:
                    ref = db.reference(f'Students/{id}')
                    studentInfo["total_attendence"] += 1
                    ref.child('total_attendence').set(studentInfo["total_attendence"])
                    ref.child('last_attendence_time').set(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modetype = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]

            if modetype != 3:
                if 10<counter<20:
                    modetype = 2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]

                if counter<=10:

                    cv2.putText(imgBackground,str(studentInfo['total_attendence']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.4,
                        (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                        (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['Year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                        (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['Starting_year']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                        (100, 100, 100), 1)
                    (w,h),_ = cv2.getTextSize(str(studentInfo['name']),cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (414 - w)//2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (50, 50, 50), 1)
                    imgBackground[175:175+216,909:909+216] = imgStudent
            counter+=1

            if counter >= 20:
                modetype = 0
                counter = 0
                studentInfo = []
                imgStudent = []
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]
    else:
        modetype = 0
        counter = 0
# place it inside the loop below 2 statements
# print(f"{studentIds[matchIndex]} Face Detected")
# print(studentIds[matchIndex])

    # cv2.imshow("frame",frame)
    cv2.imshow("Face attendence", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


