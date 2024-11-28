import python_weather
import asyncio
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('WEATHER_KEY')


def getWeatherType():
    CITY = 'College Station'

    params = {
        'access_key': api_key,
        'query': CITY,
        'units': 'f'
    }

    try:
        response = requests.get(
            'http://api.weatherstack.com/current', params=params)
        response.raise_for_status()

        data = response.json()

        if 'current' not in data:
            print("Error: 'current' key not found in response")
            print("Response content:", data)
            return None

        temperature = data['current']['temperature']
        weather_condition = data['current']['weather_descriptions'][0]
        print(f"Temperature: {temperature}°F")
        print(f"Weather condition: {weather_condition}")
        return [temperature, CITY, weather_condition]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
