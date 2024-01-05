from firebase import firebase
from firebase_admin import db


firebase = firebase.FirebaseApplication('https://smarttrainer-49e2a.firebaseio.com/',None)

result2 = firebase.post('/Exercises',"Intermediate")


