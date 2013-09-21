#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY in return.


#===============================================================================
# DOCS
#===============================================================================

"""This package contains several modules for serilize yatel network object
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
    """Register a new parser for serielize ``yatel.db.YatelNetwork`` instances
    with ``yatel.io.load`` and ``yatel.io.dump`` function

    :param cls: New parser class
    :type cls: sub-class of ``yatel.io.BaseParser``
    :param rtype: arguments with valid files extensions for the given parser

    **Example**

    >>> from yatel.io import json_parser
    >>> register(json_parser.JSONParser, "yjf", "json")

    """
    if not inspect.isclass(cls) or not issubclass(cls, BaseParser):
        raise TypeError("'cls' must be subclass of 'yatel.io.BaseParser'")
    for rtype in rtypes:
        _pars[rtype] = cls


def parsers():
    """Returns a list of all valid file formats (extensions)"""
    return _pars.keys()


def parser(rtype):
    """Return the parser for the given file format"""
    return _pars[rtype]


def load(rtype, nw, stream, **kwargs):
    """Parse and store all the ``yatel.dom`` objects in the stream in to the
    given ``yatel.db.YatelNetwork`` instance. Is user responsability to call
    ``nw.confirm_changes`` after call this function.

    :param rtype: file format
    :type rtype: string
    :param nw: The ``yatel.db.YatelNetwork`` instance (must be in ``w`` or ``a``
               mode)
    :type db: yatel.db.YatelNetwork(w|a)
    :param stream: file-like object or string with valid code in the ``rtype``
                   format
    :type stream: file-like or string
    :param kwargs: keyword argument for the subjacent parser.

    **Example**

    >>> from yatel import nw, io
    >>> nw = db.YatelNetwork('memory', mode=db.MODE_WRITE)
    >>> with open("network.xml") as fp:
    ...     io.load("xml", nw, fp)
    >>> nw.confirm_changes()

    """
    cls = _pars[rtype]
    parser = cls()
    return parser.load(nw, stream=stream, **kwargs)


def dump(rtype, nw, stream=None, **kwargs):
    """Convert all the ``yatel.dom`` objects of given
    ``yatel.db.YatelNetwork`` intance into rtype format.
    If stream is none the resulting code is returned as string.


    :param rtype: file format
    :type rtype: string
    :param nw: The ``yatel.db.YatelNetwork`` instance (must be in ``r``)
    :type db: yatel.db.YatelNetwork(r)
    :param stream: file-like object in write mode or None
    :type stream: file-like or None
    :param kwargs: keyword argument for the subjacent parser.

    **Example**

    >>> from yatel import nw, io
    >>> nw = db.YatelNetwork('memory', mode=db.MODE_WRITE)
    >>> nw.add_elements([dom.Haplotype(1), dom.Haplotype(2), dom.Haplotype(3)])
    >>> nw.add_elements([dom.Fact(1, att0=True, att1=4),
    ...                  dom.Fact(2, att0=False),
    ...                  dom.Fact(2, att0=True, att2="foo")])
    >>> nw.add_elements([dom.Edge(12, 1, 2),
    ...                  dom.Edge(34, 2, 3),
    ...                  dom.Edge(1.25, 3, 1)])
    >>> nw.confirm_changes()
    >>> with open("network.xml", "w") as fp:
    ...     io.dmp("xml", nw, fp)

    """
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
