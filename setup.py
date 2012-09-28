#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 Liricus SRL <info@liricus.com.ar>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Fra


#===============================================================================
# DOCS
#===============================================================================

"""This file is for distribute yatel

"""


#===============================================================================
# IMPORTS
#===============================================================================

import os

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

import yatel

#===============================================================================
# QT VALIDATORS
#===============================================================================

try:
    from PyQt4 import QtGui
    from PyQt4 import QtCore
    from PyQt4 import Qsci
except ImportError:
    print "You need to install PyQt 4 and PyQt Qscintilla"
    sys.exit(1)
    

#===============================================================================
# CONSTANTS
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
    install_requires=yatel.__dependencies__,
)
