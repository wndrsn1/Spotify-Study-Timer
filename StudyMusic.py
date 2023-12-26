import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from spotipy.oauth2 import SpotifyOAuth
import time
import spotipy
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


class SpotifyTimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Spotify Timer")

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                            client_secret=CLIENT_SECRET,
                                                            redirect_uri=REDIRECT_URI,
                                                            scope='playlist-read-private user-library-read user-read-playback-state user-modify-playback-state'))

        self.countdown_var = tk.StringVar()
        self.countdown_var.set("00:00")

        self.label = tk.Label(master, textvariable=self.countdown_var, font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.start_button = ttk.Button(master, text="Start Timer", command=self.start_timer)
        self.start_button.pack()


    def start_timer(self):
        timer_minutes = self.get_timer_input()
        if timer_minutes is not None:
            countdown_seconds = int(timer_minutes * 60)

            playlist_uri = self.get_playlist_input()
            if playlist_uri is not None:
                self.play_playlist(playlist_uri)

                while countdown_seconds >= 0:
                    minutes, seconds = divmod(countdown_seconds, 60)
                    time_str = f"{minutes:02}:{seconds:02}"
                    self.countdown_var.set(time_str)
                    self.master.update()
                    time.sleep(1)
                    countdown_seconds -= 1

                self.pause_playback()
                self.disconnect()


    def get_timer_input(self):
        return simpledialog.askfloat("Timer Input", "Enter study time in minutes:")

    
    def get_playlist_input(self):
        playlistlist = get_playlists()
        
        playlist_name_to_find = simpledialog.askstring("Playlist Input", f"{playlistlist}\n Enter the name of the playlist you would like to play:")
            # Retrieve all playlists
        playlists = sp.current_user_playlists()
        
        # Search for the playlist with the specified name
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name_to_find:
                playlist_name = playlist['name']
                playlist_uri = playlist['uri']
                return playlist_uri


    def play_playlist(self, playlist_uri):
        devices = self.sp.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            self.sp.start_playback(context_uri=playlist_uri, device_id=device_id)
        else:
            print("No active device found.")


    def pause_playback(self):
        self.sp.pause_playback()


    def disconnect(self):
        self.sp.auth_manager.get_access_token(as_dict=False)


def get_playlists():
    playlists = sp.current_user_playlists()
    playlist_full = ''
    for playlist in playlists['items']:
        playlist_name = playlist['name']
        playlist_uri = playlist['uri']
        playlist_full = playlist_full + f"{playlist_name}\n" 
    return playlist_full   


# Set up Spotify API connection
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='playlist-read-private user-library-read user-read-playback-state user-modify-playback-state'))

if __name__ == '__main__':
    root = tk.Tk()
    app = SpotifyTimerApp(root)
    root.mainloop()
