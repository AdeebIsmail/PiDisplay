import os
from dotenv import load_dotenv
import time
import pylast

load_dotenv()

api_key = os.getenv('FM_API_KEY') or ""
api_secret = os.getenv('FM_API_SECRET') or ""
username = os.getenv('FM_USERNAME') or ""
password_hash = pylast.md5(os.getenv("FM_PASSWORD") or "")

network = pylast.LastFMNetwork(
    api_key=api_key,
    api_secret=api_secret,
    username=username,
    password_hash=password_hash,
)

user = network.get_user(username)

prev_song_name = None


def musicData():
    global prev_song_name

    try:
        track = user.get_now_playing()

        if track is None:
            return None

        song_name = track.title
        song_artist = track.artist.name
        song_album = track.get_album()

        if prev_song_name == song_name:
            return None
        prev_song_name = song_name

        if song_album is not None:
            album_name = song_album.title
            album_art = song_album.get_cover_image()
            return [song_name, song_artist, album_name, album_art]

        return [song_name, song_artist, "", ""]

    except Exception as e:
        print(f"Request to LastFM API timed out.: {e}")
        time.sleep(60)
        return None
