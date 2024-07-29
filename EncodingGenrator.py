import cv2
import face_recognition
import pickle
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancereal-81e44-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancereal-81e44.appspot.com"
})


# importing the stu images
folderModePath = 'images'
PathList = os.listdir(folderModePath)
print(PathList)

imglist = []
studentid =[]

for path in PathList:
   imglist.append(cv2.imread((os.path.join(folderModePath,path))))
   studentid. append(os.path.splitext(path)[0])
   fileName = f'{folderModePath}/{path}'
   bucket = storage.bucket()
   blob = bucket.blob(fileName)
   blob.upload_from_filename(fileName)



   print(studentid)
#print(imglist)
 #  print(path)
  # print(os.path.splitext(path))
  #print(len(imglist))

def findEncoding(imageslist):
   encodelist =[]
   for img in imageslist:
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      encode = face_recognition.face_encodings(img)[0]
      encodelist.append(encode)

   return encodelist

print("encoding started..")
encodeListKnown = findEncoding(imglist)
print(encodeListKnown)
encodeListKnownId = [encodeListKnown, studentid]
print("encoding complete")
file = open("Encoderfile.p", "wb")
pickle.dump(encodeListKnownId, file)
file.close()
print("file saved")
