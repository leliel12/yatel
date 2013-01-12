#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This module is used for construct yatel.dom object using yatel json format
files

"""

#===============================================================================
# IMPORTS
#===============================================================================

import json

from yatel import dom
from yatel.conversors import dict2yatel


#===============================================================================
# IO FUNCTIONS
#===============================================================================

def dump(haps, facts, edges, stream=None, **kwargs):
    """Convert dom objects into yjf stream

    """
    data = dict2yatel.dump(haps, facts, edges)
    dumper = json.dump if stream else json.dumps
    return dumper(data, stream, **kwargs)


def load(stream, **kwargs):
    """Convert YJF stream into dom objects

    """
    loader = json.loads if isinstance(stream, str) else json.load
    data = loader(stream, **kwargs)
    return dict2yatel.load(data)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

