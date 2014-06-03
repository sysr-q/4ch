"""fourch
======

.. _docs: https://4ch.readthedocs.org
.. _repo: https://github.com/plausibility/4ch

fourch (stylized as 4ch) is a wrapper to the 4chan JSON API, provided by moot. It allows you to interact with 4chan (in a READONLY way) easily through your scripts.

Originally <strike>stolen</strike> forked from `e000/py-4chan <https://github.com/e000/py-4chan>`_, but then I moved repos and renamed stuff since I'm pretty bad about that.

Requirements
------------

- Python 2.7 (what I test with, 2.x might work)
- requests

Notes
-----

- This isn't guaranteed to work all the time; after all, the API may change, and 4ch will have to be updated accordingly.
- If a feature is missing, open an issue on the `repo`_, and it may well be implemented.

Running / Usage
---------------

- Install & import: ``$ pip install 4ch``, ``import fourch``
- See the `docs`_

Contributing
------------
If you're interested in contributing to the usability of 4ch, or just want to give away stars, you can visit the 4ch github `repo`_.
"""
from setuptools import setup

if __name__ != "__main__":
    import sys
    sys.exit(1)

kw = {
    "name": "4ch",
    "version": "0.4.0",
    "description": "Python wrapper for the 4chan JSON API.",
    "long_description": __doc__,
    "url": "https://github.com/plausibility/4ch",
    "author": "plausibility",
    "author_email": "chris@gibsonsec.org",
    "license": "MIT",
    "packages": ['fourch'],
    "install_requires": ["requests"],
    "zip_safe": False,
    "keywords": "wrapper 4chan chan json",
    "classifiers": [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2"
    ]
}

if __name__ == "__main__":
    setup(**kw)
