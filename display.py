
from data.weatherdata import getWeatherType
from data.musicdata import musicData
from data.prayerdata import prayerData
from PIL import Image
from io import BytesIO
import schedule
import requests
import xml.etree.ElementTree as ET
import asyncio
import epd5in83_V2 as display
import cairosvg

namespaces = {'svg': 'http://www.w3.org/2000/svg'}


def drawToScreen():
    cairosvg.svg2png(url='updated_template.svg', write_to='output.png')
    image = Image.open('output.png')
    # try:
    #     display = display.EPD()
    #     display.init()

    #     # display the image
    #     display.display(display.getbuffer(image))

    # except IOError as e:
    #     print(e)

    # finally:
    #     display.sleep()


def drawWeather(weatherData):
    print("Drawing Weather...")
    print(weatherData)
    default_ns = 'http://www.w3.org/2000/svg'
    ET.register_namespace('', default_ns)
    tree = ET.parse('template.svg')
    root = tree.getroot()
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    element = root.find(f".//svg:*[@id='{'weather-temp'}']", namespaces)

    if element is not None:
        element.text = str(weatherData[0]) + "°F"
    element = root.find(f".//svg:*[@id='{'weather-location'}']", namespaces)
    if element is not None:
        location = weatherData[1].split(',')
        element.text = str(location[0])
    element = root.find(f".//svg:*[@id='{'weather-condition'}']", namespaces)
    if element is not None:
        element.text = str(weatherData[2])
    tree.write('updated_template.svg')
    drawToScreen()


def drawPrayer(prayerData):
    print("Drawing Prayer Times...")

    default_ns = 'http://www.w3.org/2000/svg'
    ET.register_namespace('', default_ns)
    tree = ET.parse('updated_template.svg')
    root = tree.getroot()
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}

    for prayer in prayerData.keys():
        element = root.find(f".//svg:*[@id='{prayer}']", namespaces)
        if element is not None:
            element.text = prayerData[prayer]
    tree.write('updated_template.svg')
    drawToScreen()


def drawMusic(music_data):
    print("Drawing Music...")
    url = music_data[-1]['url']

    default_ns = 'http://www.w3.org/2000/svg'
    ET.register_namespace('', default_ns)
    tree = ET.parse('updated_template.svg')
    root = tree.getroot()
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}

    response = requests.get(url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    bw_image = image.convert('1')

    resized_image = bw_image.resize((388, 300))  # Example size (300x300)
    resized_image.save("album_image.png", format='PNG')
    element = root.find(f".//svg:image[@id='{'album-art'}']", namespaces)

    if element is not None:
        element.set('href', 'album_image.png')

    song_name = root.find(".//svg:*[@id='song-name']", namespaces)

    if song_name is not None:
        song_name.text = music_data[0]
    artist_name = root.find(f".//svg:*[@id='{'artist-name'}']", namespaces)
    if artist_name is not None:
        if (len(music_data[1]) != 1):
            artist_string = ""
            for artist in music_data[1]:
                artist_string += (artist + ', ')
            artist_name.text = artist_string
        else:
            artist_name.text = music_data[1][0]
    album_name = root.find(f".//svg:*[@id='{'album-name'}']", namespaces)
    if album_name is not None:
        album_name.text = music_data[2]

    tree.write('updated_template.svg')
    drawToScreen()


def weatherJob():
    print("Running Weather Job...")
    weather_type = asyncio.run(getWeatherType())
    # weather_type = currentTemperature()
    drawWeather(weather_type)


def prayerJob():
    print("Running Prayer Job...")
    prayer_data = prayerData()
    drawPrayer(prayer_data)


def musicJob():
    print("Running Music Job...")
    music_data = musicData()
    if (music_data is not None):
        drawMusic(music_data)


schedule.every().day.at("06:00").do(prayerJob)
schedule.every().day.at("08:00").do(weatherJob)
schedule.every().day.at("12:00").do(weatherJob)
schedule.every().day.at("18:00").do(weatherJob)
schedule.every(3).minutes.do(musicJob)
# while True:
#     schedule.run_pending()
drawToScreen()
