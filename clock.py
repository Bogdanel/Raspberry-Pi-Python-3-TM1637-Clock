#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
import time
import tm1637
import threading

class clock():
    def __init__(self):
        self.timer = None
        # Initialize the clock (GND, VCC=3.3V, Example Pins are DIO-20 and CLK21)
        self.display = tm1637.TM1637(CLK=23, DIO=18, brightness=1.0)

    def start(self):
        self.display.StartClock(military_time=True)
        doublepoint = True
        counter = 0
        while True:
            doublepoint = not doublepoint
            self.display.ShowDoublepoint(doublepoint)
            time.sleep(1)
    def stop(self):
        self.timer.cancel()
        self.display.Clear()

def main():
    try:
        cclock = clock()
        cclock.start()
    except (KeyboardInterrupt, SystemExit):
        cclock.stop()
        print ('\n! Received keyboard interrupt, quitting threads.\n')


if __name__ == '__main__':
    main()

