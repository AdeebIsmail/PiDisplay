import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time
load_dotenv()
scope = "user-library-read user-read-playback-state user-read-recently-played"
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')


def musicData():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    ))

    song_info = sp.current_playback(market='US')
    if (song_info is None):
        return
    song_name = song_info['item']['name']
    song_album_name = song_info['item']['album']['name']
    song_art = song_info['item']['album']['images'][0]
    print(song_name)
    print(song_album_name)


while True:
    musicData()
    time.sleep(10)
