#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# DOCS
#===============================================================================

"""This package contains all the resources (icons, images and sounds) of the
project. Also has a function to simplify the access to this files bye his 
filename

"""

#===============================================================================
# IMPORTS
#===============================================================================

import os


#===============================================================================
# CONSTANTS
#===============================================================================

PATH = os.path.dirname(os.path.abspath(__file__))

#===============================================================================
# FUNCTIONS
#===============================================================================

def get(filename):
    """This function retur a full path to a given resource
    
    Example:
    
        >>> resources.get("filename.ext")
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
