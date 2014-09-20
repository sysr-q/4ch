# vim: sw=4 expandtab softtabstop=4 autoindent
""" fourch (stylised as 4ch) is an easy-to-implement Python wrapper for
    4chan's JSON API, as provided by moot.

    It uses the documentation of the 4chan API located at:
        https://github.com/4chan/4chan-API

    This is based off of the API last updated Aug 12, 2014.
    (4chan-API commit: 1b2bc7858afc555127b8911b4d760480769872a9)
"""
from ._version import __version__

from .fourch import *

from .thread import thread as thread
from .board import board as board
from .reply import reply as reply
from .boards import boards as boards
