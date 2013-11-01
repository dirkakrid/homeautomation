#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function

import lirc
import tempfile
from collections import namedtuple

import time
import atexit
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(15, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(18, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)
atexit.register(GPIO.cleanup)


Key = namedtuple("Key", "sequence remote endpoint")

class IrApp(object):
    def __init__(self, name):
        self._name = name
        self._routes = {}
        self._endpoints = {}

    def _generate_lircrc(self, f):
        for k in self._routes:
            f.write("begin\n")
            if k.remote:
                f.write("\tremote = {}\n".format(k.remote))
            for button in k.sequence.split():
                f.write("\tbutton = {}\n".format(button))
            f.write("\tprog = {}\n".format(self._name))
            f.write("\tconfig = {}\n".format(k.endpoint))
            f.write("end\n")
        f.flush()

    def run(self):
        with tempfile.NamedTemporaryFile() as f:
            self._generate_lircrc(f)
            lirc.init(self._name, f.name)
            while True:
                x = lirc.nextcode()
                if x:
                    self._endpoints[x[0]]()

    def route(self, sequence, remote=None):
        def wrap(fun):
            endpoint = "{}:{}".format(fun.__module__, fun.__name__)
            k = Key(
                sequence=sequence,
                remote=remote,
                endpoint=endpoint,
            )
            self._routes[k] = endpoint
            self._endpoints[endpoint] = fun
            return fun
        return wrap


app = IrApp(__name__)


def click(no):
    for _ in range(2):
        GPIO.output(no, 0)
        try:
            time.sleep(0.1)
        finally:
            GPIO.output(no, 1)
        time.sleep(0.2)

@app.route("KEY_1", remote="lights")
def key_1():
    click(18)

@app.route("KEY_2", remote="lights")
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
