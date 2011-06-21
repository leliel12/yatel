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
__license__ = "GPL3"
__author__ = "JBC"
__mail__ = "jbc dot develop at gmail dot com"


#===============================================================================
# IMPORTS
#===============================================================================

from yatel import haps


#===============================================================================
# FACTS
#===============================================================================

class Fact(object):
    
    def __init__(self, fid, haplotypes=(), **atts):
        assert all(map(lambda h: isinstance(h, haps.Haplotype), haplotypes))
        assert isinstance(fid, basestring)
        self._fid = fid
        self._haps = tuple(haplotypes)
        self._atts = atts

    def __getattr__(self, k):
        return self._atts[k] 
    
    def __eq__(self, obj):
        return isinstance(obj, self.__class__) and obj.id == self.id
    
    def __hash__(self):
        return hash(self.id)

    @property
    def haplotypes(self):
        return self._haps

    @property
    def attributes(self):
        return dict(self._atts)

    @property
    def fid(self):
        return self._fid


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__
