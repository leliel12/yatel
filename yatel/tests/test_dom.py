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


class TestEdge(YatelTestCase):

    def test_getattr(self):
        edge0 = dom.Edge(1, (1, 2))
        self.assertEquals((1, 2), edge0.haps_id)
        self.assertEquals((1, 2), edge0["haps_id"])
        self.assertEquals(edge0.haps_id, edge0["haps_id"])

    def test_eq(self):
        edge0 = dom.Edge(1, [1, 2])
        edge1 = dom.Edge(1, [1, 2])
        self.assertEquals(edge0, edge1)

    def test_ne(self):
        edge0 = dom.Edge(1, [1, 2])
        edge1 = dom.Edge(2, [1, 3])
        self.assertNotEqual(edge0, edge1)

    def test_hash(self):
        edge0 = dom.Edge(1, [1, 2])
        edge1 = dom.Edge(1, [1, 2])
        self.assertEquals(hash(edge0), hash(edge1))

    def test_is(self):
        edge0 = dom.Edge(1, [1, 2])
        edge1 = dom.Edge(2, [1, 3])
        self.assertFalse(edge0 is edge1)
        self.assertTrue(edge0 is edge0)
        self.assertTrue(edge1 is edge1)

    def test_in(self):
        edge0 = dom.Edge(1, [1, 2])
        edge1 = dom.Edge(1, [1, 4])
        edge2 = dom.Edge(2, [1, 3])
        d = {edge0: [1, 4]}
        self.assertIn(edge0, d)
        self.assertNotIn(edge1, d)
        self.assertNotIn(edge2, d)
        d.update({edge1: [1, 3], edge2: [1, 2]})
        self.assertEquals(d[edge0], [1, 4])
        self.assertEquals(d[edge1], [1, 3])
        self.assertEquals(d[edge2], [1, 2])
        self.assertEquals(len(d), 3)


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


class TestEnviroment(YatelTestCase):

    def test_getattr(self):
        enviroment1 = dom.Enviroment(attr0="env")
        self.assertEquals("env", enviroment1.attr0)
        self.assertEquals("env", enviroment1["attr0"])
        self.assertEquals(enviroment1.attr0, enviroment1["attr0"])

    def test_eq(self):
        enviroment0 = dom.Enviroment(attr0="fac")
        enviroment1 = dom.Enviroment(attr0="fac")
        self.assertEquals(enviroment0, enviroment1)

    def test_ne(self):
        enviroment0 = dom.Enviroment(attr0="fac")
        enviroment1 = dom.Enviroment()
        self.assertNotEqual(enviroment0, enviroment1)

    def test_hash(self):
        enviroment0 = dom.Enviroment()
        enviroment1 = dom.Enviroment()
        self.assertEquals(hash(enviroment0), hash(enviroment1))

    def test_is(self):
        enviroment0 = dom.Enviroment(attr0="fac")
        enviroment1 = dom.Enviroment()
        self.assertFalse(enviroment0 is enviroment1)
        self.assertTrue(enviroment0 is enviroment0)
        self.assertTrue(enviroment1 is enviroment1)

    def test_in(self):
        enviroment0 = dom.Enviroment(attr0="fac")
        enviroment1 = dom.Enviroment()
        enviroment2 = dom.Enviroment()
        d = {enviroment0}
        self.assertIn(enviroment0, d)
        self.assertNotIn(enviroment1, d)
        self.assertNotIn(enviroment2, d)
        self.assertEquals(len(d), 1)

    def test_none_values(self):
        enviroment1 = dom.Enviroment(attr0=None)
        self.assertEquals(enviroment1.attr0, None)


# ===============================================================================
# MAIN
# ===============================================================================

if __name__ == "__main__":
    print(__doc__)
