import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


SCOPE = 'user-read-playback-state user-modify-playback-state'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))


def play_playlist(playlist_uri):
    devices = sp.devices()
    if devices['devices']:
        device_id = devices['devices'][0]['id']  # Use the first available device
        sp.start_playback(context_uri=playlist_uri, device_id=device_id)
    else:
        print("No active device found.")

def pause_playback():
    sp.pause_playback()

def disconnect():
    sp.auth_manager.get_access_token(as_dict=False)



playlist_uri = 'spotify:playlist:0vvXsWCC9xrXsKd4FyS8kM'
play_playlist(playlist_uri)
timer = int(input('How long would you like to study? '))
time.sleep(timer)  
pause_playback()
disconnect()