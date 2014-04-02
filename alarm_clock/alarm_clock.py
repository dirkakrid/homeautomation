#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function

import time
import requests
import argparse
from mpd import MPDClient
import rxv

START_VOLUME = -80
MID_VOLUME = -48
TARGET_VOLUME = -38


def main():
    parser = argparse.ArgumentParser(description='wake up with music')
    parser.add_argument('--playlist',
        type=str, help='foo help', default="Alarm Clock")
    parser.add_argument('--sleep',
        type=str, help='foo help', default="90 min")
    args = parser.parse_args()


    r = rxv.RXV("192.168.1.116")
    r.on = True
    time.sleep(0.5)
    r.sleep = args.sleep
    r.input = "HDMI4"
    r.volume = START_VOLUME

    cli = MPDClient()
    cli.connect("dom.wuub.net", 6600)
    cli.clear()
    cli.load(args.playlist)
    cli.play()

    for vol in range(START_VOLUME, MID_VOLUME, 1):
        r.volume = vol
        time.sleep(0.5)

    time.sleep(30)
    requests.get("http://dom.wuub.net/api/lights/small/on")

    for vol in range(MID_VOLUME, TARGET_VOLUME, 1):
        r.volume = vol
        time.sleep(2)

    time.sleep(60)
    requests.get("http://dom.wuub.net/api/lights/large/on")



if __name__ == '__main__':
    main()
