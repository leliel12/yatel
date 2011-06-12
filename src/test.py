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
import time

import numpy

from yatel import haps, ndistances, network, networkinfo, io, facts


#===============================================================================
# CONSTANTS
#===============================================================================

DIGITS = 4


#===============================================================================
# TEST IN ORDER
#===============================================================================

def randomdict():
    d = {}
    for _ in range(random.randint(0, 100)):
        d[str(random.random())] = str(random.random())
    return d
         

def randomrange(limit_low, limit_up):
    return range(random.randint(limit_low, limit_up))


#===============================================================================
# FACTS
#===============================================================================

class HaplotypeTest(unittest.TestCase):
    
    def test_all(self):
        for _ in range(1000):
            h = haps.Haplotype(str(time.time()), **randomdict())


#===============================================================================
# FACTS TESTS
#===============================================================================

class FactsTest(unittest.TestCase):
    
    def test_all(self):
        hs = []
        ants = randomdict()
        for _ in randomrange(0, 100):
            h = haps.Haplotype(str(time.time()), **randomdict())
            hs.append(h)
        fact = facts.Fact(str(time.time()), hs, **ants)
        for h in fact.haplotypes:
            self.assertTrue(h in hs)
        for k, v in ants.items():
            self.assertEqual(v, getattr(fact, k))
            
  
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
        d = ndistances.HammingDistance()
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
        d = ndistances.ExpertDistance()
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
        self.haplotypes = [haps.Haplotype(str(name), **randomdict())
                           for name in randomrange(10, 100)]
        self.conn = set([(random.choice(self.haplotypes), random.choice(self.haplotypes))
                         for _ in randomrange(10, 50)])
        self.ann = randomdict()
        self.nw = network.Network(id=str(random.random), 
                                  haplotypes=self.haplotypes, 
                                  connectivity=self.conn,
                                  ndistance_calculator=ndistances.LinkDistance(),
                                  annotations=self.ann)
                                  
    def test_(self):
        print self.conn   


#===============================================================================
# NETWORK INFO TEST
#===============================================================================

class NetworkInfoTest(unittest.TestCase):
    pass 

        
#===============================================================================
# NETWORK IO TEST
#===============================================================================

class IOTest(unittest.TestCase):
    pass

    
#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    unittest.main()


