#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


# =============================================================================
# DOC
# =============================================================================

"""Utilities to persist yatel into different file formats"""


# =============================================================================
# IMPORTS
# =============================================================================

from yatel.io.core import BaseParser
from yatel.io import yjf, yxf


# =============================================================================
# IMPORTS
# =============================================================================

PARSERS = {}
SYNONYMS = []
for p in BaseParser.__subclasses__():
    syns = tuple(set(p.file_exts()))
    for ext in syns:
        PARSERS[ext] = p
    SYNONYMS.append(syns)
SYNONYMS = frozenset(SYNONYMS)
del p


# =============================================================================
# FUNCTIONS
# =============================================================================

def load(ext, nw, stream, *args, **kwargs):
    """Deserialize data from a file or formatted string into the yatel db
        
    Parameters
    ----------
    ext:
        
    nw : yatel.db.YatelNetwork
        network destination for data
        
    stream: str or file like object
        source of data

    """
    parser = PARSERS[ext]()
    if isinstance(stream, basestring):
        return parser.loads(nw, stream, *args, **kwargs)
    return parser.load(nw, stream, *args, **kwargs)


def dump(ext, nw, stream=None, *args, **kwargs):
    """Serializes data from a yatel network to a file or string
    
    Parameters
    ----------
    ext:
        
    nw: yatel.db.YatelNetwork
        
    stream: None or bool
        Type of source data if stream is *None* assumes the source is a str 
        otherwise expects a file like object
        
    args : arguments for file source
        
    kwargs: keywords arguments for json module
        
    Returns
    -------
    string: str or None
        Returns the serialized yatel db to a formatted string if strean=None
    
    """
    parser = PARSERS[ext]()
    if stream is None:
        return parser.dumps(nw, *args, **kwargs)
    return parser.dump(nw, stream, *args, **kwargs)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(__doc__)
