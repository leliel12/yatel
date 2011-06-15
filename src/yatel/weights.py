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
__author__ = "JBC"
__mail__ = "jbc dot develop at gmail dot com"
__since__ = "0.1"
__date__ = "2011-03-02"



#===============================================================================
# IMPORTS
#===============================================================================

import abc

import random

#===============================================================================
# BASE CLASS
#===============================================================================

class Weight(object):
    """Base class for all edges weights classes

    You need to impelment weight_of(seq0, seq1) method.

    """

    __metaclass__ = abc.ABCMeta

    def __call__(self, hap0, hap1):
        return self.weight_of(hap0, hap1)

    @abc.abstractmethod
    def weight_of(self, hap0, hap1):
        """Returns the weight between hap0 and hap1"""
        raise NotImplementedError()
        
        
#===============================================================================
# LINK DISTANCE CLASS
#===============================================================================

class LinkWeight(Weight):

    def weight_of(self, hap0, hap1):
        return 1


#===============================================================================
# HAMMING DISTANCE CLASS
#===============================================================================

class HammingWeight(Weight):

    def weight_of(self, hap0, hap1):
        d = abs(len(hap0.attributes) - len(hap1.attributes))
        for k, v in hap0.attributes.items():
            d += 1 if v != hap1.attributes.get(k, None) else 0
        return d


#===============================================================================
# EXPERT DISTANCE CLASS
#===============================================================================

class ExpertWeight(Weight):

    def __init__(self):
        self._ws = {}

    def add_Weight(self, hap0, hap1, w):
        self._ws[(hap0, hap1)] = w

    def weight_of(self, hap0, hap1):
        return self._ws.get((hap0, hap1), 1)


#===============================================================================
# RANDOM DISTANCE CLASS
#===============================================================================

class RandomWeight(Weight):

    def weight_of(self, hap0, hap1):
        return random.random()
        

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

