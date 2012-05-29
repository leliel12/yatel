#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.


#===============================================================================
# DOCS
#===============================================================================

"""This module contains all the global constants of the project

"""

#===============================================================================
# IMPORTS
#===============================================================================

import encodings
import os
import pkgutil
import sys


#===============================================================================
# CONSTANTS
#===============================================================================

#: This is the project name
PRJ = "Yatel"

#: The project version as tuple of strings
VERSION = ("0", "1")

#: The project version as string
STR_VERSION = ".".join(VERSION)

#: The project root path
PRJ_PATH = os.path.dirname(os.path.abspath(__file__))


#: The path to the puser home path
HOME_PATH = os.path.expanduser("~")


#: This is a folder where user put his data
YATEL_USER_PATH = os.path.join(HOME_PATH, ".yatel")
if not os.path.isdir(YATEL_USER_PATH):
    os.mkdir(YATEL_USER_PATH)


#: A Set containing all the encodings knowin by python
ENCODINGS = tuple(sorted(set(encodings.aliases.aliases.values())))


#: Determines the default encoding of the files (default utf-8)
DEFAULT_FILE_ENCODING = encodings.aliases.aliases.get(
    sys.getfilesystemencoding().lower().replace("-", ""),
    "utf_8"
)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
