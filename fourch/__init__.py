# vim: sw=4 expandtab softtabstop=4 autoindent
""" fourch (stylised as 4ch) is an easy-to-implement Python wrapper for
    4chan's JSON API, as provided by moot.

    It uses the documentation of the 4chan API located at:
        https://github.com/4chan/4chan-API

    This is based off of the API last updated Aug 12, 2014.
    (4chan-API commit: 1b2bc7858afc555127b8911b4d760480769872a9)
"""
from ._version import __version__

from .fourch import urls

from .thread import Thread
from .board import Board
from .reply import Reply

import requests


def boards(https=False):
    """ Get a list of all boards on 4chan, in :class:`fourch.board.Board`
        objects.

        :param https: Should we use HTTPS or HTTP?
        :type https: bool
    """
    s = requests.Session()
    s.headers.update({
        "User-Agent": "fourch/{0} (@https://github.com/sysr-q/4ch)".format(
            __version__
        )
    })
    proto = "https://" if https else "http://"
    url = proto + urls['api'] + urls["api_boards"]
    r = s.get(url)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    boards = []
    for json_board in r.json()['boards']:
        boards.append(Board(json_board['board'], https=https))
    return boards
