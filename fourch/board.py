# -*- coding: utf-8 -*-

import requests
import fourch
from .thread import thread


class board(object):
    """ fourch.board is the master instance which allows easy access to the creation
        of thread objects.
    """

    def __init__(self, name, https=False, urls=None):
        """ Create the board instance, and initialize variables.

            :param name: The board name, minus slashes. e.g., 'b', 'x', 'tv'
            :param https: Should we use HTTPS or HTTP?
            :type https: bool
            :param urls: the url dictionary, with all the required url bases
            :type urls: dict or None
        """
        self.name = name
        self.https = https
        self._urls = urls or fourch.urls
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": "fourch/{0} (@https://github.com/plausibility/4ch)".format(fourch.__version__)})
        self._cache = {}  # id: fourch.thread, this stores prefetched threads

    @property
    def _base_url(self):
        """Create the base API url"""
        return self._proto + self._urls["api"]

    @property
    def _proto(self):
        """ Decide which HTTP protocol to use (HTTPS or HTTP) and return it, along with slashes.

            :return: the protocol to use
            :rtype: str
        """
        return "https://" if self.https else "http://"

    def catalog(self):
        """ Get a list of all the thread OPs and last replies.
        """
        url = self._base_url + self._urls["api_catalog"].format(board=self.name)
        r = self._session.get(url)
        return r.json()

    def threads(self):
        """ Get a list of all the threads alive, and which page they're on.

            You can cross-reference this with a threads number to see which page
            it's on at the time of calling.
        """
        url = self._base_url + self._urls["api_threads"].format(board=self.name)
        r = self._session.get(url)
        return r.json()

    def thread(self, res, update_cache=True):
        """ Create a :class:`fourch.thread` object.
            If the thread has already been fetched, return the cached thread.

            :param res: the thread number to fetch
            :type res: str or int
            :param update_cache: should we update if it's cached?
            :type update_cache: bool
            :return: the :class:`fourch.thread` object
            :rtype: :class:`fourch.thread` or None
        """
        if res in self._cache:
            t = self._cache[res]
            if update_cache:
                t.update()
            return t

        url = self._base_url + self._urls["api_thread"].format(board=self.name, thread=res)

        r = self._session.get(url)
        t = thread.from_req(self, res, r)
        if t is not None:
            self._cache[res] = t
        return t

    def page(self, page=1, update_each=False):
        """ Return all the threads in a single page.
            The page number is now one-indexed. The first page is 1, second is 2, etc.

            If a thread has already been cached, return the cache entry rather than making a new thread.

            :param page: page to pull threads from
            :type page: int
            :param update_each: should each thread be updated, to pull all replies
            :type update_each: bool
            :return: a list of :class:`fourch.thread` objects, corresponding to all threads on given page
            :rtype: list
        """
        url = self._base_url + self._urls["api_board"].format(board=self.name, page=page)
        r = self._session.get(url)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()

        json = r.json()
        threads = []

        for thj in json["threads"]:
            t = None
            res = thj["posts"][0]["no"]

            if res in self._cache:
                t = self._cache[res]
                t._should_update = True
            else:
                t = thread.from_json(self, thj, last_modified=r.headers["last-modified"])
                self._cache[res] = t

            if update_each:
                t.update()
            threads.append(t)

        return threads

    def thread_exists(self, res):
        """ Figure out whether or not a thread exists.
            This is as easy as checking if it 404s.

            :param res: the thread number to fetch
            :type res: str or int
            :return: whether or not the given thread exists
            :rtype: bool
        """
        url = self._base_url + self._urls["api_thread"].format(board=self.name, thread=res)
        return self._session.head(url).status_code == requests.codes.ok
