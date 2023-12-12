import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from config import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI

# Scope determines the level of access your app will have
SCOPE = 'playlist-read-private user-library-read user-read-playback-state user-modify-playback-state'

# Set up Spotify API connection
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# Retrieve all playlists and their URIs
def get_playlists():
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        playlist_name = playlist['name']
        playlist_uri = playlist['uri']
        print(f"Playlist Name: {playlist_name}\nPlaylist URI: {playlist_uri}\n")

# Prompt the user to enter the name of the playlist
def get_playlist_uri_by_name():
    playlist_name_to_find = input("Enter the name of the playlist you would like to play: ")
    
    # Retrieve all playlists
    playlists = sp.current_user_playlists()

    # Search for the playlist with the specified name
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name_to_find:
            playlist_name = playlist['name']
            playlist_uri = playlist['uri']
            return playlist_uri
    
    print(f"Playlist not found '{playlist_name_to_find}' .")


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

# Example usage
get_playlists()
timer = float(input('How long would you like to study?(mins) '))
if isinstance(timer, float):
    playlist_uri = get_playlist_uri_by_name()
    play_playlist(playlist_uri)
    time.sleep(timer*60)  
    pause_playback()
    disconnect()

else: print('Please enter an integer!')
