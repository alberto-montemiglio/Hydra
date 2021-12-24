import csv
from get_weather_data import get_weather_data
from pymongo import MongoClient
import os
import sys

password = "SensingIoT"
db_name = "gettingStarted"
collection_name = "people"

requested_data = ["pressure"]

dirname = os.path.dirname(__file__)

unuploaded_database_relative_path = "../database/unuploaded_database.csv"
uploaded_database_relative_path = "../database/uploaded_database.csv"
database_ID_counter_relative_path = "../database/database_ID_counter.csv"

unuploaded_database_path = os.path.join(
    dirname, unuploaded_database_relative_path)
uploaded_database_path = os.path.join(
    dirname, uploaded_database_relative_path)
database_ID_counter_path = os.path.join(
    dirname, database_ID_counter_relative_path)


connection_string = "mongodb+srv://Al_1:%s@cluster0.frpdp.mongodb.net/%s?retryWrites=true&w=majority" % (
    password, db_name)
try:
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]
except:
    print("no connection")
    sys.exit()
    # raise ConnectionError


def post_to_mongo(ID, requested_data, date):
    # post = {','.join(data for data in get_weather_data(requested_data))}

    # post = {','.join(':'))}
    try:
        post = dict(zip(requested_data, get_weather_data(requested_data, date)))
        post['ID'] = ID
        post['date'] = date
        print(post)
        post_id = collection.insert_one(post).inserted_id
        print(post_id)

    except:
        print("no connection")
        sys.exit()
        # raise ConnectionError


with open(unuploaded_database_path, 'r') as csvfile:
    csv_events = csvfile.readlines()
    csv_events = [event.strip("\n") for event in csv_events]

uploaded_events = []

for event_counter in range(len(csv_events)-1, -1, -1):

    swallow_event = csv_events[event_counter]

    with open(database_ID_counter_path, 'r') as ID_counter_file:
        ID = ID_counter_file.readlines()
        ID = [i.strip("\n") for i in ID]
        ID = int(ID[0])

    post_to_mongo(ID, requested_data, swallow_event)
    uploaded_events.append(swallow_event)

    del csv_events[event_counter]

    with open(unuploaded_database_path, 'w', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        for element in csv_events:
            csv_writer.writerow([element])

    with open(uploaded_database_path, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow([swallow_event])

    with open(database_ID_counter_path, 'w', newline='') as ID_counter_file:
        # Create a writer object from csv module
        ID_counter_file = csv.writer(ID_counter_file)
        ID_counter_file.writerow([ID+1])
# with open(uploaded_database_path, newline='') as csvfile:
#     for event in uploaded_events:
#         csvfile.write(event)


# with open(unuploaded_database_path, newline='') as csvfile:
#     for event in csv_events:
#         csvfile.write(event)
