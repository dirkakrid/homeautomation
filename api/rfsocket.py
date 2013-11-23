#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function

import time
import atexit
import hashlib
import RPi.GPIO as GPIO

class RFSocket(object):
    MASKS = [2**bit for bit in reversed(range(8))]

    KEYS = {
        "1": 0xAA,
        "2": 0xA9,
        "3": 0xA6,
        "G": 0xAA
    }

    ON = 0x96
    OFF = 0x95
    ALL_ON = 0x9A
    ALL_OFF = 0x99

    def __init__(self, pin, group_name=None, byte_prefix=None, retries=15):
        assert bool(byte_prefix) ^ bool(group_name), "Either byte_prefix or group name is required"
        if group_name:
            # automatically make 6 byte prefix from group name
            byte_prefix = [ord(ch) for ch in hashlib.sha1(group_name).digest()[:6]]

        assert len(byte_prefix) == 6, "byte_prefix must be 6 ints long"
        assert all(0 <= x <= 255 for x in byte_prefix), "byte_prefix must be bytes in 0..255 range"

        self._pin = pin
        self._byte_prefix = byte_prefix
        self._retries = retries


    def _boop(self, out=GPIO.output, sleep=time.sleep):
        pin = self._pin
        out(pin, 1)
        sleep(0.00015)
        out(pin, 0)

    def _rfsend(self, payload, sleep=time.sleep):
        boop = self._boop
        masks = self.MASKS

        boop()
        sleep(0.01)
        boop()
        sleep(0.0025)
        boop()
        for c in payload:
            for mask in masks:
                if bool(c & mask):
                    sleep(0.00090) # 0
                else:
                    sleep(0.00015) # 1
                boop()
        sleep(0.0001)

    def on(self, key):
        return self._state(key, self.ON if key != "G" else self.ALL_ON)

    def off(self, key):
        return self._state(key, self.OFF if key != "G" else self.ALL_OFF)

    def all_on(self):
        return self.on("G")

    def all_off(self):
        return self.off("G")


    def _state(self, key, state):
        skey = str(key).upper()
        payload = self._byte_prefix + [state, self.KEYS[skey]]
        for _ in xrange(self._retries):
            self._rfsend(payload)
        return state

def main():
    RF_PIN = 7
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RF_PIN, GPIO.OUT, initial=GPIO.LOW)
    atexit.register(GPIO.cleanup)
    s = RFSocket(RF_PIN, group_name="pokoj")  #byte_prefix=[0xaa, 0x5a, 0xa6, 0xaa, 0xaa, 0xa6])
    while True:
        inp = raw_input("send> ")
        key, _, what = inp.partition(' ')
        if bool(what):
            s.on(key.upper())
        else:
            s.off(key.upper())

if __name__ == '__main__':
    main()
