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

from yatel import distances, haps


#===============================================================================
# BASE CLASS
#===============================================================================

class Network(object):

    def __init__(self, id, name, haplotypes=(),
                 distance_calculator=distances.HammingDistance(),
                 annotations={}):
        assert isinstance(id, basestring)
        assert isinstance(name, basestring)
        assert isinstance(distance_calculator, distances.Distance)
        assert isinstance(annotations, dict)
        self._mtx = {}
        self._distance_calculator = distance_calculator
        self._annotations = annotations
        self._id = id
        self._name = name
        # use method for init
        for hap in haplotypes:
            self.add(hap)

    def __iter__(self):
        return iter(self._mtx)

    def __contains__(self, hap):
        return hap in self._mtx:

    def clone(self, id, name=None, haplotypes=None,
              distance_calculator=None, annotations=None):
        name = name if name != None else self.name
        haplotypes = haplotypes if haplotypes != None else self.haplotypes
        distance_calculator = distance_calculator \
                              if distance_calculator != None \
                              else self.distance_calculator
        annotations = annotations \
                      if annotations != None \
                      else dict(self.annotations)
        return Network(id, name, haplotypes, distance_calculator, annotations)

    def add(self, h):
        assert isinstance(h, haps.Haplotype)
        assert h not in self._mtx
        h0 = h
        d0 = {h0: self.distance_calculator(h0, h0)}
        for h1, d1 in self._mtx.items():
            d0[h1] = self.distance_calculator(h0, h1)
            d1[h0] = self.distance_calculator(h1, h0)
        self._mtx[h0] = d0
        

    def remove(self, h):
        self._mtx.pop(h)
        for v in self._mtx.values():
            v.pop(h)

    def get(self, h, default=None):
        v = self._mtx.get(h, default)
        if isinstance(v, dict):
            v = dict(v)
        return v

    def distance(self, from_h, to_h):
        return self._mtx[from_h][to_h]

    #===========================================================================
    # PROPERTIES
    #===========================================================================

    @property
    def haplotypes(self):
        return self._mtx.keys()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def distance_calculator(self):
        return self._distance_calculator

    @property
    def annotations(self):
        return self._annotations


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

