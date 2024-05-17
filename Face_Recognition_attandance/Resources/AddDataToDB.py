import firebase_admin 
from firebase_admin import credentials , db

cred = credentials.Certificate("Resources\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendance-51b81-default-rtdb.firebaseio.com/"
})


ref = db.reference('Students')

data = {
    "1234":
    {
        "Name": "Bill Gates",
        "Class": "TE",
        "Total Attendence": 5,
        "Division": "A"
    },
    "1235":
    {
        "Name": "Mr Bean",
        "Class": "BE",
        "Total Attendence": 8,
        "Division": "B"
    },
    "1236":
    {
        "Name": "Kevin Hart",
        "Class": "FE",
        "Total Attendence": 1,
        "Division": "C"
    }
    }



for key,value in data.items():
    ref.child(key).set(value)
