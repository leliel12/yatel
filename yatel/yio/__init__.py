#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# DOC
#===============================================================================

"""Utilities to persist yatel into diferent file formats"""


#===============================================================================
# IMPORTS
#===============================================================================

from yatel.yio.core import BaseParser
from yatel.yio import yjf, yxf


#===============================================================================
# CONSTANTS
#===============================================================================

#: Parsers container
PARSERS = {}
#: Synonyms of parser names
SYNONYMS = []
for p in BaseParser.__subclasses__():
    syns = tuple(set(p.file_exts()))
    for ext in syns:
        PARSERS[ext] = p
    SYNONYMS.append(syns)
SYNONYMS = frozenset(SYNONYMS)
del p

#===============================================================================
# FUNCTIONS
#===============================================================================

def load(ext, nw, stream, *args, **kwargs):
    """Deserializea from a `stream` to yatel network.
    
    Parameters
    ----------
    ext : str
        Extension of source data.
    nw : yatel.db.YatelNetwork
        Target database.
    stream : file or str
        Source, can be string or a file.
    
    """
    parser = PARSERS[ext]()
    if isinstance(stream, basestring):
        return parser.loads(nw, stream, *args, **kwargs)
    return parser.load(nw, stream, *args, **kwargs)


def dump(ext, nw, stream=None, *args, **kwargs):
    """Serializes from a yatel network to a file or string.
    
    Parameters
    ----------
    ext : str
        Extension of target data.
    nw : yatel.db.YatelNetwork
        Source database.
    stream : file or str
        Target, can be string or a file.
    
    """
    parser = PARSERS[ext]()
    if stream is None:
        return parser.dumps(nw, *args, **kwargs)
    return parser.dump(nw, stream, *args, **kwargs)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
