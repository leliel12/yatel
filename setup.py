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

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

import yatel


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
