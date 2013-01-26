from setuptools import setup

if __name__ != "__main__":
    import sys
    sys.exit(1)

def long_desc():
    with open('README.rst', 'rb') as f:
        return f.read()

execfile('fourch/_version.py')

kw = {
    "name": "4ch",
    "version": __version__,
    "description": "Python wrapper for the 4chan JSON API.",
    "long_description": long_desc(),
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
