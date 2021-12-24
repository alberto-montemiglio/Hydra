import requests
import json

from get_location import get_user_location

api_key = "787b972fc776329c029ebd9490466feb"


def get_weather_data(list_of_weather_data, date):

    # declare response variable
    weather_data_response = []

    # Get the user's location
    lat, lon = get_user_location()
    url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=%s&lon=%s&dt=%s&appid=%s" % (
        lat, lon, date, api_key)

    response = requests.get(url)
    data = json.loads(response.text)

    # Select the required data from the response
    for item in list_of_weather_data:
        weather_data_response.append(data["current"][item])

    return weather_data_response
