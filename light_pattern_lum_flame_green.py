#
# Handle a segment (part of) a NeoPixel light strand 
# A LightStrand is made up of 1 to many LightSegments
#

import math
import random

from light_pattern import LightPattern

BRIGHTNESS = 1
# base color
r = 6 * BRIGHTNESS
g = 99 * BRIGHTNESS
b = 31 * BRIGHTNESS
SIDE_PIXEL_COLOR=(15,100,0,0)

# Luminary Flame
class LightPatternLumFlameGreen(LightPattern):


    def __init__(self):
        super().__init__() 
        self.flamePixelSize = 16
        self.time = 0

    def Color(self, r, g, b):
        return (int(r), int(g), int(b))

    def setPixelColors(self, color):

        # Set the FLAME pixels
        # Odd = flame, even it fixed color
        for i in range(0, self.flamePixelSize):
            if i % 2 != 0: 
                self.lightSegment.setPixelColor(i,color)
            else:
                self.lightSegment.setPixelColor(i, SIDE_PIXEL_COLOR)



    def randint(self, min, max):
        return random.randrange(min, max)
        #return min + int(int.from_bytes(os.urandom(2), 10) / 65536.0 * (max - min + 1))

    def c_brightness(self, c, brightness):
        return max(0, min(c * (brightness / 100), 255))


    def update(self, updateTime):
        self.time = self.time - updateTime
        if self.time <= 0:
            self.random_mode()
            self.random_duration()

    def set_brightness(self, brightness):
        self.setPixelColors(self.Color(self.c_brightness(r, brightness), self.c_brightness(g, brightness), self.c_brightness(b, brightness)))


    def random_mode(self):
        # Probability Random LED Brightness
        # 50% 77% –  80% (its barely noticeable)
        # 30% 80% – 100% (very noticeable, sim. air flicker)
        #  5% 50% –  80% (very noticeable, blown out flame)
        #  5% 40% –  50% (very noticeable, blown out flame)
        # 10% 30% –  40% (very noticeable, blown out flame)
        brightness = 0
        r = self.randint(0, 100)
        if r < 50:
            brightness = self.randint(77, 80)
        elif r < 80:
            brightness = self.randint(80, 100)
        elif r < 85:
            brightness = self.randint(50, 80)
        elif r < 90:
            brightness = self.randint(40, 50)
        elif r < 91:
            brightness = self.randint(120, 150)
            #logger.info("bright")
        else:
            brightness = self.randint(30, 40)
        self.set_brightness(brightness)

    def random_duration(self):
        # Probability Random Time
        # 90% 20 ms
        #  3% 20 – 30 ms
        #  3% 10 – 20 ms
        #  4%  0 – 10 ms
        r = self.randint(0, 100)
        if r < 90:
            self.time = 20
        elif r < 93:
            self.time = self.randint(20, 30)
        elif r < 96:
            self.time = self.randint(10, 20)
        else:
            self.time = self.randint(0, 10)