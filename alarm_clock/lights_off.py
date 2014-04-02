#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function

import redis
import requests

REQUIRED_MACS = [
    "40:b0:fa:c6:f8",
    '20:64:32:60:f1',
]


def restore_state(sr):
    if sr.get("auto_off|large"):
        requests.post("http://dom.wuub.net/api/lights/large/on")
        sr.delete("auto_off|large")
    if sr.get("auto_off|small"):
        requests.post("http://dom.wuub.net/api/lights/small/on")
        sr.delete("auto_off|small")


def main():
    sr = redis.StrictRedis()

    for ma in REQUIRED_MACS:
        if sr.get("mac|" + ma):
            print("Active MAC: " + ma)
            restore_state(sr)
            return  # active mac

    if requests.get("http://dom.wuub.net/api/lights/large").json()['state'] == 'on':
        requests.post("http://dom.wuub.net/api/lights/large/off")
        sr.set('auto_off|large', True)
    if requests.get("http://dom.wuub.net/api/lights/small").json()['state'] == 'on':
        requests.post("http://dom.wuub.net/api/lights/small/off")
        sr.set('auto_off|small', True)


if __name__ == '__main__':
    main()
