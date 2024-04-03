from pymongo import MongoClient
import time
from datetime import date, datetime
from gpiozero import LED, Button
from time import sleep

# Info for Mongo
password = "SensingIoT"
db_name = "gettingStarted"
collection_name = "alberto_montemiglio"
connection_string = "mongodb+srv://Al_1:%s@cluster0.frpdp.mongodb.net/%s?retryWrites=true&w=majority" % (password, db_name)

# Initialise the relay and the button
relay = LED(17)
button = Button(2)

button_state = False

# ISR for when the button is pressed
def button_pressed():
	(button_state+1)%2
	if button_state == True:
		if not water_intake_monitor:
			relay.on()
			sleep(10)
			relay.off()

# download mongo posts since midnight
def download_data(collection):
		response = {"ID": []}
		
		# Calculate the timestamp of midnight
		today = date.today()
		midnight = int(datetime.combine(today, datetime.min.time()).timestamp())

		for post in collection.find({"datetime": {"$lt": midnight}}):
			response["ID"].append(post["_id"])
			
		return response

# Calculates how much should I have drank so far in the day
def should_be_drank_by_now():
	ts = time.time()
	m = 2000 / 24*3600
	return int(m*ts)

# Calculates wheter I've drank enough
def water_intake_monitor():
	client = MongoClient(connection_string, tls=True,tlsAllowInvalidCertificates=True)
	db = client[db_name]
	collection = db[collection_name]
	water_swallows = download_data(collection)

	# calculate how many swallows since this morning
	swallows = len(water_swallows["ID"])
	if swallows < should_be_drank_by_now()/20:
		False
	else: 
		True

# ISR for when the button is pressed
def button_pressed():
	# change button state variable value
	(button_state+1)%2
	if button_state == True:
		
		# If I have not drank enough..
		if not water_intake_monitor:
			relay.on()
			sleep(10)
			relay.off()


# Call ISR when the button is pressed		
button.when_pressed = button_pressed()



	

