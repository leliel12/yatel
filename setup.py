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

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

import yatel


#===============================================================================
# CONSTANTS
#===============================================================================

PYPI_REQUIRE = [
    "peewee>=2.0",
    "pycante",
    "csvcool",
    "pyzmq",
    "ipython>=0.13",
    "pilas>=0.7",
]

MANUAL_REQUIRE = {
    "PyQt4" : "http://www.riverbankcomputing.co.uk/software/pyqt",
    "PyQt4.Qsci" : "http://www.riverbankcomputing.co.uk/software/qscintilla",
    "PyQt4.phonon" : "http://www.riverbankcomputing.co.uk/software/pyqt",
    "graph_tool" : "http://projects.skewed.de/graph-tool/",
    "box2d": "https://code.google.com/p/pybox2d/",
    "numpy": "http://numpy.scipy.org/",
}


#===============================================================================
# WARNINGS FOR MANUAL REQUIRES
#===============================================================================

not_found = []
for name, url in MANUAL_REQUIRE.items():
    try:
        __import__(name)
    except ImportError:
        not_found.append("{} requires '{}' ({})".format(yatel.PRJ,
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
    name=yatel.PRJ.lower(),
    version=yatel.STR_VERSION,
    description=yatel.SHORT_DESCRIPTION,
    author=yatel.AUTHOR,
    author_email=yatel.EMAIL,
    url=yatel.URL,
    download_url=yatel.DOWNLOAD_URL,
    license=yatel.LICENSE,
    keywords=yatel.KEYWORDS,
    classifiers=yatel.CLASSIFIERS,
    packages=[pkg for pkg in find_packages() if pkg.startswith("yatel")],
    include_package_data=True,
    package_data={'images': ['yatel/gui/resources/*'],
                  'uis': ['yatel/gui/uis/*']},
    py_modules=["ez_setup"],
    scripts=["yatelgui"],
    setup_requires=["sphinx-pypi-upload"],
    install_requires=PYPI_REQUIRE,
)
