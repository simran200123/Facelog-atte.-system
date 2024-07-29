import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancereal-81e44-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')
data = {
    "1234":
        {
            "name": "Elon Musk",
            "id":2353573,
            "major": "Artificial Intelligence",
            "starting_year": 2011,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
"1589":
        {
            "name": "Simran Saxena",
            "id":2346866,
            "major": "Robotics",
            "starting_year": 2021,
            "total_attendance": 8,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
"2345":
        {
            "name": "Steve Jobs",
            "id":435467,
            "major": "Economist",
            "starting_year": 2012,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
"67895":
        {
            "name": "Mukul Kandpal",
            "id":216580,
            "major": "Robotics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
"9568":
        {
            "name": "Riya Pal",
            "id":216134,
            "major": "computer science",
            "starting_year": 2021,
            "total_attendance": 4,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"

        },
"0000":
        {
            "name": "Virat Kholi",
            "id":216510,
            "major": "cricketer",
            "starting_year": 1999,
            "total_attendance": 20,
            "standing": "G",
            "year": 18,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
"6546":
        {
            "name": "Shweta Tiwari",
            "id": 2161291,
            "major": "computer science",
            "starting_year": 2021,
            "total_attendance": 2,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"

        },
"6745":
        {
            "name": "Rakshita Suyal",
            "id": 2161281,
            "major": "computer science",
            "starting_year": 2021,
            "total_attendance": 2,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"

        },







}

for key ,value in data.items():
    ref.child(key).set(value)