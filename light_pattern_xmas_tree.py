#
# Handle a segment (part of) a NeoPixel light strand 
# A LightStrand is made up of 1 to many LightSegments
#

from light_pattern import LightPattern


class LightPatternXmasTree(LightPattern):


    def __init__(self):
        super().__init__() 


    def update(self, updateTime):

        # Turn off the first and last pixel (black)
        #self.lightSegment.setPixelColor(0, (0,0,0,0))
        #self.lightSegment.setPixelColor(self.lightSegment.numOfSegmentPixels-1, (0,0,0,0))

        for i in range(0, self.lightSegment.numOfSegmentPixels-1):
            self.lightSegment.setPixelColor(i, (0,255,0,0))

