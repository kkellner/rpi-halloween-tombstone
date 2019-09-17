#
# Handle a full NeoPixel light strand (connected to a single pin of RPi)
# This class will contain any array of LightSegment objects
#

import neopixel
import threading
import logging
import time

logger = logging.getLogger('lightstrand')

class LightStrand:

    def __init__(self, strandPin, numberOfPixels):
        """
        Parameters
        ----------
        strandPin : int
            The pin used to talk with the NeoPixel strand
            e.g., board.D18
        numberOfPixels : int
            Number of NeoPixel in the strand
      
        """
        self.strandPin = strandPin
        self.numberOfPixels = numberOfPixels
        self.segments = []

        self.update_thread = None
        self.update_thread_stop = True

        # Docs: https://circuitpython.readthedocs.io/projects/neopixel/en/latest/api.html
        self.pixels = neopixel.NeoPixel(pin=strandPin, n=numberOfPixels,
                                        brightness=1.0, auto_write=False,
                                        pixel_order=neopixel.GRBW)

    def addSegment(self, segment):
        """
        Add a segment to the strand
        """

        # Calculate the total number of pixels used by currently added segments
        # so we can find the end offset.
        totalSegmentPixels = 0
        for seg in self.segments:
            totalSegmentPixels += seg.numOfSegmentPixels

        if totalSegmentPixels + segment.numOfSegmentPixels > self.numberOfPixels:
            raise ValueError('Trying to add segment with %d pixels, but no room in strand' % seg.numOfSegmentPixels)

        segment.strandPixelOffset = totalSegmentPixels
        self.segments.append(segment)

    def removeAllSegments(self):
        self.segments = []

    def update(self, updateTime):
        for seg in self.segments:
            seg.update(updateTime)
        self.pixels.show()

    def setPixelColor(self, pixelStrandIndex, pixelColor):
        self.pixels[pixelStrandIndex] = pixelColor


    def startUpdates(self):
        if self.update_thread is None:
            logger.info('update thread start request')
            self.update_thread_stop = False
            self.update_thread = threading.Thread(target=self.updateThread)
            self.update_thread.daemon = True
            self.update_thread.start()


    def stopUpdates(self):
        if self.update_thread is not None:
            logger.info('update thread stop request')
            self.update_thread_stop = True
            self.update_thread.join()
            self.update_thread = None
            logger.info('update thread stopped')
    

    def updateThread(self):
        while not self.update_thread_stop:
            now = time.time() * 1000

            for seg in self.segments:
                seg.update(now)

            self.pixels.show()
            self.wait_ms(50)

    def wait_ms(self, ms):
        time.sleep(ms/1000.0)
