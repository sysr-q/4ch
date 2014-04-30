# -*- coding: utf-8 -*-
from ._version import __version__

urls = {
    "api": "a.4cdn.org",
    "boards": "boards.4chan.org",
    "images": "i.4cdn.org",
    "thumbs": "t.4cdn.org",

    # These are tacked to the end of the api url after formatting.
    "api_board": "/{board}/{page}.json",
    "api_thread": "/{board}/thread/{thread}.json",
    "api_threads": "/{board}/threads.json",
    "api_catalog": "/{board}/catalog.json"
}


class struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
