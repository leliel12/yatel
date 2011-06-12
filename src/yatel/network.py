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

from pygraph.classes.graph import graph

from yatel import ndistances, haps


#===============================================================================
# CONSTANTS
#===============================================================================

CONNECTIVITY_ALL = "ALL"

#===============================================================================
# BASE CLASS
#===============================================================================

class Network(object):

    def __init__(self, id, haplotypes=(), connectivity=CONNECTIVITY_ALL,
                 ndistance_calculator=ndistances.LinkDistance(),
                 annotations={}):
        assert isinstance(id, basestring)
        assert _validate_haps(haplotypes)
        assert isinstance(ndistance_calculator, ndistances.NDistance)
        assert isinstance(annotations, dict)
        assert _validate_connectivity(connectivity)
        
        # internal graph
        self._graph = graph()
        
        # setup all
        self._id = id
        self._connectivity = connectivity
        self._ndistance_calculator = ndistance_calculator
        self._annotations = annotations
        self._conn = connectivity
        self._graph.add_nodes(haplotypes)
        
        for h0 in haplotypes:
            for h1 in haplotypes:
                if connectivity==CONNECTIVITY_ALL or \
                    (callable(connectivity) and connectivity(h0, h1)) or \
                    (h0, h1) in connectivity:
                        w = ndistance_calculator(h0, h1)
                        self._graph.add_edge((h0, h1), w)
                        
    #===========================================================================
    # PROPERTIES
    #===========================================================================

    @property
    def haplotypes(self):
        return self._graph.nodes()

    @property
    def id(self):
        return self._id

    @property
    def ndistance_calculator(self):
        return self._ndistance_calculator

    @property
    def annotations(self):
        return dict(self._annotations)

    @property
    def connectivity(self):
        if isinstance(self._conn, list):
            return tuple(self._conn)
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
    print __doc__

