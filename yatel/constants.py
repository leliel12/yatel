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
import sys


#===============================================================================
# CONSTANTS
#===============================================================================

#: This is the project name
PRJ = "Yatel"

#: The project version as tuple of strings
VERSION = ("0", "1")

#: For "what" is usefull yatel
DOC = u"""Yatel allows the creation of user-profile-distance-based networks and
their multidimensional analysis through a process of exploration.

In the process of analyzing data from heterogeneous sources - like data
regarding biology, social studies, marketing, etc. -, it is often possible to
identify individuals or classes (groups of individuals that share some
characteristic). This individuals or groups are identified by attributes that
were measured and stored in the data base. For instance, in a biological
analysis, the profile can be defined by some certain properties of the
nucleic acid, in a social analysis by the data from people and in a
sales analysis by the data from sales point tickets.
    
"""

#: Home Page of yatel
URL = "http://yatel.readthedocs.org"

#: Author of this yatel
AUTHOR = "Yatel Team <utn_kdd@googlegroups.com>"

#: The project version as string
STR_VERSION = ".".join(VERSION)

#: The project root path
PRJ_PATH = os.path.dirname(os.path.abspath(__file__))

#: The license name
LICENSE = "GPL3"

#: The license of yatel
FULL_LICENSE = u"""This program is free software; you can redistribute it and/or 
modify it under the terms of the GNU General Public License as published by the 
Free Software Foundation; either version 3 of the License, or (at your option) 
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program; if not, write to the Free Software Foundation, Inc., 51 Franklin 
Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""

#: The path to the puser home path
HOME_PATH = os.path.expanduser("~")


#: This is a folder where user put his data
YATEL_USER_PATH = os.path.join(HOME_PATH, ".yatel")
if not os.path.isdir(YATEL_USER_PATH):
    os.makedirs(YATEL_USER_PATH)


#: A Set containing all the encodings knowin by python
ENCODINGS = tuple(sorted(set(encodings.aliases.aliases.values())))


#: Determines the default encoding of the files (default utf-8)
DEFAULT_FILE_ENCODING = encodings.aliases.aliases.get(
    sys.getfilesystemencoding().lower().replace("-", ""),
    "utf_8"
)

DATETIME_FORMAT = "%Y/%M/%d %H:%M:%S.%f"

DEBUG = __debug__


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
