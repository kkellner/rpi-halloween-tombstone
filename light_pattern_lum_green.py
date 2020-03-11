#
# Handle a segment (part of) a NeoPixel light strand 
# A LightStrand is made up of 1 to many LightSegments
#

import math
import random

from light_pattern import LightPattern


SIDE_PIXEL_COLOR=(0,100,0,0)

# Luminary Flame
class LightPatternLumGreen(LightPattern):


    def __init__(self):
        super().__init__() 
        self.flamePixelSize = 16
  

    def Color(self, r, g, b):
        return (int(r), int(g), int(b))

    def update(self, updateTime):

        for i in range(0, self.flamePixelSize):
            self.lightSegment.setPixelColor(i, SIDE_PIXEL_COLOR)
