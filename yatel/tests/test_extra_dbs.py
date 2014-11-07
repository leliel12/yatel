#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#==============================================================================
# DOC
#==============================================================================

"""yatel.db module tests"""


#==============================================================================
# IMPORTS
#==============================================================================

import os
import random
import string
import tempfile

from yatel import db, dom

from yatel.tests.core import YatelTestCase


#==============================================================================
# NETWORK
#==============================================================================

class YatelExtraDBTestTemplate(object):

    CONN_STR = ""

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
        self.nw = db.YatelNetwork(self.CONN_STR, mode="w")
        self.nw.add_elements(self.haplotypes + self.edges + self.facts)
        self.nw.confirm_changes()

    def test_edges(self):
        self.assertSameUnsortedContent(self.nw.edges(), self.edges)

    def test_haplotypes(self):
        self.assertSameUnsortedContent(self.nw.haplotypes(), self.haplotypes)

    def test_facts(self):
        self.assertSameUnsortedContent(self.nw.facts(), self.facts)

    def test_describe(self):
        desc = self.nw.describe()
        self.assertEquals(desc["mode"], db.MODE_READ)
        self.assertEquals(desc["size"]["facts"], len(self.facts))
        self.assertEquals(desc["size"]["edges"], len(self.edges))
        self.assertEquals(desc["size"]["haplotypes"], len(self.haplotypes))
        for a, t in desc["haplotype_attributes"].items():
            for hap in self.haplotypes:
                if a in hap:
                    self.assertTrue(isinstance(hap[a], t))
        for a, t in desc["fact_attributes"].items():
            for fact in self.facts:
                if a in fact:
                    self.assertTrue(isinstance(fact[a], t))
        max_nodes = desc["edge_attributes"]["max_nodes"]
        wt = desc["edge_attributes"]["weight"]
        for edge in self.edges:
            self.assertTrue(len(edge.haps_id) <= max_nodes)
            self.assertTrue(isinstance(edge.weight, wt))

    def test_edges_by_environment(self):
        rs = self.nw.edges_by_environment(name="Andalucia")
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0], self.edges[2])

    def test_facts_by_environment(self):
        rs = self.nw.facts_by_environment(name="Andalucia")
        orig = [self.facts[0], self.facts[3]]
        self.assertEqual(len(rs), 2)
        self.assertSameUnsortedContent(rs, orig)

    def test_haplotypes_by_environment(self):
        rs = self.nw.haplotypes_by_environment(name="Andalucia")
        self.assertEqual(len(rs), 2)
        self.assertEqual(rs[0], self.haplotypes[0])
        self.assertEqual(rs[1], self.haplotypes[2])

    def test_environments(self):
        desc = self.nw.describe()
        fact_attrs = desc["fact_attributes"].keys()
        for size in xrange(0, len(fact_attrs)):
            filters = set()
            while len(filters) < size:
                f = random.choice(fact_attrs)
                if f != "hap_id":
                    filters.add(f)
            response = self.nw.environments(list(filters))
            self.assertEquals(len(response), len(list(response)))

    def test_edges_by_haplotype(self):
        for hap in self.haplotypes:
            response = self.nw.edges_by_haplotype(hap)
            self.assertEquals(len(response), len(list(response)))
            for edge in response:
                self.assertIn(hap.hap_id, edge.haps_id)

    def test_facts_by_haplotype(self):
        for hap in self.haplotypes:
            response = self.nw.facts_by_haplotype(hap)
            self.assertEquals(len(response), len(list(response)))
            for fact in response:
                self.assertEquals(hap.hap_id, fact.hap_id)

    def test_haplotype_by_id(self):
        for hap in self.haplotypes:
            self.assertEquals(hap, self.nw.haplotype_by_id(hap.hap_id))

    def test_execute(self):
        rs = self.nw.execute("select * from {}".format(db.HAPLOTYPES))
        for row in rs:
            hap = self.nw.haplotype_by_id(row.hap_id)
            for k, v in row.items():
                if k in hap:
                    self.assertEquals(v, hap[k])
                else:
                    self.assertEquals(v, None)

    def test_uri(self):
        self.assertEquals(self.nw.uri, self.CONN_STR)

#==============================================================================
# CREATE CLASSES
#==============================================================================

def create_test_for(extra_dbs):
    extra_tests_dbs = {}
    for idx, conn_str in enumerate(extra_dbs):
        conn_str = conn_str.strip()
        if conn_str:
            data = db.parse_uri(conn_str)
            engine = data["engine"]
            database = data.get("database", "")
            cls_name = "YatelExtraDB{}{}{}".format(
                engine.title(), database.title(), idx
            ).replace("sql", "SQL")
            Cls = type(
                cls_name,
                (YatelExtraDBTestTemplate, YatelTestCase),
                {"CONN_STR": conn_str}
            )
            extra_tests_dbs[cls_name] = Cls
    return extra_tests_dbs


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
