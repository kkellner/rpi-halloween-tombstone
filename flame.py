# LED Candle animation for microypthon on esp8266

# Copyright 2018 Fritscher
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Values for the Gaussian distribution are taken from Eric's comment on https://cpldcpu.wordpress.com/2016/01/05/reverse-engineering-a-real-candle/

# https://cpldcpu.wordpress.com/2016/01/05/reverse-engineering-a-real-candle/
# https://www.instructables.com/id/LED-Candle-for-Paper-Lanterns/


import time
import os
import math
import random
import logging
import threading
#import machine, neopixel

logger = logging.getLogger('flame')

# number of leds in the strip
LED_COUNT = 1
BRIGHTNESS = 1
# base color
r = 99 * BRIGHTNESS
g = 31 * BRIGHTNESS
b = 6 * BRIGHTNESS
# 150% brighter:
# r = 148
# g = 46
# b = 9
# 200% brighter:
#r = 198
#g = 62
#b = 12
SIDE_PIXEL_COLOR=(100,15,0,0)

np = None
flame_thread = None
flame_thread_stop = True

#np = neopixel.NeoPixel(machine.Pin(4), LED_COUNT)

#def show():
#   np.write()

class LED_light(object):

    def __init__(self, displayPixelOffset, displayPixelSize, displayFlamePixelOffset, displayFlamePixelSize):
        self.time = 0
        self.displayPixelOffset = displayPixelOffset
        self.displayPixelSize = displayPixelSize
        self.displayFlamePixelOffset = displayFlamePixelOffset
        self.displayFlamePixelSize = displayFlamePixelSize
        logger.info("displayPixelOffset: %d", displayPixelOffset)

    def Color(self, r, g, b):
        return (int(r), int(g), int(b))

    def setPixelColor(self, color):
        flamePos = self.displayPixelOffset+self.displayFlamePixelOffset

        # Set LEFT side pixels of display flame to solid color
        for i in range(self.displayPixelOffset, flamePos):
            np[i] = SIDE_PIXEL_COLOR

        # Set RIGHT side pixels of display flame to solid color
        for i in range(flamePos + self.displayFlamePixelSize, flamePos + self.displayFlamePixelSize + self.displayFlamePixelOffset):
            np[i] = SIDE_PIXEL_COLOR

        # Set the FLAME pixels
        for i in range(flamePos, flamePos+self.displayFlamePixelSize, 1):
            np[i] = color

    def randint(self, min, max):
        return random.randrange(min, max)
        #return min + int(int.from_bytes(os.urandom(2), 10) / 65536.0 * (max - min + 1))

    def c_brightness(self, c, brightness):
        return max(0, min(c * (brightness / 100), 255))

    def update(self, delta):
        self.time = self.time - delta
        if self.time <= 0:
            self.random_mode()
            self.random_duration()

    def set_brightness(self, brightness):
        self.setPixelColor(self.Color(self.c_brightness(r, brightness), self.c_brightness(g, brightness), self.c_brightness(b, brightness)))


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

class Flames(object):
    def __init__(self, pixels, displayCount, displayPixelSize, displayFlamePixelOffset, displayFlamePixelSize):
        global np
        np = pixels
        self.displayCount = displayCount
        self.displayPixelSize = displayPixelSize
        self.displayFlamePixelOffset = displayFlamePixelOffset
        self.displayFlamePixelSize = displayFlamePixelSize

    def startFlames(self):
        global flame_thread
        global flame_thread_stop
        if flame_thread is None:
            logger.info('flame thread start request')
            flame_thread = threading.Thread(target=self.flameThread)
            flame_thread.daemon = True
            flame_thread_stop = False
            flame_thread.start()


    def stopFlames(self):
        global flame_thread
        global flame_thread_stop
        if flame_thread is not None:
            logger.info('flame thread stop request')
            flame_thread_stop = True
            flame_thread.join()
            flame_thread = None
            logger.info('flame thread stopped')
    


    def flameThread(self):
        global flame_thread_stop
        candles = [
            LED_light(
                (i*self.displayPixelSize), 
                self.displayPixelSize,
                self.displayFlamePixelOffset,
                self.displayFlamePixelSize) for i in range(self.displayCount)
            ]
        #candles = [LED_light(i) for i in range(LED_COUNT)]
        while not flame_thread_stop:
            now = time.time() * 1000
            [l.update(now) for l in candles]
            np.show()
            self.wait_ms(50)

    def wait_ms(self, ms):
        time.sleep(ms/1000.0)

