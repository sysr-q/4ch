# -*- coding: utf-8 -*-

import fourch
import base64
import re


class reply(object):
    """ This object stores information regarding a specific post
        on any given thread. It uses python properties to easily
        allow access to information.
    """

    def __init__(self, thread, json):
        """ Initialize the reply with the relevant information

            :param thread: the :class:`fourch.thread` parent instance
            :type thread: :class:`fourch.thread`
            :param json: the json data for this post
            :type json: dict
        """
        self._thread = thread
        self._json = json

    def __repr__(self):
        return "<{0}.{1} /{2}/{3}#{4}, image: {5}>".format(
            self.__class__.__module__,
            self.__class__.__name__,
            self._thread._board.name,
            self._thread.res,
            self.number,
            bool(self.has_file)
        )

    @property
    def is_op(self):
        """Is this post the OP (first post in thread)"""
        return self._json.get("resto", 1) == 0

    @property
    def number(self):
        """The number relating to this post"""
        return self._json.get("no", 0)

    @property
    def reply_to(self):
        """What post ID is this a reply to"""
        return self._json.get("resto", 0)

    @property
    def sticky(self):
        """Is this thread stuck?"""
        return bool(self._json.get("sticky", 0))

    @property
    def closed(self):
        """Is this thread closed?"""
        return bool(self._json.get("closed", 0))

    @property
    def now(self):
        """Humanized date string of post time"""
        return self._json.get("now", "")

    @property
    def timestamp(self):
        """The UNIX timestamp of post time"""
        return self._json.get("time", 0)

    @property
    def tripcode(self):
        """Trip code, if any, of the post"""
        return self._json.get("trip", "")

    @property
    def id(self):
        """Post ID, if any. (Admin, Mod, Developer, etc)"""
        return self._json.get("id", "")

    @property
    def capcode(self):
        """Post capcode, if any. (none, mod, admin, etc)"""
        return self._json.get("capcode", "")

    @property
    def country(self):
        """The country code this was posted from. Two characters, XX if unknown"""
        return self._json.get("country", "XX")

    @property
    def country_name(self):
        """The name of the country this was posted from"""
        return self._json.get("country_name", "")

    @property
    def email(self):
        """The email attached to the post"""
        return self._json.get("email", "")

    @property
    def subject(self):
        """The subject of the post"""
        return self._json.get("sub", "")

    @property
    def comment(self):
        """The comment, including escaped HTML"""
        return self._json.get("com", "")

    @property
    def comment_text(self):
        """ The stripped (mostly) plain text version of the comment.
            The comment goes through various regexes to become (mostly) clean.

            Some HTML will still be present, this is because Python's :mod:`HTMLParser` won't
            escape everything, and since it's undocumented, only god may know
            how to add more escapes.
        """
        import HTMLParser
        com = self.comment
        # <span class="quote">&gt;text!</span>
        # --- >text!
        com = re.sub("\<span[^>]+\>(?:&gt;|>)([^</]+)\<\/span\>", ">\\1", com, flags=re.I)
        # <a class="quotelink" href="XX#pYYYY">&gt;&gt;YYYY</a>
        # --- >>YYYY
        com = re.sub("\<a[^>]+\>(?:&gt;|>){2}(\d+)\<\/a\>", ">>\\1", com, flags=re.I)
        # Add (OP) to quotelinks to op
        com = re.sub("\>\>({0})".format(self._thread.op.number), ">>\\1 (OP)", com, flags=re.I)
        # <br> or <br /> to newline
        com = re.sub("\<br ?\/?\>", "\n", com, flags=re.I)
        # Send the remaining HTML through the HTMLParser to unescape.
        com = HTMLParser.HTMLParser().unescape(com)
        return com

    @property
    def url(self):
        """The URL of the post on the parent thread"""
        return "{0}{1}/{2}/res/{3}#p{4}".format(
            self._thread._board._proto,
            self._thread._board._urls["boards"],
            self._thread._board.name,
            self._thread.res,
            self.number
        )

    ## File related
    @property
    def has_file(self):
        """Whether or not this post has an image attached"""
        return "filename" in self._json

    @property
    def file(self):
        """ This holds the information regarding the image attached
            to a post, if there is one at all.

            It returns the relevant information in a class format,
            accessible via ``r.file.url``, for example.

            Information stored:

            - renamed
            - name
            - extension
            - size
            - md5
            - md5b64
            - width
            - height
            - thumb_width
            - thumb_height
            - deleted
            - spoiler
            - url
            - thumb_url

            :return: a struct with information related to image
        """
        if not self.has_file:
            return fourch.struct()
        f = {
            "renamed": self._json.get("tim", 0),
            "name": self._json.get("filename", ""),
            "extension": self._json.get("ext", ""),
            "size": self._json.get("fsize", 0),
            "md5": base64.b64decode(self._json.get("md5")),
            "md5b64": self._json.get("md5", ""),
            "width": self._json.get("w", 0),
            "height": self._json.get("h", 0),
            "thumb_width": self._json.get("tn_w", 0),
            "thumb_height": self._json.get("tn_h", 0),
            "deleted": bool(self._json.get("filedeleted", 0)),
            "spoiler": bool(self._json.get("spoiler", 0)),
            "url": "",
            "thumb_url": ""
        }
        f["url"] = "{0}{1}/{2}/{3}{4}".format(
            self._thread._board._proto,
            fourch.urls["images"],
            self._thread._board.name,
            f["renamed"],
            f["extension"]
        )
        f["thumb_url"] = "{0}{1}/{2}/{3}s.jpg".format(
            self._thread._board._proto,
            fourch.urls["thumbs"],
            self._thread._board.name,
            f["renamed"]
        )
        return fourch.struct(**f)
