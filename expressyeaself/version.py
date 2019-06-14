# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 1
_version_micro = ''  # use '' for first of series, number for 1 and above
_version_extra = 'dev'
# _version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

# Description should be a one-liner:
description = "ExpressYeaself: A program to predict extent to which promoter \
                sequences have on the expression of genes in yeast."
# Long description will go up on the pypi page
long_description = """
ExpressYeaself
========
ExpressYeaself is an open source scientific software package that aims to
quickly and accurately predict the contribution a promoter sequence has on
the expression of genes in Saccharomyces cerevisiae (or 'Brewer's yeast ').

This will allow the costly and time-consuming trial-and-error processes in
the development and synthesis of biotherapeutics to be streamlined. Our goal
is to use machine learning and data mining to make recommendations on which
promoter sequences are likely to contribute to high levels of gene expression,
and which are not.
License
=======
``ExpressYeaself`` is licensed under the MIT license. See the "LICENSE" file for
information on the history of this software, terms & conditions for usage,
and a DISCLAIMER OF ALL WARRANTIES.
All trademarks referenced herein are property of their respective holders.
Copyright (c) 2018 -- Emissible (Joe Abbott, Keertana Krishnan, Guoyao Chen)
at the The University of Washington.
"""

NAME = "expressyeaself"
MAINTAINER = "Joe Abbott"
MAINTAINER_EMAIL = "jwa7@uw.edu"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/yeastpro/ExpressYeaself"
DOWNLOAD_URL = ""
LICENSE = "MIT"
AUTHOR = "Joe Abbott, Keertana Krishnan, Guoyao Chen"
AUTHOR_EMAIL = "jwa7@uw.edu, keertanakrish@gmail.com, guoyao@uw.edu"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGES = ["expressyeaself"]
PACKAGE_DATA = {}
REQUIRES = ["requirements.txt"]
