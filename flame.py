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
# base color
# r = 99
# g = 31
# b = 6
# 150% brighter:
# r = 148
# g = 46
# b = 9
# 200% brighter:
r = 198
g = 62
b = 12


np = None
flame_thread = None
flame_thread_stop = True

#np = neopixel.NeoPixel(machine.Pin(4), LED_COUNT)

#def show():
#   np.write()

def Color(r, g, b):
    return (int(r), int(g), int(b))

def setPixelColor(i, color):
    #np[i] = color
    #for i in range(3, 5, 1):
    for i in range(2, 6, 1):
        np[i] = color

def wait(ms):
   time.sleep(ms/1000.0)

def randint(min, max):
    return random.randrange(min, max)
    #return min + int(int.from_bytes(os.urandom(2), 10) / 65536.0 * (max - min + 1))

def c_brightness(c, brightness):
    return max(0, min(c * (brightness / 100), 255))

class LED_light(object):
    def __init__(self, pos):
        self.time = 0
        self.pos = pos

    def update(self, delta):
        self.time = self.time - delta
        if self.time <= 0:
            self.random_mode()
            self.random_duration()

    def set_brightness(self, brightness):
        setPixelColor(self.pos, Color(c_brightness(r, brightness), c_brightness(g, brightness), c_brightness(b, brightness)))


    def random_mode(self):
        # Probability Random LED Brightness
        # 50% 77% –  80% (its barely noticeable)
        # 30% 80% – 100% (very noticeable, sim. air flicker)
        #  5% 50% –  80% (very noticeable, blown out flame)
        #  5% 40% –  50% (very noticeable, blown out flame)
        # 10% 30% –  40% (very noticeable, blown out flame)
        brightness = 0
        r = randint(0, 100)
        if r < 50:
            brightness = randint(77, 80)
        elif r < 80:
            brightness = randint(80, 100)
        elif r < 85:
            brightness = randint(50, 80)
        elif r < 90:
            brightness = randint(40, 50)
        elif r < 91:
            brightness = randint(120, 150)
            logger.info("bright")
        else:
            brightness = randint(30, 40)
        self.set_brightness(brightness)

    def random_duration(self):
        # Probability Random Time
        # 90% 20 ms
        #  3% 20 – 30 ms
        #  3% 10 – 20 ms
        #  4%  0 – 10 ms
        r = randint(0, 100)
        if r < 90:
            self.time = 20
        elif r < 93:
            self.time = randint(20, 30)
        elif r < 96:
            self.time = randint(10, 20)
        else:
            self.time = randint(0, 10)

# class Flame(object):
#     def __init__(self, np):
#         # TODO

def startFlame():
    global flame_thread
    global flame_thread_stop
    if flame_thread is None:
        logger.info('flame thread start request')
        flame_thread = threading.Thread(
            target=flameThread)
        flame_thread.daemon = True
        flame_thread_stop = False
        flame_thread.start()


def stopFlame():
    global flame_thread
    global flame_thread_stop
    if flame_thread is not None:
        logger.info('flame thread stop request')
        flame_thread_stop = True
        flame_thread.join()
        flame_thread = None
        logger.info('flame thread stopped')
 


def flameThread():
    global flame_thread_stop
    candles = [LED_light(i) for i in range(LED_COUNT)]
    while not flame_thread_stop:
        now = time.time() * 1000
        [l.update(now) for l in candles]
        np.show()
        wait(50)

