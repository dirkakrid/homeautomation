#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function

import requests

from irapp import IrApp
app = IrApp(__name__)

@app.route("KEY_VOLUMEUP", remote="lights")
def key_1():
    requests.get("http://127.0.0.1/api/lights/small/on")

@app.route("KEY_VOLUMEDOWN", remote="lights")
def key_2():
    requests.get("http://127.0.0.1/api/lights/small/off")

@app.route("KEY_UP", remote="lights")
def key_LEFT():
    requests.get("http://127.0.0.1/api/lights/large/on")

@app.route("KEY_DOWN", remote="lights")
def key_UP():
    requests.get("http://127.0.0.1/api/lights/large/off")

if __name__ == '__main__':
    app.run()
