import os
import cv2
import pickle
from datetime import datetime
import cvzone
import face_recognition
import numpy as np

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancereal-81e44-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancereal-81e44.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(5, 480)
cap.set(6, 640)
ImgBack = cv2.imread('resources/2.png')


# importing the images into the list
folderModePath = 'resources/modes'
modePathList = os.listdir(folderModePath)
imgmodeslist = []
for path in modePathList:
    imgmodeslist.append(cv2.imread(os.path.join(folderModePath, path)))


# importing the encoding file
file=open("Encoderfile.p", "rb")
encodeListKnownId = pickle.load(file)
file.close()
encodeListKnown, studentid= encodeListKnownId
#print(studentid)
print("Encode file loaded")

modType = 0
counter = 0
id = -1
imgStudent = []
array = []


while True:
    success, img = cap.read()


    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
   # compare photo nd image
    FaceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, FaceCurFrame)

    ImgBack[66:66+480, 70:70+640] = img
    ImgBack[44:44+748, 808:808+460] = imgmodeslist[modType]

    if FaceCurFrame:

        for encodeFace,faceLoc in zip(encodeCurFrame, FaceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            #print("matches", matches)
           # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
           # print("matchIndex", matchIndex)

            if matches[matchIndex]:
                 #print("face is detected")
                 y1,x2,y2,x1=faceLoc
                 y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                 bbox = 30+x1, 40+y1, x2-x1, y2-y1
                # ImgBack = cvzone.cornerRect(ImgBack,bbox,rt=0)
                 id = studentid[matchIndex]


            if counter==0:
                cvzone.putTextRect(ImgBack, "Loading", (275,400))
                cv2.imshow("Face Attendance", ImgBack)
                cv2.waitKey(1)
                counter = 1
                modType=1


            if counter!=0:

                if counter == 1:
                 # get the data
                 studentInfo = db.reference(f'Students/{id}').get()
                 print(studentInfo)
                 #get the image from storage
                 blob = bucket.get_blob(f'images/{id}.png')
                 array = np.frombuffer(blob.download_as_string(), np.uint8)
                 imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                 resized_img_student = cv2.resize(imgStudent, (220, 234))

                 # Update data of attendance
                 datetimeObj = datetime.strptime(studentInfo['last_attendance_time'],
                                              "%Y-%m-%d %H:%M:%S")
                 secondsElapsed = (datetime.now()-datetimeObj).total_seconds()
                 print(secondsElapsed)

                 if secondsElapsed > 30:
                     ref = db.reference(f'Students/{id}')
                     studentInfo['total_attendance'] += 1
                     ref.child('total_attendance').set(studentInfo['total_attendance'])
                     ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                 else:
                    modType = 3
                    counter = 0
                    ImgBack[44:44 + 748, 808:808 + 460] = imgmodeslist[modType]

            if modType != 3:
                if 10 < counter < 20:
                    modType = 2
                ImgBack[44:44 + 748, 808:808 + 460] = imgmodeslist[modType]

                if counter <= 10:
                    cv2.putText(ImgBack, str(studentInfo['total_attendance']), (862, 159),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (225,255,255), 1)
                    cv2.putText(ImgBack, str(studentInfo['name']), (900, 500),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,50), 1)
                    cv2.putText(ImgBack, str(studentInfo['major']), (1030, 615),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
                    cv2.putText(ImgBack, str(studentInfo['id']), (1016, 554),
                         cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(ImgBack, str(studentInfo['standing']), (910, 700),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    cv2.putText(ImgBack, str(studentInfo['year']), (1028, 700),
                         cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    cv2.putText(ImgBack, str(studentInfo['starting_year']), (1126, 700),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)


                    (w,h),_ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (410-w)//2
                    cv2.putText(ImgBack, str(studentInfo['name']), (900, 500),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    ImgBack[210:210+234, 923:923+220] = resized_img_student

            counter += 1

            if counter >= 20:
                counter = 0
                modType = 0
                studentInfo = []
                imgStudent = []
                ImgBack[44:44 + 748, 808:808 + 460] = imgmodeslist[modType]
        else:
             modType = 0
             counter = 0
      # cv2.imshow("Webcam", img)
        cv2.imshow("Face Attendance", ImgBack)
        cv2.waitKey(10)
