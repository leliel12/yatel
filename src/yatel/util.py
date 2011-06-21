#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.


#===============================================================================
# DOCS
#===============================================================================


"""Various utilities for yatel."""


#===============================================================================
# META
#===============================================================================

__version__ = "0.1"
__license__ = "GPL3"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2011-02-17"

#===============================================================================
# CLASSES
#===============================================================================

class StringParser(object):
    
    def __init__(self, **kwargs):
        self._types_parser = {}
        self._default = {}
        for type_name, methods in kwargs.items():
            dumps, loads = methods
            self.add_parser(type_name, dumps, loads)
            
    def add_parser(self, type_name, dumps, loads):
        assert isinstance(type_name, basestring)
        assert callable(dumps)
        assert callable(loads)
        self._types_parser[type_name] = {"dumps": dumps, "loads": loads}
    
    def del_parser(self, type_name):
        self._types_parser.pop(type_name)
       
    def loads(self, value_type, value):
        return self._types_parser[value_type]["loads"](value)
    
    def dumps(self, value):
        type_name = unicode(type(value).__name__)
        return self._types_parser[type_name]["dumps"](value), type_name
        
    @property
    def valid_types(self):
        return self._types.keys()
        
        
#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__
