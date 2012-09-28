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

#: The project version as string
STR_VERSION = ".".join(VERSION)

#: For "what" is usefull yatel
DOC = (u"Yatel allows the creation of user-profile-distance-based networks and "
       u"their multidimensional analysis through a process of exploration.\n"
       u"In the process of analyzing data from heterogeneous sources - like "
       u"data regarding biology, social studies, marketing, etc. -, it is often "
       u"possible to identify individuals or classes (groups of individuals "
       u"that share some characteristic). This individuals or groups are "
       u"identified by attributes that were measured and stored in the data "
       u"base. For instance, in a biological analysis, the profile can be "
       u"defined by some certain properties of the nucleic acid, in a social "
       u"analysis by the data from people and in a sales analysis by the data "
       u"from sales point tickets.")
       

#: The short description for pypi
SHORT_DESCRIPTION = DOC.splitlines()[0]

#: Clasifiers for optimize search in pypi
CLASSIFIERS = (
    "Topic :: Utilities",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Programming Language :: Python :: 2",
)

#: Home Page of yatel
URL = "http://bitbucket.org/liricus/socialframe"

#: Download for pypi
DOWNLOAD_URL = "{}/downloads/{}-{}.tar.gz".format(URL, PRJ.lower(), STR_VERSION)

#: Author of this yatel
AUTHOR = "Yatel Team"

#: Email ot the autor
EMAIL = "utn_kdd@googlegroups.com"

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
#: external libraries for made yatel work
DEPENDENCIES = ("peewee", 
                "pycante", 
                "csvcool",
                "pyzmq",
                "ipython",
                "PyQt",
                "graph-tool",
                "pilas==0.68")

#: Keywords for search of pypi
KEYWORDS = """Yatel user-profile-distance-based networks  multidimensional
exploration biology database kdd datamining"""

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

#: Format to represent the datetime
DATETIME_FORMAT = "%Y/%M/%d %H:%M:%S"

#: If the program is en debug mode
DEBUG = __debug__


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
