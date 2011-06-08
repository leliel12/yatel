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

"""


"""


#===============================================================================
# META
#===============================================================================

__version__ = "0.1"
__license__ = "GPL3"
__author__ = "JBC "
__mail__ = "jbc dot develop at gmail dot com"
__since__ = "0.1"
__date__ = "2011-03-02"

    
#===============================================================================
# HAPLOTYPE
#===============================================================================

class Haplotype(object):
    
    def __init__(self, name, **atts):
        assert isinstance(name, basestring)
        self._name = name
        self._atts = atts

    def __repr__(self):
        return "<%s '%s' at %s>" % (self.__class__.__name__,
                                    self.name,
                                    hex(id(self)))

    def __eq__(self, obj):
        return isinstance(obj, self.__class__) and obj.name == self.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __getattr__(self, name):
        return self._atts[name]
        
    @property
    def name(self):
        return self._name
    
    @property
    def attributes(self):
        return dict(self._atts)
        

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__
