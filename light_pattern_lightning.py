#
# Handle a segment (part of) a NeoPixel light strand 
# A LightStrand is made up of 1 to many LightSegments
#

from light_pattern import LightPattern

import logging

logger = logging.getLogger('LightPatternLightning')


class LightPatternLightning(LightPattern):


    def __init__(self):
        super().__init__()
        self.firstUpdate = 0
        self.lastUpdate = 0
        self.sequenceStart = 0
        self.sequenceCount = 0

    def update(self, updateTime):

        ON_COLOR = (200,200,200,200)
        OFF_COLOR = (0, 0, 0, 0)

        if self.firstUpdate == 0:
            self.firstUpdate = updateTime

        if self.sequenceStart == 0:
            self.sequenceStart = updateTime

        delta = updateTime - self.sequenceStart
        if delta > 160 and self.sequenceCount < 2:
            # Start sequence over
            self.sequenceStart = updateTime
            self.sequenceCount += 1
            delta = 0

        color = OFF_COLOR
        if delta <  100:
            color = ON_COLOR

        for i in range(0, self.lightSegment.numOfSegmentPixels):
            self.lightSegment.setPixelColor(i, color)


        # for f in range(3):
        #     for i in range(0, 16, 1):
        #         self.pixels[i] = (200,200,200,200)
        #     self.pixels.show()
        #     time.sleep(0.100)
        #     self.pixels.fill((0, 0, 0, 0))
        #     self.pixels.show()
        #     time.sleep(0.150)
