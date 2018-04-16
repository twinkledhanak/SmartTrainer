from firebase import firebase
from firebase_admin import db

########## USE THIS FILE ONLY WHEN PUTTING VALUES DYNAMICALLY
#### VALUES PUT THROUGH CONSOLE FOR EXERCISE

firebase = firebase.FirebaseApplication('https://smarttrainer-49e2a.firebaseio.com/',None)


#result1 = firebase.post('/Exercises',"Beginner")
#result2 = firebase.post('/Exercises',"Intermediate")
#result3 = firebase.post('/Exercises',"Advanced")

root = '/Exercises/Beginner/Tadasana/'
result = firebase.post(root + 'type',"side")
result = firebase.post(root + 'pair',"N-RH#RH-RL") # ride side is towards the screen
#result = firebase.post(root + 'measure',"20#20")
												   

#result = firebase.post(root,{"type":"Side-Facing"})
#result = firebase.post(root,{"Neck-Hand":"2.33"})
#result = firebase.post(root,{"Hand-Leg":"17.1"})

root = '/Exercises/Intermediate/Warrior pose/'
result = firebase.post(root + 'type',"front")
result = firebase.post(root + 'pair',"N-H#H-RL")
#result = firebase.post(root + 'measure',"20#20")

root = '/Exercises/Advanced/Tree/'
result = firebase.post(root + 'type',"front")
result = firebase.post(root + 'pair',"N-H#H-RL")
#result = firebase.post(root + 'measure',"20#20")



print(result)
