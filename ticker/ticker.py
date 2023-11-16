"""
ABOUT:
    
    Ticker class and main program to run the LED matrix with several interactive
    widgets.
    See documentation at https://github.com/rcheeter/ticker.
    
LICENSE:
    
    Copyright 2023, Robert Heeter.
    See LICENSE (GNU General Public License, version 3).
    
"""

import pyledscape
import Adafruit_BBIO.GPIO as GPIO
from PIL import Image, ImageEnhance
from urllib import request

import os
import time

from widget import Widget
from clock_widget import ClockWidget
from weather_widget import WeatherWidget
from spotify_widget import SpotifyWidget

class Ticker():
    
    def __init__(self, widgets, matrix_pins, button_pins, weather_pins, brightness=6, refresh_rate=20, verbose=False):
        self.widgets = widgets # list of widget objects to cycle through
        self.matrix_pins = matrix_pins # list of LED matrix pins (see documentation)
        self.button_pins = button_pins # list of button pins (from left to right)
        self.weather_pins = weather_pins # list of I2C2 pins for AHT10 temperature/humidity sensor
        self.brightness = brightness # initial display brightness, from 0 to 6
        self.refresh_rate = refresh_rate # refresh rate of display in Hz, recommend 20 Hz max
        self.verbose = verbose # toggles printing information to terminal
        
    def setup(self):
        print("Ticker.setup()")
        
        self.image = None
        self.matrix = pyledscape.pyLEDscape() # instantiates LED matrix driver
        
        for pin in self.matrix_pins: # configure matrix pins to GPIO
            os.system(f"config-pin {pin} gpio")
            
        for pin in self.button_pins: # configure button pins to GPIO
            os.system(f"config-pin {pin} gpio")
            GPIO.setup(pin.replace("_0","_"), GPIO.IN)
            
        for pin in self.weather_pins: # configure AHT10 temperature/humidity sensor pins to I2C
            os.system(f"config-pin {pin} i2c")
        
        for widget in self.widgets: # set up each widget
            widget.setup()
        
        self.action_state = 0
        self.action_state_waiting = False
        self.action_state_times = [0, -1, -2]
        
        self.widget_index = 0
        print(f"Ticker.widget_index = {self.widget_index}")
        print(f"Ticker.brightness = {self.brightness}")
        
    def run(self):
        print("Ticker.run()")

        while True:
            self.update_widget_index() # checks widget cycling buttons
            widget = self.widgets[self.widget_index] # update current widget object
            
            self.update_action_state() # checks action button
            
            try:
                self.image = widget.update(action_state=self.action_state) # update current widget given action_state; returns image to display
            except Exception as e:
                print(f"ERROR: Ticker.run(): {e}")
                self.image.paste('red', (0, 0, self.width, self.height)) # error; red screen
                
            self.update_brightness() # update brightness of image to display
            
            self.update_display() # update display with image
            
    def update_brightness(self): # check brightness buttons and update brightness
        if self.button_pressed(self.button_pins[3]) and (self.brightness < 6):
            self.brightness += 1
            while self.button_pressed(self.button_pins[3]):
                time.sleep(1/self.refresh_rate)
            print(f"Ticker.brightness = {self.brightness}")
        
        elif self.button_pressed(self.button_pins[4]) and (self.brightness > 0):
            self.brightness -= 1
            while self.button_pressed(self.button_pins[4]):
                time.sleep(1/self.refresh_rate)
            print(f"Ticker.brightness = {self.brightness}")
                
        brightness_calibration = [0, 4, 3, 1, 5, 9, 10] # more appropriate brightness range based on LED matrix testing
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(brightness_calibration[self.brightness]/10)
        
    def update_widget_index(self): # check widget cycling buttons and update widget_index
        if self.button_pressed(self.button_pins[0]):
            if self.widget_index > 0:
                self.widget_index -= 1
            elif self.widget_index == 0:
                self.widget_index = len(widgets)-1
            while self.button_pressed(self.button_pins[0]):
                time.sleep(1/self.refresh_rate)
            print(f"Ticker.widget_index = {self.widget_index}")
            
        elif self.button_pressed(self.button_pins[2]):
            if self.widget_index < len(widgets)-1:
                self.widget_index += 1
            elif self.widget_index == len(widgets)-1:
                self.widget_index = 0
            while self.button_pressed(self.button_pins[2]):
                time.sleep(1/self.refresh_rate)
            print(f"Ticker.widget_index = {self.widget_index}")
            
    def update_action_state(self): # check action button and update action_state
        current_time = time.time()
        delay_time = 0.4 # delay before deciding final action_state
        
        if self.button_pressed(self.button_pins[1]):
            self.action_state_times.insert(0, current_time)
            self.action_state_times.pop()
            self.action_state_waiting = True
            while self.button_pressed(self.button_pins[1]):
                time.sleep(1/self.refresh_rate)
        
        if self.action_state_waiting == True:
            if self.action_state_times[0] - self.action_state_times[1] < delay_time:
                if self.action_state_times[1] - self.action_state_times[2] < delay_time:
                    if (current_time - self.action_state_times[0]) > delay_time:
                        self.action_state = 3
                        self.action_state_waiting = False
                        self.action_state_times = [0, -1, -2]
                        print(f"Ticker.action_state = {self.action_state}")
                else:
                    if (current_time - self.action_state_times[0]) > delay_time:
                        self.action_state = 2
                        self.action_state_waiting = False
                        self.action_state_times = [0, -1, -2]
                        print(f"Ticker.action_state = {self.action_state}")
            else:
                if (current_time - self.action_state_times[0]) > 2*delay_time:
                    self.action_state = 1
                    self.action_state_waiting = False
                    self.action_state_times = [0, -1, -2]
                    print(f"Ticker.action_state = {self.action_state}")
        else:
            self.action_state = 0
            if self.verbose == True:
                print(f"Ticker.action_state = {self.action_state}")

    def update_display(self): # update LED matrix
        try:
            self.matrix.draw(self.image)

        except Exception as e:
            raise Exception(f"ERROR: Ticker.update_display(): {e}")

    def button_pressed(self, pin): # generic function to check if button is pressed
        return GPIO.input(pin.replace("_0","_")) == GPIO.HIGH

