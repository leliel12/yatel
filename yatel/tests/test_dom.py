#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#===============================================================================
# DOC
#===============================================================================

"""yatel.dom module tests"""


#===============================================================================
# IMPORTS
#===============================================================================

import random

from yatel import dom
from yatel.tests.core import YatelTestCase


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class TestHaplatoype(YatelTestCase):

    def test_getattr(self):
        hap1 = dom.Haplotype(1, arg="fa")
        self.assertEquals("fa", hap1.arg)
        self.assertEquals("fa", hap1["arg"])
        self.assertEquals(hap1.arg, hap1["arg"])

    def test_eq(self):
        hap0 = dom.Haplotype(1)
        hap1 = dom.Haplotype(1, arg="foo")
        self.assertEquals(hap0, hap1)

    def test_ne(self):
        hap0 = dom.Haplotype(1)
        hap1 = dom.Haplotype(2)
        self.assertNotEqual(hap0, hap1)

    def test_hash(self):
        hap0 = dom.Haplotype(1)
        hap1 = dom.Haplotype(1, arg="foo")
        self.assertEquals(hash(hap0),hash(hap1))

    def test_is(self):
        hap0 = dom.Haplotype(1)
        hap1 = dom.Haplotype(1, arg="foo")
        self.assertFalse(hap0 is hap1)
        self.assertTrue(hap0 is hap0)
        self.assertTrue(hap1 is hap1)

    def test_in(self):
        hap0 = dom.Haplotype(1)
        hap1 = dom.Haplotype(1, attr="foo")
        hap2 = dom.Haplotype(2)
        d = {hap0: "foo"}
        self.assertIn(hap0, d)
        self.assertIn(hap1, d)
        self.assertNotIn(hap2, d)
        d.update({hap1: "faa", hap2: "fee"})
        self.assertEquals(d[hap0], "faa")
        self.assertEquals(d[hap1], "faa")
        self.assertEquals(d[hap2], "fee")
        self.assertEquals(len(d), 2)


    def test_none_values(self):
        hap0 = dom.Haplotype(1, attr=None)
        self.assertRaises(AttributeError, lambda: hap0.attr)

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
