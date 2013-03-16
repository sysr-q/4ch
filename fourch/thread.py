# -*- coding: utf-8 -*-

import requests
from .reply import reply


class thread(object):
    """ This object stores information about the given thread.
        It has a list of fourch.replies, as well as options to
        easily pull in updates (new posts), and create an instance
        with the json of a thread.
    """

    def __init__(self, board, res):
        """ Create the thread instance and initialize variables.

            :param board: the :class:`fourch.board` parent instance
            :type board: :class:`fourch.board`
            :param res: the given threads number
            :type res: str or int
        """
        self._board = board
        self.res = res
        self.alive = True  # has the thread died on us? 404 = True
        self.op = None
        self.replies = []
        self.omitted_posts = 0
        self.omitted_images = 0
        self._should_update = False  # If this is a precached thread, should it get updated?
        self._last_modified = None  # HTTP Last-Modified header for If-Modified-Since

    def __repr__(self):
        end = ""
        if self.omitted_posts or self.omitted_images:
            end = ", {0} omitted posts, {1} omitted images".format(self.omitted_posts, self.omitted_images)
        return "<{0}.{1} /{2}/{3}, {4} replies{5}>".format(
            self.__class__.__module__,
            self.__class__.__name__,
            self._board.name,
            self.res,
            len(self.replies),
            end
        )

    @staticmethod
    def from_req(board, res, r):
        """ Create a thread object from the given request.
            If the thread has 404d, this will return None,
            and if it isn't 200 OK, it will raise_for_status().
            Actually creates the thread by calling :func:`from_json`.

            :param board: the :class:`fourch.board` parent instance
            :type board: :class:`fourch.board`
            :param res: the given threads number
            :type res: str or int
            :param r: the requests object
            :type r: requests.models.Response
        """
        if r.status_code == requests.codes.not_found:
            return None
        elif r.status_code == requests.codes.ok:
            return thread.from_json(board, r.json(), res=res, last_modified=r.headers["last-modified"])
        else:
            r.raise_for_status()

    @staticmethod
    def from_json(board, json, res=None, last_modified=None):
        """ Create a thread object from the given JSON data.

            :param board: the :class:`fourch.board` parent instance
            :type board: :class:`fourch.board`
            :param json: the json data from the 4chan API
            :type board: dict
            :param res: the given threads number
            :type res: str or int
            :param last_modified: when was the page last modified
            :type last_modified: int or None
            :return: the created :class:`fourch.thread`
            :rtype: :class:`fourch.thread`
        """
        t = thread(board, res)
        t._last_modified = last_modified

        replies = json["posts"]

        t.op = reply(t, replies.pop(0))
        t.replies = [reply(t, r) for r in replies]

        if res is None:
            t._should_update = True
            t.res = t.op.number
            t.omitted_posts = t.op._json.get("omitted_posts", 0)
            t.omitted_images = t.op._json.get("omitted_images", 0)

        return t

    @property
    def sticky(self):
        """ Is this thread stuck?

            :return: whether or not the thread is stuck
            :rtype: bool
        """
        return self.op.sticky

    @property
    def closed(self):
        """ Is the thread closed?

            :return: whether or not the thread is closed
            :rtype: bool
        """
        return self.op.closed

    @property
    def last_reply(self):
        """ Return the last :class:`fourch.reply` to the thread, or the op
            if there are no replies.

            :return: the last :class:`fourch.reply` to the thread.
            :rtype: :class:`fourch.reply`
        """
        if not self.replies:
            return self.op
        return self.replies[-1]

    @property
    def images(self):
        """ Create a generator which yields all of the image urls for the thread.

            :return: a generator yieling all image urls
            :rtype: generator
        """
        yield self.op.file.url
        for r in self.replies:
            if not r.has_file:
                continue
            yield r.file.url

    def update(self, force=False):
        """ Update the thread, pulling in new replies,
            appending them to the reply pool.

            :param force: should replies be replaced with fresh reply objects
            :type force: bool
            :return: the number of new replies
            :rtype: int
        """
        if not self.alive and not force:
            return 0

        url = self._board._base_url + self._board._urls["api_thread"].format(board=self._board.name, thread=self.res)
        headers = None
        if self._last_modified:
            # If-Modified-Since, to not waste bandwidth.
            headers = {
                "If-Modified-Since": self._last_modified
            }

        r = self._board._session.get(url, headers=headers)

        if r.status_code == requests.codes.not_modified:
            # 304 Not Modified
            return 0

        elif r.status_code == requests.codes.not_found:
            # 404 Not Found
            self.alive = False
            # Remove from cache.
            self._board._cache.pop(self.res, None)
            return 0

        elif r.status_code == requests.codes.ok:
            if not self.alive:
                self.alive = True
                self._board._cache[self.res] = self

            self._should_update = False
            self.omitted_posts = 0
            self.omitted_images = 0

            self._last_modified = r.headers["last-modified"]
            replies = r.json()["posts"]

            post_count = len(self.replies)
            self.op = reply(self, replies.pop(0))
            if not force:
                self.replies.extend([reply(self, p) for p in replies if p["no"] > self.last_reply.number])
            else:
                self.replies = [reply(self, p) for p in replies]
            post_count_new = len(self.replies)
            post_count_diff = post_count_new - post_count
            if not post_count_diff:
                return 0
            return post_count_diff

        else:
            r.raise_for_status()
