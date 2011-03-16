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
        assert isinstance(atts, dict)
        self._name = name
        self._atts = atts

    def __len__(self):
        return len(self._len)

    def __iter__(self):
        return iter(self._atts)
    
    def __getitem__(self, k):
        return self._atts[k]
    
    def items(self):
        return self._atts.items()
        
    def values(self):
        return self._atts.values()
        
    def keys(self):
        return self._atts.keys()
        

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__
