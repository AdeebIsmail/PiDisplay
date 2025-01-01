import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time
import json
import requests

load_dotenv()
scope = "user-library-read user-read-playback-state user-read-recently-played"
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
))
prev_song_name = None


def musicData():
    global prev_song_name

    try:
        song_info = sp.current_playback(market='US')
        if song_info is None or song_info['item'] is None:
            return None

        song_name = song_info['item']['name']
        song_album_name = song_info['item']['album']['name']

        if not song_info['item']['album']['images']:
            return None
        song_art = song_info['item']['album']['images'][1]

        if not song_info['item']['artists']:
            return None
        song_artists = song_info['item']['artists']
        song_artists_list = []

        if prev_song_name == song_name:
            return None

        prev_song_name = song_name

        for artist in song_artists:
            song_artists_list.append(artist['name'])

        return [song_name, song_artists_list, song_album_name, song_art]

    except requests.exceptions.ReadTimeout:
        print("Request to Spotify API timed out.")
        time.sleep(60)
        return None
