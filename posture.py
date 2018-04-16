# posture calculation
from firebase import firebase
from firebase_admin import db
import numpy as np


firebase = firebase.FirebaseApplication('https://smarttrainer-49e2a.firebaseio.com/',None)

# 1. get exercise details
# ON-CLICK OF SOME BUTTON SHOULD COME TO THIS FILE AND FETCH ALL DETAILS

#name = "tree"  #OBTAIN THIS NAME FROM INTENT COMING FROM THE CLICK

# returns ename, epair and emeasure
# measure , stored as a string values, but all measures are concatenated together
# so, 20#20 is an example of emeasure

def getExerciseDetails(name): # takes name of the exercise
	if name == "tadasana":
		# fetch details for tadasana
		root = '/Exercises/Beginner/Tadasana/'
		etype = firebase.get(root +'type/',None)
		epair = firebase.get(root +'pair/',None)
		emeasure = firebase.get(root + 'measure/',None)
		print("Type:::",etype)
		print("pairs::",epair)
		print("measure::",emeasure)

	elif name == "warrior":
		root = '/Exercises/Intermediate/Warrior Pose/'
		etype = firebase.get(root + 'type/',None)
		epair = firebase.get(root + 'pair/',None)
		emeasure = firebase.get(root + 'measure/',None)
		print("Type:::",etype)
		
		print("pairs::",epair)
		print("measure::",emeasure)

	elif name == "tree":
		root = '/Exercises/Advanced/Tree/'
		etype = firebase.get(root + 'type/',None)
		epair = firebase.get(root + 'pair/',None)
		emeasure = firebase.get(root + 'measure/',None)
		print("Type:::",etype)
		print("pairs::",epair)	
		print("measure::",emeasure)

	return etype,epair,emeasure

# returns list of bandNames
def getBandName(pair): # TAKING THE PAIR NAME AS THE INPUT
	
	result = pair.split('#')
	print(result)

	bodyParts = []
	bandName = []

	for i in range(len(result)):
		#print ("individual",result[i])

		string = result[i].split('-')
		for j in range(len(string)):
			#print("characters",string[j])
			bodyParts.append(string[j])

	for i in range(len(bodyParts)):
		
		

		if bodyParts[i] == "H": # hip
			bandName.append("G") # ASSUME WE HAVE GREEN FOR THE HIP TOO
		
		elif bodyParts[i] == "LH":
			bandName.append("B1")

		elif bodyParts[i] == "RH":
			bandName.append("B2")

		elif bodyParts[i] == "LL":
			bandName.append("G1")

		elif bodyParts[i] == "RL":
			bandName.append("G2")
						
		print("BodyPart: ",bodyParts[i])	
		print("Band Name:: ",bandName[i])			

	return bandName

# returns list of bandNames
def getMeasureDetails(measure): # TAKING THE PAIR NAME AS THE INPUT
	
	result = measure.split('#')
	print(result)
	#      20#20


	for i in range(len(result)):
		print ("individual",result[i])
	

	return result


# returns the angle calculated in degrees
def calculateSlope(ax,ay,bx,by): # coordinates needed, takes only 2 points at one time
	print("twinkle:",ax)
	print("kishor:",ay)
	print("manisha:",bx)
	print("dhanak:",by)
	if ax == bx:
		bx = bx + 1
	angle = 999 # cant be zero , because zero might turn out to be actual measure
	try:
		slope = (by-ay)/(bx-ax)
		angle = np.degrees(np.arctan(slope))
		print("angle in degrees is:",angle)
	except IndexError:
		angle = 999
		print("Sorry , angle could not be measured")	

	return angle	

#def compareMeasurements(emeasure,umeasure): # this has two measure strings, each with multiple values


