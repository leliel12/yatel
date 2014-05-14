#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This package contains all the html for render inside yatel.

"""

#===============================================================================
# IMPORTS
#===============================================================================

import os


#===============================================================================
# CONSTANTS
#===============================================================================

# : Path of the resource folder
PATH = os.path.dirname(os.path.abspath(__file__))


#===============================================================================
# FUNCTIONS
#===============================================================================

def get(filename):
    """This function retur a full path to a given resource

    Example:

        >>> html.get("filename.ext")
        "path/to/resources/filename.ext"

    """
    filepath = os.path.join(PATH, filename)
    if not os.path.isfile(filepath):
        raise IOError(2, 'No such file', filename)
    return filepath


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
