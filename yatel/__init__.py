#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

(u"Yatel allows the creation of user-profile-distance-based networks and "
u"their multidimensional analysis through a process of exploration.\n"
u"In the process of analyzing data from heterogeneous sources - like "
u"data regarding biology, social studies, marketing, etc. -, it is "
u"often possible to identify individuals or classes (groups of  "
u"individuals that share some characteristic). This individuals or "
u"groups are identified by attributes that were measured and stored in "
u"the data data base. For instance, in a biological analysis, the "
u"profile can be defined by some certain properties of the nucleic "
u"acid, in a social  analysis by the data from people and in a sales "
u"analysis by the data from sales point tickets.")


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
VERSION = ("0", "2")

#: The project version as string
STR_VERSION = ".".join(VERSION)
__version__ = STR_VERSION

#: For "what" is usefull yatel
DOC = __doc__

#: The short description for pypi
SHORT_DESCRIPTION = DOC.splitlines()[0]

#: Clasifiers for optimize search in pypi
CLASSIFIERS = (
    "Topic :: Utilities",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 2",
)

#: Home Page of yatel
URL = "http://bitbucket.org/leliel12/yatel"

#: Download for pypi
DOWNLOAD_URL = "{}/downloads/{}-{}.tar.gz".format(URL, PRJ.lower(),
                                                   STR_VERSION)

#: Url of the official yatel doc
DOC_URL = "http://yatel.readthedocs.org"

#: Author of this yatel
AUTHOR = "Yatel Team"

#: Email ot the autor
EMAIL = "utn_kdd@googlegroups.com"

#: The project root path
PRJ_PATH = os.path.dirname(os.path.abspath(__file__))

#: The license name
LICENSE = "WISKEY-WARE"

#: The license of yatel
FULL_LICENSE = u""""THE WISKEY-WARE LICENSE":
<utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
you can do whatever you want with this stuff. If we meet some day, and you
think this stuff is worth it, you can buy us a WISKEY us return.

"""

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
