import json
from urllib.request import urlopen

api_key = "buI3TU4DrJpV3GxOYoph"
url = "https://extreme-ip-lookup.com/json/?key=%s" % api_key


def get_user_location():
    response = urlopen(url)
    geo = json.load(response)

    return geo["lon"], geo["lat"]
