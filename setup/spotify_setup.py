"""
ABOUT:
    
    This script sets up access and permissions for Spotify's API using Spotipy and should be run on a Mac or Windows computer (i.e., via Visual Studio Code, NOT on the PocketBeagle Cloud9).
    See documentation at https://github.com/rcheeter/ticker for setting up this widget.
    
LICENSE:
    
    Copyright 2023, Robert Heeter.
    See LICENSE (GNU General Public License, version 3).
    
"""

# parameters
SPOTIFY_CLIENT_ID = 'ADD CLIENT ID HERE' # string of alphanumeric characters
SPOTIFY_CLIENT_SECRET = 'ADD CLIENT SECRET HERE' # string of alphanumeric characters
SPOTIPY_REDIRECT_URI = 'ADD REDIRECT URI HERE' # should likely be a https:// type address

# program
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

if os.path.exists(".cache"):
    os.remove(".cache") # delete any cached access tokens to generate a new access token
else:
    pass

scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))

# check access token
"""
To check if a provided access token (i.e., URL pasted into the computer terminal) works for the given scope above, the code below will print the currently playing track to the terminal without error assuming the computer is connected to the internet and a song is currently playing an internet-connected Spotify device.

Ignore this code if retrieving an access token for the PocketBeagle TICKER SpotifyWidget.
"""
currently_playing = sp.current_user_playing_track()
track_name = currently_playing['item']['name']
print(f"Currently listening to: {track_name}")
