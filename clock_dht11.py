#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

import dht11
import time
import tm1637
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import requests
import threading

class clock():
    def __init__(self):
        self.lastRead = {
            "intern": {"humidity": 0, "temperature": 0},
            "extern": {"humidity": 0, "temperature": 0}
        }
        self.timer = None
        # Initialize the clock (GND, VCC=3.3V, Example Pins are DIO-20 and CLK21)
        self.display = tm1637.TM1637(CLK=23, DIO=18, brightness=0.1)
        # read data using pin 17
        self.sensor = dht11.DHT11(pin=17)

    def start(self):
        self.setTemperature()
        doublepoint = True
        counter = 0
        while True:
            doublepoint = not doublepoint
            self.display.ShowDoublepoint(doublepoint)
            counter += 1
            if counter == 10:
                self.showTemperature(True)
                time.sleep(1)
                self.showHumidity(True)
            elif counter == 20:
                counter = 0
                self.showTemperature(False)
                time.sleep(1)
                self.showHumidity(False)
            time.sleep(1)
            self.showClock()

    def log(self, message):
        print ('{time} ({unixtime}):  {msg}'.format(time=time.strftime('%d/%m/%Y %H:%M:%S'), unixtime=int(time.time()), msg=message))

    def updateExternaltemperature(self):
        try:
            url = 'http://localhost/api/weather/clock'
            resp = requests.get(url=url)
            response = resp.json()
            self.log(response)
            self.lastRead['extern'] = response
        except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
            self.log('External temperature request update failed')
            pass
    def updateInternaltemperature(self):
        result = self.sensor.read()
        if result.is_valid():
            self.lastRead['intern']['temperature'] = result.temperature
            self.lastRead['intern']['humidity'] = result.humidity
            self.putOnNode(result)
        else:
            time.sleep(5)
            self.updateInternaltemperature()
        self.log(self.lastRead['intern'])
    def putOnNode(self, result):
        try:
            url = 'http://localhost/api/weather/clock'
            data = {
                "temperature": result.temperature,
                "humidity": result.humidity
            }
            r = requests.post(url, json=data)
            response = r.json()
            self.log(response)
        except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
            self.log('Internal temperature request update failed')
            pass

    def setTemperature(self):
        self.updateInternaltemperature()
        self.updateExternaltemperature()
        # Timer has seconds as unit. // 5 minutes
        self.timer = threading.Timer(1 * 60 * 5, self.setTemperature, [])
        self.timer.start()

    def showHumidity(self, intern):
        self.display.ShowDoublepoint(not intern)
        location = 'intern' if intern == True else 'extern'
        h = self.lastRead[location]['humidity']
        digits = [0, 0, 0, 0]
        digits[0] = h // 10
        digits[1] = h % 10
        digits[2] = 36
        digits[3] = 17
        if h == 100:
            digits[0] = 1
            digits[1] = 0
            digits[2] = 0
            digits[3] = 17
        self.display.Show(digits)

    def showTemperature(self, intern):
        self.display.ShowDoublepoint(not intern)
        location = 'intern' if intern == True else 'extern'
        h = self.lastRead[location]['temperature']
        digits = [0, 0, 0, 0]
        if h >= 0:
            digits[0] = h // 10 if h // 10 else 36
            digits[1] = h % 10
            digits[2] = 38
            digits[3] = 12
        else:
            neg = abs(h)
            if neg > 9:
                digits[0] = 37
                digits[1] = neg // 10 if neg // 10 else 36
                digits[2] = neg % 10
                digits[3] = 12
            else:
                digits[0] = 37
                digits[1] = neg % 10
                digits[2] = 38
                digits[3] = 12

        self.display.Show(digits)
    def showClock(self):
        t = time.localtime()
        d0 = t.tm_hour // 10 if t.tm_hour // 10 else 36
        d1 = t.tm_hour % 10
        d2 = t.tm_min // 10
        d3 = t.tm_min % 10
        digits = [d0, d1, d2, d3]
        self.display.Show(digits)
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

