# Basalt project
#
# light.py - handle LED updates (NeoPixel) of basalt light
#

import logging
import time
import threading
import board
import RPi.GPIO as GPIO
import neopixel
from enum import Enum



from light_segment import LightSegment
from light_pattern_ghost import LightPatternGhost
from light_pattern_flame import LightPatternFlame
from light_pattern_startup import LightPatternStartup
from light_pattern_lightning import LightPatternLightning
from light_pattern_off import LightPatternOff
from light_pattern_full_on import LightPatternFullOn
from light_pattern_snowman import LightPatternSnowman
from light_pattern_xmas_tree import LightPatternXmasTree
from light_strand import LightStrand


logger = logging.getLogger('light')

class Color:
    RED = (255, 0, 0)
    YELLOW = (255, 200, 0)
    GREEN = (0, 255, 0)
    AQUA = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (255, 0, 255)
    BLACK = (0, 0, 0)

class LightState(Enum):
    UNKNOWN = 0
    STARTUP = 1
    SHUTDOWN = 2
    ERROR = 3
    OFF = 10
    NIGHT_LIGHT = 11
    LIGHTNING = 12
    RED = 13
    HALLOWEEN = 14
    FLAME = 15
    FULL_ON = 16
    XMAS = 17
    TEST1 = 100
    TEST2 = 100
    TEST3 = 100


class Light:
    """Handle LED Light operations"""

    # Configure GPIO pins
    #motion_detect_pin = 17  # G17
    pixel_pin = board.D18

    # The number of NeoPixels
    num_pixels = 144 

    display_auto_off_time_seconds = 5

    def __init__(self, basalt):
        self.basalt = basalt
        self.lightState = LightState.UNKNOWN
        self.lightStrand = LightStrand(Light.pixel_pin, Light.num_pixels)


    def shutdown(self):
        self.turnLightOff()

    def getUserLightStates(self): 
        response = {}
        for data in LightState:
            if data.value >= LightState.OFF.value:
                response[data.name] = data.value
        return response


    def turnLightOff(self):
        logger.info('In turnLightOff')
        #self.pixels.fill((0, 0, 0, 0))
        #self.pixels.show()
        self.lightStrand.removeAllSegments()
        self.lightStrand.addSegment(LightSegment(self.lightStrand, Light.num_pixels, LightPatternOff() ))
        self.lightStrand.update()


    def getLightState(self):
        return self.lightState

    def setLightState(self, lightState):
        self.lightState = lightState
        lightStateName = lightState.name

        # Determine the method name to call based on light state
        methodSuffix = lightState.name
        handlerMethodName = "_setLight_" + methodSuffix
        handlerMethod = getattr(self, handlerMethodName)
        result = handlerMethod()

        # Publish the new light state
        self.basalt.pubsub.publishLightState(lightStateName)

        return result

    def _setLight_OFF(self):
        self.stopLightAnimation()
        self.turnLightOff()

    def transision(self, fromColor, toColor, speed):
        # Todo
        self.turnLightOff()

    def _setLight_NIGHT_LIGHT(self):
        self.stopLightAnimation()
        for i in range(8):
            self.pixels[i] = (0,0,0,60)
        for i in range(8, 144, 1):
            self.pixels[i] = (0,0,0,60)
        self.pixels.show()

    def _setLight_TEST1(self):
        self.stopLightAnimation()
        for i in range(8):
            self.pixels[i] = (60,0,0,0)
        for i in range(8, 144, 1):
            self.pixels[i] = (0,60,0,0)
        self.pixels.show()

    def _setLight_RED(self):
        for i in range(8):
            self.pixels[i] = (100,0,0,0)
        for i in range(8, 16, 1):
            self.pixels[i] = (100,0,0,0)
        self.pixels.show()

    def _setLight_HALLOWEEN(self):
        strand = self.lightStrand
        strand.removeAllSegments()
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternGhost() ))
        #strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternFlame() ))
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternFlame() ))
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternGhost() ))
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternGhost() ))
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternFlame() ))
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternFlame() ))
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternFlame() ))
        self.lightStrand.startUpdates()


    def _setLight_XMAS(self):
        strand = self.lightStrand
        strand.removeAllSegments()
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternSnowman() )) # Snowman
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternXmasTree() )) # Tree
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternOff() ))   # Off
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternSnowman() )) # Snowman
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternOff() )) # Off
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternOff() )) # Off
        strand.addSegment(LightSegment(self.lightStrand, 8, LightPatternOff() )) # Off
        self.lightStrand.startUpdates()


    def _setLight_FLAME(self):
        self.stopLightAnimation()
        for i in range(8):
            self.pixels[i] = (100,20,0,0)
        for i in range(8, 16, 1):
            self.pixels[i] = (100,20,0,0)
        self.pixels.show()


    def _setLight_LIGHTNING(self):
        strand = self.lightStrand
        strand.removeAllSegments()
        strand.addSegment(LightSegment(self.lightStrand, Light.num_pixels, LightPatternLightning() ))
        self.lightStrand.startUpdates()


    def _setLight_FULL_ON(self):
        strand = self.lightStrand
        strand.removeAllSegments()
        strand.addSegment(LightSegment(self.lightStrand, Light.num_pixels, LightPatternFullOn() ))
        self.lightStrand.startUpdates()


    def stopLightAnimation(self):
        self.lightStrand.stopUpdates()


    def showStartup(self):
        self._STARTUP_Sequence()

    def _STARTUP_Sequence(self):
        strand = self.lightStrand

        strand.addSegment(LightSegment(self.lightStrand, Light.num_pixels, LightPatternStartup() ))
        self.lightStrand.update()
        time.sleep(1)
        strand.removeAllSegments()
        strand.addSegment(LightSegment(self.lightStrand, Light.num_pixels, LightPatternOff() ))
        self.lightStrand.update()
        strand.removeAllSegments()


    def _ERROR_Sequence(self):
        speed = 0.2
        self.pixels[0] = Color.RED
        self.pixels[1] = Color.BLACK
        self.pixels.show()
        time.sleep(speed)
        self.pixels[0] = Color.BLACK
        self.pixels[1] = Color.RED
        self.pixels.show()
        time.sleep(speed)

