# -*- coding: utf-8 -*-

import requests
import fourch


class listed_board:
    """ This object stores info about a board on 4chan.
        It is used by fourch.boards(), a function to
        get a list of all the boards and their properties.
    """

    def __init__(self, json):
        """ Initialize the board with the information it has.

            :param json: the json data for this post
            :type json: dict
        """
        self._json = json

    @property
    def board(self):
        """The board name, minus slashes. e.g., 'b', 'x', 'tv'"""
        return self._json['board']

    @property
    def title(self):
        """The title of the board, e.g., 'Random', 'Paranormal', 'Television & Film'"""
        return self._json['title']

    @property
    def ws(self):
        """Is the board worksafe?"""
        return bool(self._json['ws_board'])

    @property
    def pages(self):
        """How many pages does the board have?"""
        return self._json['pages']

    @property
    def per_page(self):
        """How many posts are there on 1 page?"""
        return self._json['per_page']


def boards(https=False):
    """ Get a list of all boards on 4chan, in :class:`fourch.boards.listed_board` objects
        containing information about the boards.

        :param https: Should we use HTTPS or HTTP?
        :type https: bool
    """
    s = requests.Session()
    s.headers.update({"User-Agent": "fourch/{0} (@https://github.com/plausibility/4ch)".format(fourch.__version__)})
    proto = "https://" if https else "http://"
    url = proto + fourch.urls['api'] + fourch.urls["api_boards"]
    r = s.get(url)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    boards = []
    for json_board in r.json()['boards']:
        boards.append(listed_board(json_board))
    return boards
