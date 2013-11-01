#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function

import time
import atexit
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(15, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(18, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)
atexit.register(GPIO.cleanup)

from irapp import IrApp
app = IrApp(__name__)

def click(no):
    for _ in range(2):
        GPIO.output(no, 0)
        try:
            time.sleep(0.1)
        finally:
            GPIO.output(no, 1)
        time.sleep(0.2)


@app.route("KEY_VOLUMEUP", remote="lights")
def key_1():
    click(18)


@app.route("KEY_VOLUMEDOWN", remote="lights")
def key_2():
    click(22)


@app.route("KEY_UP", remote="lights")
def key_LEFT():
    click(11)


@app.route("KEY_DOWN", remote="lights")
def key_UP():
    click(15)

if __name__ == '__main__':
    app.run()