"""
connected_internet
    checks if device is connected to the internet
    
    PARAMS:

    RETURNS:
    - True/False to indicate internet connectivity
"""
def connected_internet():
    try:
        request.urlopen("https://www.google.com", timeout=1)
        return True
    except request.URLError as err: 
        return False
        
if __name__ == '__main__':
    
    # wait until the device is connected to the internet
    while not connected_internet():
        time.sleep(1) # wait 1 second
    
    # widget instantiation
    widget_0 = Widget(refresh_rate=20, verbose=False)

    widget_1 = ClockWidget(timeshift=-6, unit='12', refresh_rate=20, verbose=False)
    
    widget_2 = WeatherWidget(unit='F', refresh_rate=20, verbose=False)
    
    SPOTIFY_CLIENT_ID = 'ADD CLIENT ID HERE'
    SPOTIFY_CLIENT_SECRET = 'ADD CLIENT SECRET HERE'
    SPOTIPY_REDIRECT_URI = 'ADD REDIRECT URI HERE'
    
    widget_3 = SpotifyWidget(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, refresh_rate=20, interval=1, verbose=False)

    # list of widget objects to cycle through
    widgets = [widget_0, widget_1, widget_2, widget_3]
    
    # list of PocketBeagle pins
    matrix_pins = ["P2_02","P2_04","P2_06","P2_03","P1_34","P1_20","P2_24","P2_33","P2_22","P2_18","P2_10","P2_08","P2_01"]
    button_pins = ["P1_02","P1_04","P1_06","P1_08","P1_10"]
    weather_pins = ["P1_26","P1_28"]
    
    # setup and run ticker LED matrix
    ticker = Ticker(widgets, matrix_pins, button_pins, weather_pins, brightness=6, refresh_rate=10, verbose=False)
    ticker.setup()
    ticker.run()
    
