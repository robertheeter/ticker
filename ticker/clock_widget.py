"""
ABOUT:
    
    ClockWidget class to display the current time and date.
    Not intended to be run directly.
    
    Copyright 2023, ROBERT HEETER

"""

from PIL import Image, ImageDraw

import time
from datetime import datetime, timedelta

from widget import Widget

class ClockWidget(Widget):
    
    def __init__(self, timeshift=0, unit='12', refresh_rate=20, verbose=False):
        self.timeshift = timeshift # time zone shift in hours from UTC (i.e., Houston is -6 hours)
        self.unit = unit # units for hours, '12' for 12-hour, '24' for 24-hour
        self.refresh_rate = refresh_rate # refresh rate of display
        self.verbose = verbose # toggles printing information to terminal

    def setup(self):
        print("ClockWidget.setup()")
        
        self.width = Widget.width
        self.height = Widget.height
        self.image = Image.new('RGBX', (self.width, self.height), 'black') # black/blank screen
        self.previous_second = -1
    
    def update(self, action_state):
        if self.verbose == True:
            print(f"ClockWidget.update(action_state={int(action_state)})")
        
        time.sleep(1/self.refresh_rate)
        
        try:
            current_second = datetime.now().strftime("%S")
            
            if current_second != self.previous_second: # update time/date once per second
                self.previous_second = current_second
                
                self.image.paste('black', (0, 0, self.width, self.height)) # clear screen
                
                current_datetime = datetime.now() + timedelta(hours=self.timeshift) # account for time zone shift
                
                if self.unit == '12': # change units for time and update string format
                    current_time = current_datetime.strftime("%I:%M")
                elif self.unit == '24':
                    current_time = current_datetime.strftime("%H:%M")
                else:
                    raise Exception(f"ERROR: ClockWidget.update(): unit must be '12' or '24'")
                    
                current_date = current_datetime.strftime("%b %d") # update string format

                text = [current_time, current_date]
                
                text_length = len(text[0])*12
    
                time_image = Image.new('RGBX', (text_length, 32), 'black')
                time_image_draw = ImageDraw.Draw(time_image)
                
                time_image_draw.text((0, 0), text[0], font=Widget.font12, fill='white') # add text of time/date information
                time_image_draw.text((0, 13), text[1], font=Widget.font8, fill='white')
                
                self.image.paste(time_image, (2, 9))
        
                if self.verbose == True:
                    print(f"ClockWidget.update.current_time = {current_time}")
                    print(f"ClockWidget.update.current_date = {current_date}")
                    
        except Exception as e:
            print(f"ERROR: ClockWidget.update(): {e}")
            self.image.paste('red', (0, 0, self.width, self.height)) # error; red screen
            return self.image
        
        return self.image
