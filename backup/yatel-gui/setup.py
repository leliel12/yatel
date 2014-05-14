#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This file is for distribute yatel with distutils

"""


#===============================================================================
# IMPORTS
#===============================================================================

import sys

try:
    import PyQt4
except ImportError:
    sys.stderr.write("PyQt4 not found: \n")
    sys.exit(1)

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

import yatel_gui


#===============================================================================
# CONSTANTS
#===============================================================================

PYPI_REQUIRE = [
    "yatel",
    "caipyrinha",
    "Pygments",
    "ipython",
    "pyZMQ",
]


#===============================================================================
# FUNCTIONS
#===============================================================================

setup(
    name=yatel_gui.PRJ.lower(),
    version=yatel_gui.STR_VERSION,
    description=yatel_gui.SHORT_DESCRIPTION,
    author=yatel_gui.AUTHOR,
    author_email=yatel_gui.EMAIL,
    url=yatel_gui.URL,
    download_url=yatel_gui.DOWNLOAD_URL,
    license=yatel_gui.LICENSE,
    keywords=yatel_gui.KEYWORDS,
    classifiers=yatel_gui.CLASSIFIERS,
    packages=[pkg for pkg in find_packages() if pkg.startswith("yatel_gui")],
    include_package_data=True,
    py_modules=["ez_setup"],
    install_requires=PYPI_REQUIRE,
)
