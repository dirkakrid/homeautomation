#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mixer that controls volume using a Yamaha RXV-X73 amplifier."""
from __future__ import with_statement, division, absolute_import, print_function

import time
import logging

import pygst
pygst.require('0.10')
import gobject
import gst
from .rxv473 import RXV473

logger = logging.getLogger('mopidy_rxv')


class RXVMixer(gst.Element, gst.ImplementsInterface, gst.interfaces.Mixer):
    __gstdetails__ = (
        'RXVMixer',
        'Mixer',
        'Mixer to control Yamaha RXV-X73 amplifiers using http requests',
        'Mopidy')


    ip = gobject.property(type=str, default='192.168.1.116')
    source = gobject.property(type=str)
    min_volume = gobject.property(type=int, default=-80)
    max_volume = gobject.property(type=int, default=-5)
    volume_ttl = gobject.property(type=int, default=5)
    _volume_cache = (None, -1)
    _client = None

    def _public_to_ampli(self, public_volume):
        ampli_range = self.max_volume - self.min_volume
        public_relative = public_volume / 100.0
        ampli_volume = self.min_volume + ampli_range * public_relative
        return int(ampli_volume)

    def _ampli_to_public(self, ampli_volume):
        ampli_range = self.max_volume - self.min_volume
        base = ampli_volume - self.min_volume
        return int(base / ampli_range * 100.0)

    def cached_volume(self):
        now = time.time()
        cached, expire_at = self._volume_cache
        if expire_at > now:
            return cached
        new = self._client.volume
        self._volume_cache = (new, now + self.volume_ttl)
        return new

    @property
    def scaled_volume(self):
        ampli_vol = self.cached_volume()
        public_vol = self._ampli_to_public(ampli_vol)
        logger.debug("GET Volume: Public: %s Real: %s", public_vol, ampli_vol)
        return public_vol

    @scaled_volume.setter
    def scaled_volume(self, public_vol):
        scaled = self._public_to_ampli(public_vol)
        logger.debug("SET Volume: Public: %s Ampli: %s", public_vol, scaled)
        self._client.volume = scaled

    def list_tracks(self):
        track = create_track(
            label='Master',
            initial_volume=self.scaled_volume,
            min_volume=0,
            max_volume=100,
            num_channels=1,
            flags=(
                gst.interfaces.MIXER_TRACK_MASTER |
                gst.interfaces.MIXER_TRACK_OUTPUT))
        return [track]

    def get_volume(self, track):
        return [self.scaled_volume]

    def set_volume(self, track, volumes):
        if len(volumes):
            volume = int(volumes[0])
            self.scaled_volume = volume

    def set_mute(self, track, mute):
        logger.info("MUTE: not implemented yet")

    def do_change_state(self, transition):
        if transition == gst.STATE_CHANGE_NULL_TO_READY:
            logger.info("rxv")
            self._client = RXV473(self.ip)
                #return gst.STATE_CHANGE_FAILURE
        return gst.STATE_CHANGE_SUCCESS


def create_track(label, initial_volume, min_volume, max_volume,
                 num_channels, flags):

    class Track(gst.interfaces.MixerTrack):
        def __init__(self):
            super(Track, self).__init__()
            self.volumes = (initial_volume,) * self.num_channels

        @gobject.property
        def label(self):
            return label

        @gobject.property
        def min_volume(self):
            return min_volume

        @gobject.property
        def max_volume(self):
            return max_volume

        @gobject.property
        def num_channels(self):
            return num_channels

        @gobject.property
        def flags(self):
            return flags

    return Track()
