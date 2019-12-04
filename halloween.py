#!/usr/bin/python3
# Halloween tombstone lights
#
# xxxxxxxxxxxxxx


# interrupt-based GPIO example using LEDs and pushbuttons

import RPi.GPIO as GPIO
import time
import threading
import time
import board
import logging, logging.handlers 
import signal
import sys
import os

from pubsub import Pubsub
from light import Light
from http_request import HttpServer
from rpi_info import RpiInfo


logger = logging.getLogger('halloween')


class Halloween:
    """Handle Halloween display operations"""

    def __init__(self):
        self.pubsub = None
        self.server = None
        self.light = None
        self.rpi_info = None

        # Docs: https://docs.python.org/3/library/logging.html
        # Docs on config: https://docs.python.org/3/library/logging.config.html
        FORMAT = '%(asctime)-15s %(threadName)-10s %(levelname)6s %(message)s'
        logging.basicConfig(level=logging.NOTSET, format=FORMAT)
  
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        GPIO.setwarnings(True)

    def __setup_logger(self, logger_name, log_file, level=logging.INFO):
        l = logging.getLogger(logger_name)
        FORMAT = '%(asctime)-15s %(message)s'
        formatter = logging.Formatter(FORMAT)
        # Docs: https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler
        fileHandler = logging.handlers.RotatingFileHandler(log_file, mode='a',
                                                           maxBytes=1000000, backupCount=2)
        fileHandler.setFormatter(formatter)
        l.setLevel(level)
        l.addHandler(fileHandler)
        l.propagate = False
  
    def signal_handler(self, signal, frame):
        logger.info('Shutdown...')
        if self.server is not None:
            self.server.shutdown()
        if self.light is not None:
            self.light.shutdown()
        if self.pubsub is not None:
            self.pubsub.shutdown()
        GPIO.cleanup()
        sys.tracebacklimit = 0
        sys.exit(0)

    def startup(self):
        logger.info('Startup...')

        self.light = Light(self)
        self.light.showStartup()
        self.pubsub = Pubsub(self)
        self.rpi_info = RpiInfo(self)
 
        self.server = HttpServer(self)
        # the following is a blocking call
        self.server.run()


def main():
    """
    The main function
    :return:
    """
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

    # f = open("/proc/net/wireless", "rt")
    # data = f.read()
    # link = int(data[177:179])
    # level = int(data[182:185])
    # noise = int(data[187:192])
    # print("Link:{} Level:{} Noise:{}".format(link, level, noise))

    halloween = Halloween()
    halloween.startup()


if __name__ == '__main__':
    main()
