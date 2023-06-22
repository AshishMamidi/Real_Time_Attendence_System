import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL' : "https://attendancesystemrtcv-default-rtdb.firebaseio.com/"
                              })
ref = db.reference('Students')
# register the students first manually in firebase
data = {
    "20BK1A6602":
        {
            "name" : "Mamidi Ashish Kumar",
            "major" : "Machine learning",
            "Starting_year" : 2020,
            "total_attendence" : 6,
            "standing" : "Good",
            "Year":3,
            "last_attendence_time" : "2023-04-16 11:24:50"
        },
"20BK1A6643":
        {
            "name" : "Murugula Preetham Rajnesh",
            "major" : "Machine learning",
            "Starting_year" : 2020,
            "total_attendence" : 3,
            "standing" : "Medium",
            "Year":3,
            "last_attendence_time" : "2023-04-16 10:24:50"
        }

}

for key,value in data.items():
    ref.child(key).set(value)