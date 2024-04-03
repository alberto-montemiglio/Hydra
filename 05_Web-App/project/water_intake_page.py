from pymongo import MongoClient
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show
from flask_login import login_required, current_user
import pandas


# Mongo data:

password = "SensingIoT"
db_name = "SensingIoT"
connection_string = "mongodb+srv://Al_1:%s@cluster0.frpdp.mongodb.net/%s?retryWrites=true&w=majority" % (password, db_name)

def download_data(collection):
		
		# Initialise response dict:

		response = {"ID": [], "datetime": [], "temp": [], "feels_like": [], "pressure": [], "humidity": []}


		# Build a dict out of the response:

		for post in collection.find():

			response["ID"].append(post["_id"])
			response["datetime"].append(post["datetime"])
			response["temp"].append(post["temp"])
			response["feels_like"].append(post["feels_like"])
			response["pressure"].append(post["pressure"])
			response["humidity"].append(post["humidity"])

		return response

def water_intake_page():

	# Create a connection to the online database of the current user

	client = MongoClient(connection_string, tls=True,tlsAllowInvalidCertificates=True)
	db = client[db_name]
	collection = db[str(current_user.name)]
	water_swallows = download_data(collection)
	
	
	# Binning of the data in 20 min bins

	df = pandas.DataFrame.from_dict(water_swallows)
	df['datetime'] = pandas.to_datetime(df['datetime'], unit='s')
	df['bin'] = (df['datetime'].dt.floor('20Min'))
	drank = df.groupby('bin')["ID"].count()
	a = df["bin"].drop_duplicates()
	

	# Order data:

	temp = [ele for ele, idx in sorted(enumerate(water_swallows['datetime']),
                                          key = lambda x : x[1])]
  
	water_swallows = {key : [val[idx] for idx in temp] for key, val in water_swallows.items()}
	water_swallows["datetime"] = pandas.to_datetime(water_swallows['datetime'], unit='s')
	water_swallows["pressure"] = [d/101.325 for d in water_swallows["pressure"]]
	water_swallows["humidity"] = [d/10 for d in water_swallows["humidity"]]


	# Create Plots:

	p = figure(title="Water Swallows, Temperature, Humidity and Presssure", x_axis_label='Time and Date', plot_height=600, x_axis_type = 'datetime', sizing_mode="stretch_width")

	p.step(x=water_swallows['datetime'], y=water_swallows['temp'], legend_label="Temperature", color="blue", line_width=2)
	p.step(x=water_swallows['datetime'], y=water_swallows['feels_like'], legend_label="Temperature - Feels Like", color="red", line_width=2)
	p.step(x=water_swallows['datetime'], y=water_swallows['pressure'], legend_label="Pressure", color="green", line_width=2)
	p.step(x=water_swallows['datetime'], y=water_swallows['humidity'], legend_label="Humidity", color="yellow", line_width=2)

	p.vbar(x = a, top = drank)

	p.legend.click_policy = "hide"


	# Return Plots:


	return p

