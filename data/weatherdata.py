import python_weather
import asyncio
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('WEATHER_KEY')


async def getWeatherType():
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get('College Station')
        temp = weather.temperature
        location = weather.location + ", " + weather.region
        kind = weather.kind
        emoji = weather.kind.emoji
        return [temp, location, str(kind), emoji]


# def currentTemperature():
#     url = "https://api.tomorrow.io/v4/weather/realtime?"

#     querystring = {
#         "location": "College Station",
#         'units': 'imperial',
#         "apikey": api_key}

#     response = requests.request("GET", url, params=querystring)
#     data = response.json()
#     # print(json.dumps(data, indent=4))
#     temperature = data['data']['values']['temperature']
#     # humidity = data.get['data']['values']['humidity']
#     # wind_speed = data.get['data']['values']['rainIntensity']
#     return temperature


# def upcomingForcast():
#     url = "https://api.tomorrow.io/v4/weather/forecast?"

#     querystring = {
#         "location": "College Station",
#         'units': 'imperial',
#         "apikey": api_key,
#         "daily": "1d"}

#     response = requests.request("GET", url, params=querystring)
#     data = response.json()
#     print(json.dumps(data, indent=4))
#     daily_data = data.get('timelines', {}).get('daily', [])
#     for day in daily_data:
#         time = day.get('time')
#         values = day.get('values', {})
#         temperature_avg = values.get('temperatureAvg')
#         humidity_avg = values.get('humidityAvg')
#         wind_speed_avg = values.get('windSpeedAvg')

#         print(f"Date: {time}")
#         print(f"Average Temperature: {temperature_avg}")
#         print(f"Average Humidity: {humidity_avg}")
#         print(f"Average Wind Speed: {wind_speed_avg}")
#         print("-" * 20)
