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
    TEST1 = 100
    TEST2 = 100
    TEST3 = 100


class Light:
    """Handle LED Light operations"""

    # Configure GPIO pins
    #motion_detect_pin = 17  # G17
    pixel_pin = board.D18

    # The number of NeoPixels
    num_pixels =  28

    display_auto_off_time_seconds = 5

    def __init__(self, basalt):
        self.basalt = basalt
        self.lightState = LightState.UNKNOWN

        # Docs: https://circuitpython.readthedocs.io/projects/neopixel/en/latest/api.html
        self.pixels = neopixel.NeoPixel(pin=Light.pixel_pin, n=Light.num_pixels,
                                        brightness=1.0, auto_write=False,
                                        pixel_order=neopixel.GRBW)

        # Configure motion detection
        #GPIO.setup(Light.motion_detect_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.add_event_detect(Light.motion_detect_pin, GPIO.BOTH, callback=self.motionHandler)


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
        self.pixels.fill((0, 0, 0, 0))
        self.pixels.show()

    def getLightState(self):
        return self.lightState

    def setLightState(self, lightState):
        self.lightState = lightState
        methodSuffix = lightState.name
        handlerMethodName = "_setLight_" + methodSuffix
        handlerMethod = getattr(self, handlerMethodName)
        result = handlerMethod()
        return result

    def _setLight_OFF(self):
        self.turnLightOff()

    def transision(self, fromColor, toColor, speed):
        # Todo
        self.turnLightOff()

    def _setLight_NIGHT_LIGHT(self):
        for i in range(16):
            self.pixels[i] = (0,0,0,0)
        for i in range(16, 26, 1):
            self.pixels[i] = (0,0,0,60)
        for i in range(26, Light.num_pixels, 1):
            self.pixels[i] = (0,0,0,0)
        self.pixels.show()

    def _setLight_TEST1(self):
        for i in range(16):
            self.pixels[i] = (0,0,0,0)
        for i in range(16, 26, 1):
            self.pixels[i] = (60,60,20,0)
        for i in range(26, Light.num_pixels, 1):
            self.pixels[i] = (0,0,0,0)
        self.pixels.show()

    def _setLight_RED(self):
        for i in range(16):
            self.pixels[i] = (0,0,0,0)
        for i in range(16, 26, 1):
            self.pixels[i] = (70,10,0,0)
        for i in range(26, Light.num_pixels, 1):
            self.pixels[i] = (0,0,0,0)
        self.pixels.show()

    def _setLight_LIGHTNING(self):
        for f in range(3):
            for i in range(16):
                self.pixels[i] = (0,0,0,0)
            for i in range(16, 26, 1):
                self.pixels[i] = (200,200,200,200)
            for i in range(26, Light.num_pixels, 1):
                self.pixels[i] = (0,0,0,0)
            self.pixels.show()
            time.sleep(0.100)
            self.pixels.fill((0, 0, 0, 0))
            self.pixels.show()
            time.sleep(0.150)


    def showStartup(self):
        self._STARTUP_Sequence()

    def _STARTUP_Sequence(self):
        self.pixels.fill((0, 0, 1, 0))
        self.pixels.show()
        time.sleep(1)
        self.pixels.fill((0, 0, 0, 0))
        self.pixels.show()

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

