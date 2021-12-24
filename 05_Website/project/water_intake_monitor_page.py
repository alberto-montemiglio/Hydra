from pymongo import MongoClient
from flask_login import current_user
import time
from datetime import date
from datetime import datetime

# Mongo data:

password = "SensingIoT"
db_name = "SensingIoT"
connection_string = "mongodb+srv://Al_1:%s@cluster0.frpdp.mongodb.net/%s?retryWrites=true&w=majority" % (password, db_name)


def download_data(collection):
		
		# Initialise response dict:

		response = {"ID": [], "datetime": [], "temp": [], "feels_like": [], "pressure": [], "humidity": []}
		
		# Get today's midnight:
		today = date.today()
		midnight = int(datetime.combine(today, datetime.min.time()).timestamp())


		
		# Get online database since midnight:

		for post in collection.find({"datetime": {"$lt": midnight}}):

			# Build a dict out of the response:

			response["ID"].append(post["_id"])
			response["datetime"].append(post["datetime"])
			response["temp"].append(post["temp"])
			response["feels_like"].append(post["feels_like"])
			response["pressure"].append(post["pressure"])
			response["humidity"].append(post["humidity"])

		return response



# Calculate water intake based on the user's weight and age

def water_intake(age, weight):
	
	if int(age) < 30: return int(int(weight)*0.6*65.2)
	elif int(age) < 54: return int(int(weight)*0.54*65.2)
	elif int(age) < 65: return int(int(weight)*0.46*65.2)
	else: return int(weight*0.38*65.2)



# Calculate how much should the uesr have drank so far in the day:

def should_be_drank_by_now():
	ts = time.time()
	m = (water_intake(current_user.age, current_user.weight)) / 24*3600
	return int(m*ts)



# Calculate % drank and if drank wnough so far in the day:

def water_intake_monitor_page(weight, height, age):
	
	client = MongoClient(connection_string, tls=True,tlsAllowInvalidCertificates=True)
	db = client[db_name]
	collection = db[str(current_user.name)]
	water_swallows = download_data(collection)

	swallows = len(water_swallows["ID"])
	if swallows < should_be_drank_by_now()/20:
		return swallows*20/water_intake(current_user.age, current_user.weight)*100, False
	else: 
		return swallows*20/water_intake(current_user.age, current_user.weight)*100, True
	
