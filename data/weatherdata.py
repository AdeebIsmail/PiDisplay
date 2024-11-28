import python_weather
import asyncio
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('WEATHER_KEY')


# async def getWeatherType():
#     async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
#         weather = await client.get('College Station')
#         temp = weather.temperature
#         location = weather.location + ", " + weather.region
#         kind = weather.kind
#         emoji = weather.kind.emoji
#         return [temp, location, str(kind), emoji]


def getWeatherType():
    CITY = 'College Station'

    params = {
        'access_key': api_key,
        'query': CITY,
        'units': 'f'
    }
    response = requests.get(
        'http://api.weatherstack.com/current', params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temperature']
        weather_condition = data['current']['weather_descriptions'][0]
        print(f"Temperature: {temperature}°C")
        print(f"Weather condition: {weather_condition}")
        return [temperature, CITY, weather_condition]
    else:
        print("Error fetching data:", response.status_code)
        return None
