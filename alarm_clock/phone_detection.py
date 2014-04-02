#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function

import re
import requests
import redis
import time

COOLDOWN = 600  #s
RE_MAC = r"([0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})"

def main():
    s = requests.session()
    sr = redis.StrictRedis()
    s.post(
        "http://192.168.1.1/goform/formLogin",
        data={'username': "admin", 'password': PASSWORD}
    )
    now = int(time.time())
    try:
        res = s.get("http://192.168.1.1/wlstatbl.asp")
        mac_addresses = re.findall(RE_MAC, res.content)
        print(mac_addresses)
        sr.delete(*sr.keys("mac|*"))
        for ma in mac_addresses:
            sr.setex("mac|" + ma, COOLDOWN, now)
    finally:
        s.post("http://192.168.1.1/goform/formLogout", data={'logout': 'Apply Change'})


if __name__ == '__main__':
    main()
