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

import numpy

from yatel import haps, distances, network, networkinfo, io


#===============================================================================
# CONSTANTS
#===============================================================================

DIGITS = 4


#===============================================================================
# TEST IN ORDER
#===============================================================================

_tests = []


def register(test_cls):
    _tests.append(test_cls)
    return test_cls


#===============================================================================
# HAPLOTYPE TESTS
#===============================================================================

@register
class HaplotypeTest(unittest.TestCase):
    
    def test_creation(self):
        haps.Haplotype("hap0a", att0=1, att1="hi")
        haps.Haplotype("hap0b", att0=1, att1="hi")
        haps.Haplotype("hap1a", att0=2, att1="bye")
        haps.Haplotype("hap1b", att0=2, att1="bye")

    
#===============================================================================
# DISTANCES
#===============================================================================

@register
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

@register
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

@register
class NetworkInfoTest(unittest.TestCase):
    
    def setUp(self):
        self.h0a = haps.Haplotype("hap0a", att0=1, att1="hi")
        self.h0b = haps.Haplotype("hap0b", att0=1, att1="hi")
        self.h1a = haps.Haplotype("hap1a", att0=2, att1="bye")
        self.h1b = haps.Haplotype("hap1b", att0=2, att1="bye")
        
        # create distance
        d0a0b = round(random.random(), DIGITS)
        d0a1b = round(random.random(), DIGITS)
        d1a0b = round(random.random(), DIGITS)
        d1a1b = round(random.random(), DIGITS)
        self.distances = (d0a0b, d0a1b, d1a0b, d1a1b)
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
        
    def test_distances(self):
        self.assertTrue(None not in self.nwi.distances())
        self.assertTrue(None in self.nwi.distances(ignore_none=False))
    

    def test_distances_avg(self):
        mavg = round(numpy.average(self.distances), DIGITS)
        self.assertEqual(mavg, round(self.nwi.distance_avg(), DIGITS))
        
    def test_distances_std(self):
        mstd = round(numpy.std(self.distances), DIGITS)
        self.assertEqual(mstd, round(self.nwi.distance_std(), DIGITS))
        
    def test_max_min(self):
        mmax = numpy.max(self.distances)
        mmin = numpy.min(self.distances)
        self.assertEqual(mmax, self.nwi.distance_max())
        self.assertEqual(mmin, self.nwi.distance_min())
        self.assertTrue(mmax >= mmin)
        
    def test_mode(self):
        freqs = self.nwi.distance_frequency()
        mf = numpy.max(freqs.values())
        for d in self.nwi.distance_mode():
            self.assertEqual(freqs[d], mf)
        
    def test_anti_mode(self):
        freqs = self.nwi.distance_frequency()
        mf = numpy.min(freqs.values())
        for d in self.nwi.distance_anti_mode():
            self.assertEqual(freqs[d], mf)
        
#===============================================================================
# NETWORK IO TEST
#===============================================================================

@register
class IOTest(unittest.TestCase):
    
    def setUp(self):
        self.h0a = haps.Haplotype("hap0a", att0=1, att1="hi")
        self.h0b = haps.Haplotype("hap0b", att0=1, att1="hi")
        self.h1a = haps.Haplotype("hap1a", att0=2, att1="bye")
        self.h1b = haps.Haplotype("hap1b", att0=2, att1="bye")
        
        self.nw = network.Network(id=str(random.random()),
                                  name=str(random.random()),
                                  haplotypes=(self.h0a, self.h0b, self.h1a, self.h1b),
                                  annotations=dict((str(random.random()), str(random.random())) 
                                                   for _ in range(random.randint(0, 100))))
    def test_csv(self):
        pnw = io.loads("csv", io.dumps("csv", self.nw))
        for hap0 in pnw:
            self.assertTrue(hap0 in self.nw)
            for hap1 in pnw:
                dorig = self.nw.distance(hap0, hap1)
                dpar = pnw.distance(hap0, hap1)
                self.assertEqual(dorig, dpar)
        self.assertEqual(pnw.name, "")
        self.assertEqual(pnw.id, "")
        self.assertEqual(pnw.annotations, {})
        
    def test_njd(self):
        pnw = io.loads("njd", io.dumps("njd", self.nw))
        for hap0 in pnw:
            self.assertTrue(hap0 in self.nw)
            for hap1 in pnw:
                dorig = round(self.nw.distance(hap0, hap1), DIGITS)
                dpar = round(pnw.distance(hap0, hap1), DIGITS)
                self.assertEqual(dorig, dpar)
        self.assertEqual(pnw.name, self.nw.name)
        self.assertEqual(pnw.id, self.nw.id)
        for k, v in pnw.annotations.items():
            self.assertEqual(v, self.nw.annotations[k])
            
    def test_nyd(self):
        pnw = io.loads("nyd", io.dumps("nyd", self.nw))
        for hap0 in pnw:
            self.assertTrue(hap0 in self.nw)
            for hap1 in pnw:
                dorig = round(self.nw.distance(hap0, hap1), DIGITS)
                dpar = round(pnw.distance(hap0, hap1), DIGITS)
                self.assertEqual(dorig, dpar)
        self.assertEqual(pnw.name, self.nw.name)
        self.assertEqual(pnw.id, self.nw.id)
        for k, v in pnw.annotations.items():
            self.assertEqual(v, self.nw.annotations[k])
    
    def test_xml(self):
        pnw = io.loads("nxd", io.dumps("nxd", self.nw))
        for hap0 in pnw:
            self.assertTrue(hap0 in self.nw)
            for hap1 in pnw:
                dorig = round(self.nw.distance(hap0, hap1), DIGITS)
                dpar = round(pnw.distance(hap0, hap1), DIGITS)
                self.assertEqual(dorig, dpar)
        self.assertEqual(pnw.name, self.nw.name)
        self.assertEqual(pnw.id, self.nw.id)
        for k, v in pnw.annotations.items():
            self.assertEqual(v, self.nw.annotations[k])
    
    
#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    for _ in xrange(1000):
        unittest.main()


