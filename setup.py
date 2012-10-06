#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This file is for distribute yatel

"""


#===============================================================================
# IMPORTS
#===============================================================================

import os
import collections

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

import yatel


#===============================================================================
# CONSTANTS
#===============================================================================

PYPI_REQUIRE = [
    "peewee",
    "pycante",
    "csvcool",
    "pyzmq",
    "ipython",
    "Box2D",
    "pilas",
    "numpy"
]

MANUAL_REQUIRE = {
    "PyQt4" : "http://www.riverbankcomputing.co.uk/software/pyqt",
    "PyQt4.Qsci" : "http://www.riverbankcomputing.co.uk/software/qscintilla",
    "PyQt4.phonon" : "http://www.riverbankcomputing.co.uk/software/pyqt",
    "graph_tool" : "http://projects.skewed.de/graph-tool/",
}


#===============================================================================
# WARNINGS FOR MANUAL REQUIRES
#===============================================================================

not_found = []
for name, url in MANUAL_REQUIRE.items():
    try:
        __import__(name)
    except ImportError:
        not_found.append("{} requires '{}' ({})".format(yatel.__prj__,
                                                        name, url))

if not_found:
    limits = "=" * max(map(len, not_found))
    print "\nWARNING\n{}\n{}\n{}\n".format(limits,
                                            "\n".join(not_found),
                                            limits)


#===============================================================================
# FUNCTIONS
#===============================================================================

setup(
    name=yatel.__prj__,
    version=yatel.__str_version__,
    description=yatel.__short_description__,
    author=yatel.__author__,
    author_email=yatel.__email__,
    url=yatel.__url__,
    download_url=yatel.__download_url__,
    license=yatel.__license__,
    keywords=yatel.__keywords__,
    classifiers=yatel.__classifiers__,
    packages=[pkg for pkg in find_packages() if pkg.startswith("yatel")],
    include_package_data=True,
    package_data={'images': ['yatel/gui/resources/*'],
                  'uis': ['yatel/gui/uis/*']},
    py_modules=["ez_setup"],
    scripts=["yatelgui"],
    setup_requires=["sphinx-pypi-upload"],
    install_requires=PYPI_REQUIRE,
)
