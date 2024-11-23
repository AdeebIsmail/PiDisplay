import requests
import json
from datetime import datetime

# for prayer in prayers:
#     print(prayer, prayers[prayer])


def prayerData():
    url = "https://api.aladhan.com/v1/timingsByCity?"

    current_date = datetime.now()
    formatted_date = current_date.strftime("%d-%m-%Y")

    querystring = {
        "date": formatted_date,
        'city': 'College+Station',
        "country": "United+States+America"}

    response = requests.request("GET", url, params=querystring)
    data = response.json()
    prayers = data['data']['timings']
    return prayers
