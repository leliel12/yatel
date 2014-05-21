#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#===============================================================================
# DOC
#===============================================================================

"""yatel.db module tests"""


#===============================================================================
# IMPORTS
#===============================================================================

import random

from yatel import db, dom

from yatel.tests.core import YatelTestCase


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class TestDBFunctions(YatelTestCase):

    def test_enviroments(self):
        desc = self.nw.describe()
        fact_attrs = desc["fact_attributes"].keys()
        for size in xrange(0, len(fact_attrs)):
            filters = set()
            while len(filters) < size:
                f = random.choice(fact_attrs)
                if f != "hap_id":
                    filters.add(f)
            list(self.nw.enviroments(list(filters)))

    def test_copy(self):
        anw = db.YatelNetwork(engine="memory", mode=db.MODE_WRITE)
        db.copy(self.nw, anw)
        anw.confirm_changes()
        for method in ["haplotypes", "facts", "edges"]:
            nw_values = getattr(self.nw, method)()
            anw_values = getattr(anw, method)()
            self.assertSameUnsortedContent(nw_values, anw_values)
        self.assertEquals(self.nw.describe(), anw.describe())


#==============================================================================
# NETWORK
#==============================================================================

class YatelNetwork(YatelTestCase):

    def setUp(self):
        self.haplotypes = [
            dom.Haplotype(0, name="Cordoba", clima="calor", age=200),
            dom.Haplotype(1, name="Cordoba", population=12),
            dom.Haplotype(2, name="Cordoba")
        ]
        self.edges = [
            dom.Edge(6599, (0, 1)),
            dom.Edge(8924, (1, 2)),
            dom.Edge(9871, (2, 0))
        ]
        self.facts = [
            dom.Fact(0, name="Andalucia", lang="sp", timezone="utc-3"),
            dom.Fact(1, lang="sp"),
            dom.Fact(1, timezone="utc-6"),
            dom.Fact(2, name="Andalucia", lang="sp", timezone="utc")
        ]
        self.nw = db.YatelNetwork("memory", mode="w")
        self.nw.add_elements(self.haplotypes + self.edges + self.facts)
        self.nw.confirm_changes()

    def test_edges_by_enviroment(self):
        rs = list(self.nw.edges_by_enviroment(name="Andalucia"))
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0], self.edges[2])







#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
