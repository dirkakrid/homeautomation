from __future__ import unicode_literals

import os

import pygst
pygst.require('0.10')
import gst
import gobject

from mopidy import config, ext


__version__ = '0.1.0'


class Extension(ext.Extension):

    dist_name = 'Mopidy-RXV'
    ext_name = 'rxv'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def register_gstreamer_elements(self):
        from .mixer import RXVMixer
        gobject.type_register(RXVMixer)
        gst.element_register(
            RXVMixer, 'rxv', gst.RANK_MARGINAL)
