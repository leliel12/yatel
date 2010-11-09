#!/usr/bin/env python
#-*-coding:utf-8-*-

# Copyright (C) 2010 Juan BC <jbc dot develop at gmail dot com>

# Biopython License Agreement

# Permission to use, copy, modify, and distribute this software and its
# documentation with or without modifications and for any purpose and
# without fee is hereby granted, provided that any copyright notices
# appear in all copies and that both those copyright notices and this
# permission notice appear in supporting documentation, and that the
# names of the contributors or copyright holders not be used in
# advertising or publicity pertaining to distribution of the software
# without specific prior permission.

# THE CONTRIBUTORS AND COPYRIGHT HOLDERS OF THIS SOFTWARE DISCLAIM ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL THE
# CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY SPECIAL, INDIRECT
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
# OR PERFORMANCE OF THIS SOFTWARE.

#===============================================================================
# FUTURE
#===============================================================================

from __future__ import absolute_import


#===============================================================================
# DOCS
#===============================================================================

"""
    
    
"""


#===============================================================================
# META
#===============================================================================

__version__ = "0.1"
__license__ = "Biopython License"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2010-08-04"


#===============================================================================
# IMPORTS
#===============================================================================



from Bio import SeqRecord 

from yatel import Network

from yatel.NetworkIO.base import AbstractNetworkFileHandler
from yatel.NetworkIO.base import NetworkFileHandlerError

from yatel.NetworkIO import njd


#===============================================================================
# REGISTER
#===============================================================================

_parsers = {}


def register_parser(name, parser_class):
    assert issubclass(parser_class, AbstractNetworkFileHandler), \
           "parser_class must be 'AbstractNetworkFileHandler' instance find: %s" \
           % str(type(parser_class))
    assert isinstance(name, basestring), \
           "name must be str or unicode instance find: %s" % str(type(name))
    _parsers[name] = parser_class
    

def unregister_parser(name):
    _parsers.pop(name)


def parsers():
    return _parsers.keys()


def get_parser(parser_name):
    return _parsers[parser_name]


#===============================================================================
# FUNCTIONS
#===============================================================================

def read(handle, format):
    assert hasattr(handle, "read") and callable(handle.read), \
           "handle not have read method"
    return _parsers[format]().read(handle)


def parse(handle, format):
    assert hasattr(handle, "read") and callable(handle.read), \
           "handle not have read method"
    return _parsers[format]().parse(handle)


def write(networks, handle, format):
    assert hasattr(handle, "write") and callable(handle.write), \
           "handle not have write method"
    assert all(map(lambda r: isinstance(r, Network.Network), networks)), \
           "networks must be an iterable of SeqRecords"
    return _parsers[format]().write(networks, handle)


#===============================================================================
# CHARGE
#===============================================================================

register_parser("njd", njd.NJDFileHandler)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

