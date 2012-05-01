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

import os


#===============================================================================
# CONSTANTS
#===============================================================================

# This is the project name
PRJ = "Yatel"

# The project version as tuple of strings
VERSION = ("0", "1")

# The project version as string
STR_VERSION = ".".join(VERSION)

# The project root path
PRJ_PATH = os.path.dirname(os.path.abspath(__file__))


# The path to the puser home path
try:
    # ...works on at least windows and linux.
    # In windows it points to the user"s folder
    #  (the one directly under Documents and Settings, not My Documents)

    # In windows, you can choose to care about local versus roaming profiles.
    # You can fetch the current user"s through PyWin32.
    #
    # For example, to ask for the roaming "Application Data" directory:
    # CSIDL_APPDATA asks for the roaming, CSIDL_LOCAL_APPDATA for the local one
    from win32com.shell import shellcon, shell
    HOME_PATH = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
except ImportError:
    # quick semi-nasty fallback for non-windows/win32com case
    HOME_PATH = os.path.expanduser("~")


# This is a folder where user put his data
YATEL_USER_PATH = os.path.join(HOME_PATH, ".yatel")
if not os.path.isdir(YATEL_USER_PATH):
    os.mkdir(YATEL_USER_PATH)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
