"""
ABOUT:
    
    Generic Widget class to display a white screen and supporting functions.
    Not intended to be run directly.
    See documentation at https://github.com/rcheeter/ticker for setting up this widget.
    
LICENSE:
    
    Copyright 2023, Robert Heeter.
    See LICENSE (GNU General Public License, version 3).
    
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance

import time

class Widget():
    
    # ticker LED matrix and graphics properties
    width = 64 # width of matrix
    height = 32 # height of matrix
    font8 = ImageFont.truetype("./fonts/dogica.ttf", 8) # 8-pixel font
    font_bold8 = ImageFont.truetype("./fonts/dogicabold.ttf", 8) # 8-pixel bold font
    font12 = ImageFont.truetype("./fonts/dogica.ttf", 12) # 12-pixel font
    font_bold12 = ImageFont.truetype("./fonts/dogicabold.ttf", 12) # 12-pixel bold font
    
    def __init__(self, refresh_rate=20, verbose=False):
        self.refresh_rate = refresh_rate # refresh rate of display
        self.verbose = verbose # toggles printing information to terminal
    
    def setup(self):
        print("Widget.setup()")
        
        self.width = Widget.width
        self.height = Widget.height
        self.image = Image.new('RGBX', (self.width, self.height), 'black') # black/blank screen

    def update(self, action_state):
        if self.verbose == True:
            print(f"Widget.update(action_state={int(action_state)})")
        
        time.sleep(1/self.refresh_rate)
        
        try:
            self.image = Image.new('RGBX', (self.width, self.height),'white') # white screen
            
        except Exception as e:
            print(f"ERROR: Widget.update(): {e}")
            self.image.paste('red', (0, 0, self.width, self.height))
            return self.image
            
        return self.image

"""
add_image
    converts, resizes, and enhances image file to PIL Image object
    
    PARAMS:
    - image_file = image data or file path
    - image_size = dimensions of resized image in pixels
    
    RETURNS:
    - image = PIL Image object with resized and enhanced image
"""
def add_image(image_file, image_size=(32, 32)):
    image = Image.open(image_file) # open image file
    image = image.resize(image_size, resample=Image.LANCZOS) # resize/resample image
    enhancer = ImageEnhance.Contrast(image) # enhance image contrast
    image = enhancer.enhance(1.2)
    
    return image
    
"""
add_text
    adds 3 lines of text to PIL Image object
    assumes height of 32 pixels and text formatting
    
    PARAMS:
    - text = list of 3 strings for each line of text

    RETURNS:
    - image = PIL Image object with text
"""
def add_text(text):
    text_length, _ = max([(len(line), line) for line in text])
    text_length = text_length*8
    
    image = Image.new('RGBX', (text_length, 32), 'black')
    image_draw = ImageDraw.Draw(image)
    
    image_draw.text((0, 4), text[0], font=Widget.font_bold8, fill='white') # add text
    image_draw.text((0, 13), text[1], font=Widget.font_bold8, fill='white')
    image_draw.text((0, 22), text[2], font=Widget.font_bold8, fill='white')
    
    return image
    
