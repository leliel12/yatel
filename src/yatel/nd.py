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
__since__ = "0.1"
__date__ = "2011-03-02"


#===============================================================================
# IMPORTS
#===============================================================================

import inspect
import itertools

from pygraph.classes import graph

from yatel import ndistances, haps


#===============================================================================
# CONSTANTS
#===============================================================================

CONNECTIVITY_ALL = "ALL"


#===============================================================================
# BASE CLASS
#===============================================================================

class NetworkDescriptor(object):

    def __init__(self, nwid, haplotypes=(), connectivity=CONNECTIVITY_ALL,
                 ndistance_calculator=ndistances.LinkDistance(),
                 annotations={}):
        assert isinstance(nwid, basestring)
        assert _validate_haps(haplotypes)
        assert isinstance(ndistance_calculator, ndistances.NDistance)
        assert isinstance(annotations, dict)
        assert _validate_connectivity(connectivity)
        
        super(self.__class__, self).__init__()
        
        self._nwid = nwid
        self._ndistance_calculator = ndistance_calculator
        self._annotations = annotations
        self._conn = connectivity
        self._haps = set()
        self._edges = set()
    
        for h in haplotypes:
            attrs = [("name", h.name)]
            attrs.extend(h.attributes.items())
            self._add_haplotype(h)
             
        else:
            haps_prod = itertools.product(haplotypes, haplotypes)
            if self._conn == CONNECTIVITY_ALL:
                for h0, h1 in haps_prod:
                    w = abs(self._ndistance_calculator(h0, h1))
                    self._add_edge(h0, h1, w)
            if callable(self._conn):
                for h0, h1 in haps_prod:
                    if self._conn(h0, h1):
                        w = abs(self._ndistance_calculator(h0, h1))
                        self._add_edge(h0, h1, w)
            elif getattr(self._conn, '__iter__', False):
                for h0, h1 in haps_prod:
                    if (h0, h1) in self._conn:
                        w = abs(self._ndistance_calculator(h0, h1))
                        self._add_edge(h0, h1, w)
                    
    def __eq__(self, obj):
        return isinstance(obj, self.__class__) and \
                self._nwid == obj._nwid and \
                self._ndistance_calculator == obj._ndistance_calculator and \
                self._annotations == obj._annotations and \
                self._conn == obj._conn
                
    def __ne__(self, obj):
        return not self == obj
    
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return "<%s (%i Haplotypes) at %s>" % (self.__class__.__name__, 
                                                len(self.haplotypes),
                                                hex(id(self)))
    
    def _add_haplotype(self, hap):
        self._haps.add(hap)
    
    def _add_edge(self, hap0, hap1, w):
        if hap0 not in self._haps:
            msg = "hap0 (%s) not in this descriptor" % repr(hap0)
            raise ValueError(hap0)
        if hap1 not in self._haps:
            msg = "hap1 (%s) not in this descriptor" % repr(hap1)
            raise ValueError(hap0)
        self._edges.add((hap0, hap1, w))
    
    @property
    def haplotypes(self):
        return tuple(self._haps)

    @property
    def nodes(self):
        return tuple(self._haps)
    
    @property
    def edges(self):
        return tuple(self._edges)

    @property
    def nwid(self):
        return self._id

    @property
    def ndistance_calculator(self):
        return self._ndistance_calculator

    @property
    def annotations(self):
        return self._annotations

    @property
    def connectivity(self):
        return self._conn

                    
#===============================================================================
# SUPPORT
#===============================================================================

def _validate_haps(haplotypes):
    for h in haplotypes:
        if not isinstance(h, haps.Haplotype):
            return False
    return True
        

def _validate_connectivity(c):
    if c == CONNECTIVITY_ALL:
        return True
    if getattr(c, '__iter__', False):
        for ce in c:
            if not isinstance(ce, tuple) or len(ce) != 2 \
            or not isinstance(ce[0], haps.Haplotype) \
            or not isinstance(ce[1], haps.Haplotype):
                return False
        return True
    if callable(c):
        args = inspect.getargspec(c).args
        if inspect.isfunction(c) and len(args) != 2:
            return False
        if inspect.ismethod(c) and len(args) != 3:
            return False


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

