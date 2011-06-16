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
import datetime

from yatel import haps
from yatel import weights
from yatel import nd
from yatel import facts
from yatel import ndinfo
from yatel import util
from yatel import db


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
        d = weights.HammingWeight()
        self.assertEquals(d.weight_of(self.h0a, self.h0b), 0)
        self.assertEquals(d.weight_of(self.h1a, self.h1b), 0)
        self.assertEquals(d.weight_of(self.h1a, self.h0b), 2)
        self.assertEquals(d.weight_of(self.h1b, self.h0a), 2)
        
    def test_expert(self):
        # get random distances
        d0a0b = random.random()
        d0a1b = random.random()
        d1a0b = random.random()
        d1a1b = random.random()
        
        # create the expert
        d = weights.ExpertWeight()
        d.add_Weight(self.h0a, self.h0b, d0a0b)
        d.add_Weight(self.h0a, self.h1b, d0a1b)
        d.add_Weight(self.h1a, self.h0b, d1a0b)
        d.add_Weight(self.h1a, self.h1b, d1a1b)
        
        # test
        self.assertEquals(d.weight_of(self.h0a, self.h0b), d0a0b)
        self.assertEquals(d.weight_of(self.h0a, self.h1b), d0a1b)
        self.assertEquals(d.weight_of(self.h1a, self.h0b), d1a0b)
        self.assertEquals(d.weight_of(self.h1a, self.h1b), d1a1b)

        
#===============================================================================
# NETWORK TEST
#===============================================================================

class NetworkDescriptorTest(unittest.TestCase):
    
    def test_creation(self):
        self.haplotypes = [haps.Haplotype(str(name), **randomdict())
                           for name in randomrange(10, 100)]
        self.conn = set([(random.choice(self.haplotypes), random.choice(self.haplotypes))
                         for _ in randomrange(10, 50)])
        self.ann = randomdict()
        self.nw = nd.NetworkDescriptor(nwid=str(random.random),
                                       haplotypes=self.haplotypes,
                                       connectivity=self.conn,
                                       w_calculator=weights.LinkWeight(),
                                       annotations=self.ann)



#===============================================================================
# NETWORK INFO TEST
#===============================================================================

class NDInfoTest(unittest.TestCase):        
    
    def setUp(self):
        self.haplotypes = [haps.Haplotype(str(name), **randomdict())
                           for name in randomrange(10, 100)]
        self.conn = set([(random.choice(self.haplotypes), random.choice(self.haplotypes))
                         for _ in randomrange(10, 50)])
        self.ann = randomdict()
        self.nw = nd.NetworkDescriptor(nwid=str(random.random),
                                       haplotypes=self.haplotypes,
                                       connectivity=self.conn,
                                       w_calculator=weights.RandomWeight(),
                                       annotations=self.ann)
    
    
for fn in dir(ndinfo):
    f = getattr(ndinfo, fn)
    if not fn.startswith("_") and callable(f):
        test_func = lambda self: f(self.nw)
        setattr(NDInfoTest, "test_%s" % fn, test_func)
del fn


#===============================================================================
# NETWORK IO TEST
#===============================================================================

class UtilTest(unittest.TestCase):
    
    def test_string_parser(self):
        parser = util.StringParser(
            int=(unicode, int),
            float=(unicode, float),
            bool=(unicode, lambda v: v == "True"),
            str=(unicode, str),
            unicode=(unicode, unicode),
            datetime=(unicode, 
                      lambda s: datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f"))
        )
        for _ in randomrange(100, 1000):
            datas = [random.randint(10, 2303), round(random.random(), 4), 
                     bool(random.randint(0, 1)), str(random.random),
                     unicode(random.random()), datetime.datetime.now()]
            while datas:
                data = datas.pop(random.randint(0, len(datas) - 1))
                pdata = parser.loads(type(data).__name__, parser.dumps(data))
                self.assertEquals(data, pdata)
                
#===============================================================================
# DB
#===============================================================================

class DBTest(unittest.TestCase):
    
    def test_connect(self):
        pass

#===============================================================================
# MAIN
#===============================================================================


if __name__ == "__main__":
    unittest.main()


