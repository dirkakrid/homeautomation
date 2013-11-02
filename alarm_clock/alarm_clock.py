#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function

import time
import argparse
from mpd import MPDClient
from mopidy_rxv import rxv473

def main():
    parser = argparse.ArgumentParser(description='wake up with music')
    parser.add_argument('--playlist',
        type=str, help='foo help', default="Alarm Clock")
    parser.add_argument('--sleep',
        type=str, help='foo help', default="90 min")
    args = parser.parse_args()


    r = rxv473.RXV473("192.168.1.116")
    r.on = True
    time.sleep(0.5)
    r.sleep = args.sleep
    r.input = "HDMI4"
    r.volume = -80

    cli = MPDClient()
    cli.connect("dom.wuub.net", 6600)
    cli.clear()
    cli.load(args.playlist)
    cli.play()

    for vol in range(-80, -35, 1):
        r.volume = vol
        time.sleep(0.5)


if __name__ == '__main__':
    main()
