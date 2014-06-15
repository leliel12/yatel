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
# VALIDATE TESTS
#==============================================================================

class TestDBFunctions(YatelTestCase):

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

    def test_copy(self):
        anw = db.YatelNetwork(engine="memory", mode=db.MODE_WRITE)
        db.copy(self.nw, anw)
        anw.confirm_changes()
        for method in ["haplotypes", "facts", "edges"]:
            nw_values = getattr(self.nw, method)()
            anw_values = getattr(anw, method)()
            self.assertSameUnsortedContent(nw_values, anw_values)
        self.assertEquals(self.nw.describe(), anw.describe())

    def test_parse_uri(self):
        for mode in db.MODES:
            for log in [True, False]:
                parsed = db.parse_uri(
                    "engine://user:password@host:666/db", mode=mode, log=log
                )
                self.assertEquals(parsed["engine"], "engine")
                self.assertEquals(parsed["host"], "host")
                self.assertEquals(parsed["port"], 666)
                self.assertEquals(parsed["user"], "user")
                self.assertEquals(parsed["password"], "password")
                self.assertEquals(parsed["mode"], mode)
                self.assertEquals(parsed["log"], log)

    def test_to_uri(self):
        for eng in db.ENGINES:
            for mode in db.MODES:
                for log in [True, False]:
                    conf = dict(
                        (k, "foo") for k in db.ENGINE_VARS[eng]
                    )
                    conf["mode"] = mode
                    conf["log"] = log
                    if "port" in conf:
                        conf["port"] = 666

                    orig = string.Template(
                        db.ENGINE_URIS[eng]
                    ).safe_substitute(engine=eng, **conf)
                    uri = db.to_uri(engine=eng, **conf)
                    self.assertEquals(orig, uri)

    def test_exists(self):
        try:
            fd, ftemp = tempfile.mkstemp()
            self.assertFalse(db.exists("sqlite", database=ftemp))
        except:
            raise
        finally:
            os.close(fd)
        try:
            fd, ftemp = tempfile.mkstemp()
            self.get_random_nw({"engine": "sqlite", "database": ftemp})
            self.assertTrue(db.exists("sqlite", database=ftemp))
        except:
            raise
        finally:
            os.close(fd)

    def test_qfilter(self):
        query = list(
            db.qfilter(self.nw.haplotypes(), lambda hap: hap.get("age") == 200)
        )
        self.assertEquals(len(query), 1)
        self.assertEquals(query[0].hap_id, 0)


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

    def add_element(self):
        haplotypes = [
            dom.Haplotype(0, name="Cordoba", clima="calor", age=200),
            dom.Haplotype(1, name="Cordoba", population=12),
            dom.Haplotype(2, name="Cordoba")
        ]
        edges = [
            dom.Edge(6599, (0, 1)),
            dom.Edge(8924, (1, 2)),
            dom.Edge(9871, (2, 0))
        ]
        facts = [
            dom.Fact(0, name="Andalucia", lang="sp", timezone="utc-3"),
            dom.Fact(1, lang="sp"),
            dom.Fact(1, timezone="utc-6"),
            dom.Fact(2, name="Andalucia", lang="sp", timezone="utc")
        ]
        nw = db.YatelNetwork("memory", mode="w")
        for cont in [haplotypes, edges, facts]:
            for elem in cont:
                self.nw.add_element(elem)
        self.nw.confirm_changes()
        self.assertEquals(nw.describe(), self.nw.describe())
        self.assertSameUnsortedContent(nw.haplotypes(), self.nw.haplotypes())
        self.assertSameUnsortedContent(nw.facts(), self.nw.facts())
        self.assertSameUnsortedContent(nw.edges(), self.nw.edges())
        self.assertSameUnsortedContent(nw.enviroments(), self.nw.enviroments())

    def test_add_elements(self):
        # indirectly tested
        pass

    def test_confirm_changes(self):
        # indirectly tested
        pass

    def test_edges_by_enviroment(self):
        rs = list(self.nw.edges_by_enviroment(name="Andalucia"))
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0], self.edges[2])

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





#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
