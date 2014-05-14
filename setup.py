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

import sys, os

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

import yatel


#===============================================================================
# CONSTANTS
#===============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))

REQUIREMENTS_PATH = os.path.join(PATH, "requirements.txt")

with open(REQUIREMENTS_PATH) as fp:
    REQUIREMENTS =  fp.read().splitlines()


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
    py_modules=["ez_setup"],
    entry_points={'console_scripts': ['yatel = yatel.cli2:main']},
    install_requires=REQUIREMENTS,
)
