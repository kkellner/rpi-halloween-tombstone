#
# Handle a segment (part of) a NeoPixel light strand 
# A LightStrand is made up of 1 to many LightSegments
#

from light_pattern import LightPattern
import logging

logger = logging.getLogger('pattern')

class LightPatternOff(LightPattern):


    def __init__(self):
        super().__init__() 

    def update(self, updateTime):

        for i in range(0, self.lightSegment.numOfSegmentPixels-1):
            self.lightSegment.setPixelColor(i, (0,0,0,0))
            #logger.info("set pixel to off: %d", i)


