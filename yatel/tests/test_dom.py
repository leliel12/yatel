#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

# ===============================================================================
# DOC
# ===============================================================================

"""yatel.dom module tests"""


# ===============================================================================
# IMPORTS
# ===============================================================================

from yatel import dom
from yatel.tests.core import YatelTestCase


# ===============================================================================
# VALIDATE TESTS
# ===============================================================================

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
        self.assertEquals(hash(hap0), hash(hap1))

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


class TestFact(YatelTestCase):
    def test_getattr(self):
        fact1 = dom.Fact(1, attr0="fac")
        self.assertEquals("fac", fact1.attr0)
        self.assertEquals("fac", fact1["attr0"])
        self.assertEquals(fact1.attr0, fact1["attr0"])

    def test_eq(self):
        fact0 = dom.Fact(1, attr0="fac")
        fact1 = dom.Fact(1, attr0="fac")
        self.assertEquals(fact0, fact1)

    def test_ne(self):
        fact0 = dom.Fact(1, attr0="fac", attr1="fact")
        fact1 = dom.Fact(2, attr0="fac", attr1="fact")
        self.assertNotEqual(fact0, fact1)

    def test_hash(self):
        fact0 = dom.Fact(1)
        fact1 = dom.Fact(1)
        self.assertEquals(hash(fact0), hash(fact1))

    def test_is(self):
        fact0 = dom.Fact(1)
        fact1 = dom.Fact(1, attr0="foo")
        self.assertFalse(fact0 is fact1)
        self.assertTrue(fact0 is fact0)
        self.assertTrue(fact1 is fact1)

    def test_in(self):
        fact0 = dom.Fact(1)
        fact1 = dom.Fact(1, attr0="foo")
        fact2 = dom.Fact(2)
        d = {fact0: "foo"}
        self.assertIn(fact0, d)
        self.assertNotIn(fact1, d)
        self.assertNotIn(fact2, d)
        d.update({fact1: "faa", fact2: "fee"})
        self.assertEquals(d[fact0], "foo")
        self.assertEquals(d[fact1], "faa")
        self.assertEquals(d[fact2], "fee")
        self.assertEquals(len(d), 3)

    def test_none_values(self):
        fact1 = dom.Fact(1, attr0="foo", attr1=None)
        self.assertRaises(AttributeError, lambda: fact1.attr1)

# ===============================================================================
# MAIN
# ===============================================================================

if __name__ == "__main__":
    print(__doc__)
