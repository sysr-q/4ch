# -*- coding: utf-8 -*-
from ._version import __version__

urls = {
    "api": "api.4chan.org",
    "boards": "boards.4chan.org",
    "images": "images.4chan.org",
    "thumbs": "0.thumbs.4chan.org",

    # These are tacked to the end of the api url after formatting.
    "api_board": "/{board}/{page}.json",
    "api_thread": "/{board}/res/{thread}.json"
}


class struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
