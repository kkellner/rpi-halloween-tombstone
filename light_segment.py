#
# Handle a segment (part of) a NeoPixel light strand 
# A LightStrand is made up of 1 to many LightSegments
#
class LightSegment:

    def __init__(self, lightStrand, numOfSegmentPixels, lightPattern):
        
        self.lightStrand = lightStrand

        # Number of pixels in this segment
        self.numOfSegmentPixels = numOfSegmentPixels

        # This will be calculated when its added to a strand
        self.strandPixelOffset = 0

        # A pattern is what should be shown on the segment pixels
        # E.g., "fire"
        # This is likely going to be a LightPatern Object
        self.lightPattern = lightPattern
        lightPattern.lightSegment = self

    def update(self, updateTime):
        if self.lightPattern is None:
            raise ValueError('The LightSegment does not have a LightPattern assigned')
        self.lightPattern.update(updateTime)

    def setPixelColor(self, pixelSegmentIndex, pixelColor):
        self.lightStrand.setPixelColor(self.strandPixelOffset + pixelSegmentIndex, pixelColor)
