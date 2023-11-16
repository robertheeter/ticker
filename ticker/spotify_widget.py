"""
ABOUT:
    
    SpotifyWidget class to display the currently playing track, pause/play, and skip to the next or previous track.
    Not intended to be run directly.
        
LICENSE:
    
    Copyright 2023, Robert Heeter.
    See LICENSE (GNU General Public License, version 3).
    
"""

from PIL import Image, ImageDraw
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import requests
import time

from widget import Widget, add_image

class SpotifyWidget(Widget):
    
    def __init__(self, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, refresh_rate=20, interval=1, verbose=False):
        self.SPOTIFY_CLIENT_ID = SPOTIFY_CLIENT_ID # Spotify API client ID
        self.SPOTIFY_CLIENT_SECRET = SPOTIFY_CLIENT_SECRET # Spotify API client secret
        self.SPOTIPY_REDIRECT_URI = SPOTIPY_REDIRECT_URI # Spotify API redirect URI
        self.refresh_rate = refresh_rate # refresh rate of display
        self.interval = interval # interval pixel shift for text scrolling
        self.verbose = verbose # toggles printing information to terminal

    def setup(self):
        print("SpotifyWidget.setup()")
        
        self.width = Widget.width
        self.height = Widget.height
        self.image = Image.new('RGBX', (self.width, self.height), 'black') # black/blank screen

        self.currently_playing = 'currently_playing'
        self.prev_currently_playing = 'prev_currently_playing'
        self.index = 0
        
        scope='user-read-currently-playing user-read-playback-state user-modify-playback-state' # scope of Spotify permissions for Ticker application
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=self.SPOTIFY_CLIENT_ID, client_secret=self.SPOTIFY_CLIENT_SECRET, redirect_uri=self.SPOTIPY_REDIRECT_URI))
        
        self.is_playing = True
    
    def update(self, action_state):
        if self.verbose == True:
            print(f"SpotifyWidget.update(action_state={int(action_state)})")
        
        time.sleep(1/self.refresh_rate)

        # check action_state
        try:
            try:
                if action_state == 1: # pause/play track
                    if self.is_playing == False:
                        self.sp.start_playback()
                        self.is_playing = True
                    elif self.is_playing == True:
                        self.sp.pause_playback()
                        self.is_playing = False
            except:
                if action_state == 1: # if track is already paused/playing, play/pause track
                    if self.is_playing == False:
                        self.sp.pause_playback()
                        self.is_playing = False
                    elif self.is_playing == True:
                        self.sp.start_playback()
                        self.is_playing = True
                        
            if action_state == 2: # switch to next track
                self.sp.next_track()
                self.index = 0
                self.is_playing = True
                time.sleep(0.5)
                    
            elif action_state == 3: # switch to previous track
                self.sp.previous_track()
                self.index = 0
                self.is_playing = True
                time.sleep(0.5)
            
        except Exception as e:
            print(f"ERROR: SpotifyWidget.update(): {e}")
        
        # update currently playing track (album artwork, track information)
        try:
            if self.is_playing == True:
                if self.index == 0:
                    self.image.paste('black', (0, 0, self.width, self.height)) # clear screen
                
                    try:
                        self.currently_playing = self.sp.current_user_playing_track() # get currently playing track information
                        self.is_playing = self.currently_playing['is_playing']
                        self.song_name = self.currently_playing['item']['name']
                        artists = self.currently_playing['item']['artists']
                        self.artist_names = []
                        for artist in artists:
                            self.artist_names.append(artist['name'])
                        self.album_name = self.currently_playing['item']['album']['name']
                        self.image_url = self.currently_playing['item']['album']['images'][2]['url']
                        
                    except Exception as e:
                        print(f"ERROR: SpotifyWidget.update(): {e}")
                        self.image.paste('LimeGreen', (2, 2, 30, 30)) # failed to use API; green screen
                        self.index = 0
                        return self.image
                        
                    if self.currently_playing != self.prev_currently_playing:
                        self.prev_currently_playing = self.currently_playing
                        
                        image_file = requests.get(self.image_url, stream=True).raw # get album artwork data from web URL
                        image_size = (28, 28)
                        image_album = add_image(image_file, image_size) # add image
                        self.image.paste(image_album, (2, 2))
                
                text = [self.song_name, ', '.join(self.artist_names), self.album_name]
                window_size = (30, 32)
                text_track, reset_index = self.add_text_hscroll(text, window_size, self.index, self.interval) # add scrolling text of currently playing track information
                self.image.paste(text_track, (32, 0))
                
                if reset_index == True:
                    self.index = 0
                else:
                    self.index += 1
                    
                if self.verbose == True:
                    print(f"SpotifyWidget.song_name = {self.song_name}")
                    print(f"SpotifyWidget.artist_names = {self.artist_names}")
                    print(f"SpotifyWidget.album_name = {self.album_name}")
                    print(f"SpotifyWidget.index = {self.index}")
                    print(f"SpotifyWidget.is_playing = {self.is_playing}")
            
            else:
                try:
                    self.currently_playing = self.sp.current_user_playing_track() # get currently playing track information
                    self.is_playing = self.currently_playing['is_playing'] # check if song is currently playing
                    
                except Exception as e:
                    print(f"ERROR: SpotifyWidget.update(): {e}")
                    self.image.paste('LimeGreen', (2, 2, 30, 30)) # failed to use API; green screen
                    self.index = 0
                    return self.image
                    
        except Exception as e:
            print(f"ERROR: SpotifyWidget.update(): {e}")
            self.image.paste('red', (2, 2, 30, 30)) # error; red screen
            return self.image
        
        return self.image
    
    """
    add_text_hscroll
        assists with creating 3 lines of horizontal-scrolling text by iteratively cropping a text frame
        assumes height of 32 pixels and text formatting
        
        PARAMS:
        - text = list of 3 strings for each line of text
        - window_size = dimensions of sliding window of text in pixels
        - index = pixel index of current window location
        - interval = pixel shift between sequential windows of text
        
        RETURNS:
        - image_cropped = PIL Image object of current text window
        - reset_index = indicates when window reaches end of text and index must be reset
    """
    def add_text_hscroll(self, text, window_size=(32, 32), index=0, interval=1):
        text_length, _ = max([(len(line), line) for line in text])
        text_length = text_length*8 + (2*window_size[0])
    
        image = Image.new('RGBX', (text_length , window_size[1]), 'black')
        image_draw = ImageDraw.Draw(image)
        
        image_draw.text((window_size[0], 4), text[0], font=Widget.font_bold8, fill='white')
        image_draw.text((window_size[0], 13), text[1], font=Widget.font_bold8, fill='white')
        image_draw.text((window_size[0], 22), text[2], font=Widget.font_bold8, fill='white')
    
        image_cropped = image.crop((index*interval, 0, index*interval + window_size[0], window_size[1]))
        
        if index > (text_length - window_size[0])/interval:
            reset_index = True
        else:
            reset_index = False
        
        return image_cropped, reset_index
        