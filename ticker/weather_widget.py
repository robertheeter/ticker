"""
ABOUT:
    
    WeatherWidget class to display the current temperature and humidity.
    Not intended to be run directly.
    
    Copyright 2023, ROBERT HEETER

"""

from PIL import Image, ImageDraw
import adafruit_ahtx0
import board
import busio

import time
from datetime import datetime

from widget import Widget

class WeatherWidget(Widget):
    
    def __init__(self, unit='C', refresh_rate=20, verbose=False):
        self.unit = unit # units for temperature, 'F' for Fahrenheit, 'C' for Celsius
        self.refresh_rate = refresh_rate # refresh rate of display
        self.verbose = verbose # toggles printing information to terminal

    def setup(self):
        print("WeatherWidget.setup()")
        
        self.width = Widget.width
        self.height = Widget.height
        self.image = Image.new('RGBX', (self.width, self.height), 'black') # black/blank screen
        self.previous_minute = -1
        
    def update(self, action_state):
        if self.verbose == True:
            print(f"WeatherWidget.update(action_state={int(action_state)})")
        
        time.sleep(1/self.refresh_rate)
        
        try:
            current_minute = datetime.now().strftime("%M")
            
            if current_minute != self.previous_minute: # update weather once per minute
                self.previous_minute = current_minute
                
                self.image.paste('black', (0, 0, self.width, self.height)) # clear screen
                
                i2c = busio.I2C(board.SCL_2, board.SDA_2) # connect to PocketBeagle I2C2 pins
                
                aht10 = adafruit_ahtx0.AHTx0(i2c) # get information from AHT10 sensor
                
                temperature = '{:.2f}°F'.format(aht10.temperature) # get temperature
                
                if self.unit == 'F': # change units of temperature and update string format
                    temperature = aht10.temperature*(9/5)+32
                    temperature = '{:.1f}°F'.format(temperature)
                elif self.unit == 'C':
                    temperature = aht10.temperature
                    temperature = '{:.1f}°C'.format(temperature)
                else:
                    raise Exception(f"ERROR: WeatherWidget.update(): unit must be 'F' or 'C'")
                    
                humidity = aht10.relative_humidity # get humidity
                humidity = '{:.0f}%'.format(humidity) # update string format

                text = [temperature, humidity]
                
                text_length, _ = max([(len(line), line) for line in text])
                text_length = text_length*8
                
                time_image = Image.new('RGBX', (text_length, 32), 'black')
                time_image_draw = ImageDraw.Draw(time_image)
                
                time_image_draw.text((0, 0), text[0], font=Widget.font8, fill='white') # add text of weather information
                time_image_draw.text((0, 9), text[1], font=Widget.font8, fill='white')
                
                self.image.paste(time_image, (2, 13))
                
                if self.verbose == True:
                    print(f"WeatherWidget.update.temperature = {temperature}")
                    print(f"WeatherWidget.update.humidity = {humidity}")
                
        except Exception as e:
            print(f"ERROR: WeatherWidget.update(): {e}")
            self.image.paste('red', (0, 0, self.width, self.height)) # error; red screen
            return self.image
            
        return self.image
