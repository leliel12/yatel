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
from reportlab.lib.validators import isCallable


#===============================================================================
# DOCS
#===============================================================================

"""Tests Suits"""


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

import unittest
import random
import os

from yatel import haps, distances, network, networkinfo


#===============================================================================
# HAPLOTYPE TESTS
#===============================================================================

class HaplotypeTest(unittest.TestCase):
    
    def test_creation(self):
        hap0a = haps.Haplotype("hap0a", att0=1, att1="hi")
        hap0b = haps.Haplotype("hap0b", att0=1, att1="hi")
        hap1b = haps.Haplotype("hap1a", att0=2, att1="bye")
        hap1b = haps.Haplotype("hap1b", att0=2, att1="bye")

    
#===============================================================================
# DISTANCES
#===============================================================================

class TestDistances(unittest.TestCase):
    
    def setUp(self):
        self.h0a = haps.Haplotype("hap0a", att0=1, att1="hi")
        self.h0b = haps.Haplotype("hap0b", att0=1, att1="hi")
        self.h1a = haps.Haplotype("hap1a", att0=2, att1="bye")
        self.h1b = haps.Haplotype("hap1b", att0=2, att1="bye")
        
    def test_hamming(self):
        d = distances.HammingDistance()
        self.assertEquals(d.distance_of(self.h0a, self.h0b), 0)
        self.assertEquals(d.distance_of(self.h1a, self.h1b), 0)
        self.assertEquals(d.distance_of(self.h1a, self.h0b), 2)
        self.assertEquals(d.distance_of(self.h1b, self.h0a), 2)
        
    def test_expert(self):
        # get random distances
        d0a0b = random.random()
        d0a1b = random.random()
        d1a0b = random.random()
        d1a1b = random.random()
        
        # create the expert
        d = distances.ExpertDistance()
        d.add_distance(self.h0a, self.h0b, d0a0b)
        d.add_distance(self.h0a, self.h1b, d0a1b)
        d.add_distance(self.h1a, self.h0b, d1a0b)
        d.add_distance(self.h1a, self.h1b, d1a1b)
        
        # test
        self.assertEquals(d.distance_of(self.h0a, self.h0b), d0a0b)
        self.assertEquals(d.distance_of(self.h0a, self.h1b), d0a1b)
        self.assertEquals(d.distance_of(self.h1a, self.h0b), d1a0b)
        self.assertEquals(d.distance_of(self.h1a, self.h1b), d1a1b)

        
#===============================================================================
# NETWORK TEST
#===============================================================================

class NetworkTest(unittest.TestCase):
    
    def setUp(self):
        self.h0a = haps.Haplotype("hap0a", att0=1, att1="hi")
        self.h0b = haps.Haplotype("hap0b", att0=1, att1="hi")
        self.h1a = haps.Haplotype("hap1a", att0=2, att1="bye")
        self.h1b = haps.Haplotype("hap1b", att0=2, att1="bye")
        
        # create distance
        d0a0b = random.random()
        d0a1b = random.random()
        d1a0b = random.random()
        d1a1b = random.random()
        d = distances.ExpertDistance()
        d.add_distance(self.h0a, self.h0b, d0a0b)
        d.add_distance(self.h0a, self.h1b, d0a1b)
        d.add_distance(self.h1a, self.h0b, d1a0b)
        d.add_distance(self.h1a, self.h1b, d1a1b)
        
        self.nw = network.Network(id=str(random.random()),
                                  name=str(random.random()),
                                  haplotypes=(self.h0a, self.h0b, self.h1a, self.h1b),
                                  distance_calculator=d,
                                  annotations=dict((str(random.random()), random.random()) 
                                                   for _ in range(random.randint(0, 100))))
                                           
    
    def test_haps_in_nw(self):
        self.assertTrue(self.h0a in self.nw) 
        self.assertTrue(self.h0b in self.nw)
        self.assertTrue(self.h1a in self.nw)
        self.assertTrue(self.h1b in self.nw)
        self.assertTrue(haps.Haplotype("hap1b", att0=2, att1="bye")
                        in self.nw)
        self.assertTrue(not haps.Haplotype("hap1bz", att0=2, att1="bye")
                        in self.nw)
    

#===============================================================================
# NETWORK INFO TEST
#===============================================================================

class NetworkInfoTest(unittest.TestCase):
    
    def setUp(self):
        self.h0a = haps.Haplotype("hap0a", att0=1, att1="hi")
        self.h0b = haps.Haplotype("hap0b", att0=1, att1="hi")
        self.h1a = haps.Haplotype("hap1a", att0=2, att1="bye")
        self.h1b = haps.Haplotype("hap1b", att0=2, att1="bye")
        
        # create distance
        d0a0b = random.random()
        d0a1b = random.random()
        d1a0b = random.random()
        d1a1b = random.random()
        d = distances.ExpertDistance()
        d.add_distance(self.h0a, self.h0b, d0a0b)
        d.add_distance(self.h0a, self.h1b, d0a1b)
        d.add_distance(self.h1a, self.h0b, d1a0b)
        d.add_distance(self.h1a, self.h1b, d1a1b)
        
        self.nw = network.Network(id=str(random.random()),
                                  name=str(random.random()),
                                  haplotypes=(self.h0a, self.h0b, self.h1a, self.h1b),
                                  distance_calculator=d,
                                  annotations=dict((str(random.random()), random.random()) 
                                                   for _ in range(random.randint(0, 100))))
        self.nwi = networkinfo.NetworkInfo(self.nw)
        
    def test_all(self):
        for k in dir(self.nwi):
            if not k.startswith("_"):
                v = getattr(self.nwi, k)
                if isCallable(v):
                    v()
                else:
                    v
    

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    unittest.main()


