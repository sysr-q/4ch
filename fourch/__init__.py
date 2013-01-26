""" fourch (stylised as 4ch) is an easy-to-implement Python wrapper for
    4chan's JSON API, as provided by moot.

    It uses the documentation of the 4chan API located at: https://github.com/4chan/4chan-API
    
    This is based off of the API last updated Jan 4th, 2013.
"""
from ._version import __version__

from .fourch import *

from .thread import thread as thread
from .board import board as board
from .reply import reply as reply
