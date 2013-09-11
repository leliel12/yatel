#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This package contains several modules for serielze yatel dom object
into streams

"""

#===============================================================================
# IMPORTS
#===============================================================================

import inspect

from yatel.io.core import BaseParser, ParserError

#===============================================================================
# FUNCTIONS
#===============================================================================

_pars = {}
def register(cls, *rtypes):
    if not inspect.isclass(cls) or not issubclass(cls, BaseParser):
        raise TypeError("'cls' must be subclass of 'yatel.io.BaseParser'")
    for rtype in rtypes:
        _pars[rtype] = cls


def parsers():
    return _pars.keys()


def parser(rtype):
    return _pars[rtype]


def load(rtype, nw, stream, **kwargs):
    cls = _pars[rtype]
    parser = cls()
    return parser.load(nw, stream=stream, **kwargs)


def dump(rtype, nw, stream=None, **kwargs):
    cls = _pars[rtype]
    parser = cls()
    return parser.dump(nw, stream=stream, **kwargs)


#===============================================================================
# REGISTERS!
#===============================================================================

from yatel.io import json_parser
register(json_parser.JSONParser, "yjf", "json")


from yatel.io import yaml_parser
register(yaml_parser.YAMLParser, "yyf", "yaml", "ymf")

from yatel.io import xml_parser
register(xml_parser.XMLParser, "xml", "yxf")

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
