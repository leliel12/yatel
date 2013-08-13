#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This package contains several modules for convert yatel dom object
into objests of another libraries

"""

#===============================================================================
# IMPORTS
#===============================================================================

import inspect

#===============================================================================
# FUNCTIONS
#===============================================================================

from yatel.conv.coreconv import BaseConverter, ConversionError

_convs = {}


def register(cls, *rtypes):
    if not inspect.isclass(cls) or not issubclass(cls, BaseConverter):
        raise TypeError("'cls' must be subclass of 'yatel.con.BaseConverter'")
    for rtype in rtypes:
        _convs[rtype] = cls


def convs():
    return _convs.keys()


def conv(rtype):
    return _convs[rtype]


def load(rtype, nw, stream, **kwargs):
    cls = _convs[rtype]
    conv = cls()
    return conv.load(nw, stream=stream, **kwargs)


def dump(rtype, nw, stream=None, **kwargs):
    cls = _convs[rtype]
    conv = cls()
    return conv.dump(nw, stream=stream, **kwargs)


#===============================================================================
# REGISTERS!
#===============================================================================

from yatel.conv import jsonconv
register(jsonconv.JSONConverter, "yjf", "json")


from yatel.conv import yamlconv
register(yamlconv.YAMLConverter, "yyf", "yaml", "yml")


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
