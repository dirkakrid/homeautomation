#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function


import time
import atexit
import RPi.GPIO as GPIO

SMALL_ON = 18
SMALL_OFF = 22
LARGE_ON = 11
LARGE_OFF = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LARGE_ON, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(LARGE_OFF, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(SMALL_ON, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(SMALL_OFF, GPIO.OUT, initial=GPIO.HIGH)
atexit.register(GPIO.cleanup)

from flask import Flask, jsonify
app = Flask(__name__)

def click(no):
    for _ in range(2):
        GPIO.output(no, 0)
        try:
            time.sleep(0.1)
        finally:
            GPIO.output(no, 1)
        time.sleep(0.5)


LIGHTS = {
    'large': {'on': LARGE_ON, 'off': LARGE_OFF, 'state': 'unknown'},
    'small': {'on': SMALL_ON, 'off': SMALL_OFF, 'state': 'unknown'},
}

@app.route("/api/lights")
def lights_all():
    return jsonify(LIGHTS)

@app.route("/api/lights/<name>")
def lights_one(name):
    return jsonify(LIGHTS[name])

@app.route("/api/lights/<name>/<state>", methods=["GET", "POST"])
def lights_switch(name, state):
    click(LIGHTS[name][state])
    LIGHTS[name]['state'] = state
    return jsonify(LIGHTS[name])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
