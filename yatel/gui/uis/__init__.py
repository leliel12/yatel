#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice 
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.

#===============================================================================
# DOCS
#===============================================================================

"""Package containing all *QtDegigner* ``ui`` files.

"""


#===============================================================================
# IMPORTS
#===============================================================================

import os

import pycante


#===============================================================================
# CONSTANTS
#===============================================================================

#: Path of the uis folder
PATH = os.path.abspath(os.path.dirname(__file__))

#: Function to construct a class hierarchy from a *QtDesigner* ``ui`` files.
UI = pycante.EDir(PATH)


#===============================================================================
# MAIN
#===============================================================================
if __name__ == "__main__":
    print(__doc__)

