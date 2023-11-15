"""
LICENSE:

    Copyright 2023, ROBERT HEETER

    Redistribution and use in source and binary forms, with or without 
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this 
    list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice, 
    this list of conditions and the following disclaimer in the documentation 
    and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its contributors 
    may be used to endorse or promote products derived from this software without 
    specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

ABOUT:
    
    This script sets up access and permissions for Spotify's API using Spotipy and
    should be run on a Mac or Windows computer (i.e., via VSCode, NOT on Cloud9 on
    the PocketBeagle).

INFORMATION:

    Install Spotipy: pip install spotipy --upgrade

    1. Enter the SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and
    SPOTIFY_REDIRECT_URI parameters below, found in the Spotify developer app
    client settings at developer.spotify.com/dashboard. These client tokens
    should NEVER be shared or published publicly.
    
    2. Connect to the internet and run this script on a Mac or Windows computer
    (i.e., via VSCode, NOT on Cloud9 on the PocketBeagle), which should open a
    webpage on the computer's default browser for user authorization for the app
    to access Spotify data and features. This process follows the OAuth 2.0
    authorization framework.

    3. The user should log in to their Spotify account and agree to the
    permissions. This will redirect the user to a blank page URL under the
    SPOTIFY_REDIRECT_URI. Copy the entire URL from the browser page and save it to
    be pasted into the PocketBeagle terminal. Do NOT paste the URL into the local
    computer terminal. This URL contains the access token required to run Spotipy
    and should NEVER be shared or published publicly.
    
    If the URL is pasted into the terminal, the access token will be saved in a
    .cache file in the current directory so the user does not need to repeatedly
    provide a new access token.

"""

# PARAMETERS
SPOTIFY_CLIENT_ID = 'ADD CLIENT ID HERE' # string of alphanumeric characters
SPOTIFY_CLIENT_SECRET = 'ADD CLIENT SECRET HERE' # string of alphanumeric characters
SPOTIPY_REDIRECT_URI = 'ADD REDIRECT URI HERE' # should likely be a https:// type address

# PROGRAM
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

if os.path.exists(".cache"):
    os.remove(".cache") # delete any cached access tokens to generate a new access token
else:
    pass

scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))

# CHECK ACCESS TOKEN
"""
To check if a provided access token (i.e., URL pasted into the computer terminal)
works for the given scope above, the code below will print the currently playing
track to the terminal without error assuming the computer is connected to the
internet and a song is currently playing an internet-connected Spotify device.

Ignore this code if retrieving an access token for the PocketBeagle.
"""
currently_playing = sp.current_user_playing_track()
track_name = currently_playing['item']['name']
print(f"Currently listening to: {track_name}")
