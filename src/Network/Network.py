#!/usr/bin/env python
#-*-coding:utf-8-*-

# Copyright (C) 2010 Juan BC <jbc dot develop at gmail dot com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


################################################################################
# DOCS
################################################################################

"""
    
    
"""


################################################################################
# META
################################################################################

__version__ = "0.1"
__license__ = "GPL3"
__author__ = "JB <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2010-08-04"


################################################################################
# IMPORTS
################################################################################

from Bio import Seq

import Distance

################################################################################
# CLASSES
################################################################################

class SeqNetwork(object):
    
    def __init__(self, iterable, distance=None):
        self._mtx = {}
        self.distance = distance \
                        if distance != None \
                        else Distance.DefaultDistance()
        for i in iterable:
            self.add(i)
    
    def re_calculate_distances(self):
        for seq0, distances in self._mtx.items():
            for seq1, distance in distances.items():
                distances[seq1] = self._distance.distance_of(seq0, seq1)
    
    def add(self, seq0):
        assert isinstance(seq, Seq.Seq), "seq0 must be Seq instance"
        if seq0 not in self._mtx:
            self._mtx[seq0] = {}
            for seq1, distances in self._mtx.items():
                if seq0 != seq1:
                    distances[seq0] = self._distance.distance_of(seq1, seq0)
                self._mtx[seq0][seq1] = self._distance.distance_of(seq0, seq1)
        
    def _get_distance(self):
        return self._distance
        
    def _set_distance(self, d):
        assert isinstance(d, Distance.Distance), \
               "distance must be Distance instance"
        self._distance = d
        
    distance = property(_get_distance, _set_distance)


################################################################################
# MAIN
################################################################################

if __name__ == "__main__":
    print __doc__

