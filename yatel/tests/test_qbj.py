#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#===============================================================================
# DOC
#===============================================================================

"""yatel.qbj package tests"""


#===============================================================================
# IMPORTS
#===============================================================================

import random, datetime, json, StringIO

import jsonschema

from yatel import qbj, stats, dom, typeconv
from yatel.tests.core import YatelTestCase
from yatel.tests import queries


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class _ValidateFunctionTest(YatelTestCase):

    def setUp(self):
        pass

    def _test_validquery(self):
        for query in queries.VALID:
            qbj.validate(query)


#===============================================================================
# QBJ TEST
#===============================================================================

class FunctionTest(YatelTestCase):

    def setUp(self):
        super(FunctionTest, self).setUp()
        self.wrapped = qbj.wrap_network(self.nw)

    def test_all_functions(self):
        comps = {

            # directly map to network
            "describe": {"cto": self.nw.describe},
            "enviroments": {"cto": self.nw.enviroments,
                            "precmp": list, "args": [["place", "native"]]},
            "haplotypes": {"cto": self.nw.haplotypes, "precmp": list},
            "haplotype_by_id": {"cto": self.nw.haplotype_by_id,
                                "args": [random.choice(self.haps_ids)]},
            "haplotypes_by_enviroment": {
                "cto": self.nw.haplotypes_by_enviroment, "precmp": list,
                "kwargs": {"place": "Mordor", "native": True}
            },

            "facts": {"cto": self.nw.facts, "precmp": list},
            "facts_by_haplotype": {
                "cto": self.nw.facts_by_haplotype, "precmp": list,
                "args": [self.nw.haplotype_by_id(random.choice(self.haps_ids))]
            },
            "facts_by_enviroment": {
                "cto": self.nw.facts_by_enviroment, "precmp": list,
                "kwargs": {"place": "Mordor", "native": True}
            },

            "edges": {"cto": self.nw.edges, "precmp": list},
            "edges_by_haplotype": {
                "cto": self.nw.edges_by_haplotype, "precmp": list,
                "args": [self.nw.haplotype_by_id(random.choice(self.haps_ids))]
            },
            "edges_by_enviroment": {
                "cto": self.nw.edges_by_enviroment, "precmp": list,
                "kwargs": {"place": "Mordor", "native": True}
            },

            # stats
            "amin": {
                "cto": lambda *a, **k: stats.amin(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "amax": {
                "cto": lambda *a, **k: stats.amax(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "average": {
                "cto": lambda *a, **k: stats.average(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "env2weightarray": {
                "cto": lambda *a, **k: stats.env2weightarray(self.nw, *a, **k),
                "precmp": list, "kwargs": {"place": "Mordor", "native": True}
            },
            "kurtosis": {
                "cto": lambda *a, **k: stats.kurtosis(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "min": {
                "cto": lambda *a, **k: stats.min(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "median": {
                "cto": lambda *a, **k: stats.median(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "max": {
                "cto": lambda *a, **k: stats.max(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "mode": {
                "cto": lambda *a, **k: stats.mode(self.nw, *a, **k),
                "precmp": list, "kwargs": {"place": "Mordor", "native": True}
            },
            "percentile": {
                "cto": lambda *a, **k: stats.percentile(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True, "q": (25, 55, 60)}
            },
            "range": {
                "cto": lambda *a, **k: stats.range(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "std": {
                "cto": lambda *a, **k: stats.std(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "sum": {
                "cto": lambda *a, **k: stats.sum(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "var": {
                "cto": lambda *a, **k: stats.var(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "variation": {
                "cto": lambda *a, **k: stats.variation(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },


            # natives from qbj
            "slice": {"cto": lambda x, f, t: x[f:t],
                      "args": ["guilkmnbhgfyuiooijhg", 5, 8]},
            "ping": {"cto": lambda: True},
        }
        for impfunc in self.wrapped.keys():
            self.assertIn(impfunc, comps,
                          "QBJ Function '{}' not tested".format(impfunc))
        for fname, cmpdata in comps.items():
            cto = cmpdata["cto"]
            precmp = cmpdata.get("precmp", lambda x: x)
            args = cmpdata.get("args", ())
            kwargs = cmpdata.get("kwargs", {})
            qbjvalue = precmp(self.wrapped.evaluate(fname, args, kwargs))
            ctovalue = precmp(cto(*args, **kwargs))
            self.assertEquals(qbjvalue, ctovalue, "Failed '{}'".format(fname))

#===============================================================================
# QBJ
#===============================================================================

class QBJEngineTest(YatelTestCase):

    def setUp(self):
        super(QBJEngineTest, self).setUp()
        self.jnw = qbj.QBJEngine(self.nw)

    def test_valid_queries(self):
        for dictionary in queries.VALID:
            string = json.dumps(dictionary)
            stream = StringIO.StringIO(string)
            for q in [dictionary, string, stream]:
                result = self.jnw.execute(q, True)
                if isinstance(q, dict) and q["id"] == 1545454845:
                    import pprint;pprint.pprint(result)
                if result["error"]:
                    self.fail("\n".join(
                        [result["error_msg"], result["stack_trace"]])
                    )
                    print("\n".join(
                        [result["error_msg"], result["stack_trace"]])
                    )



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
