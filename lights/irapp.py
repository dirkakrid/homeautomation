#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function

import lirc
import tempfile
from collections import namedtuple

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
