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

from yatel import qbj, stats, dom
from yatel.tests.core import YatelTestCase


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class ValidateFunctionTest(YatelTestCase):

    def setUp(self):
        pass

    def _test_validquery(self):
        valid_query = {
            "id": 1545454845,
            "function": {
                "name": "haplotype_by_id",
                "args": [
                    {"type": 12},
                    {
                        "type": "integer",
                        "function": {
                            "name": "slice",
                            "kwargs": {
                                "iterable": {"type": "string", "value": "id_21_"},
                                "f": {"type": "integer", "value": "-1"},
                                "t": {"type": "integer", "value": "-3"}
                            }
                        }
                    }
                ]
            }
        }
        qbj.validate(valid_query)


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
            "varQ": {
                "cto": lambda *a, **k: stats.varQ(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "variation": {
                "cto": lambda *a, **k: stats.variation(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "Q": {
                "cto": lambda *a, **k: stats.Q(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "TRI": {
                "cto": lambda *a, **k: stats.TRI(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "MID": {
                "cto": lambda *a, **k: stats.MID(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "MD": {
                "cto": lambda *a, **k: stats.MD(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "MeD": {
                "cto": lambda *a, **k: stats.MeD(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "MAD": {
                "cto": lambda *a, **k: stats.MAD(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "H3_kelly": {
                "cto": lambda *a, **k: stats.H3_kelly(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "H1_yule": {
                "cto": lambda *a, **k: stats.H1_yule(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "Sp_pearson": {
                "cto": lambda *a, **k: stats.Sp_pearson(self.nw, *a, **k),
                "kwargs": {"place": "Mordor", "native": True}
            },
            "K1_kurtosis": {
                "cto": lambda *a, **k: stats.K1_kurtosis(self.nw, *a, **k),
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
# TYPE TESTS
#===============================================================================

class TypeTest(YatelTestCase):

    def test_all_types(self):
        now = datetime.datetime.now()
        comps = {
            "boolean": {"original": True, "to_parse": "true"},
            "string": {"original": u"asi", "to_parse": "asi"},
            "integer": {"original": 10, "to_parse": "10"},
            "array": {"original": [1], "to_parse": "[1]"},
            "float": {"original": 23.0, "to_parse": 23},
            "null": {"original": None, "to_parse": ""},
            "complex": {"original": 1+2j, "to_parse": "1+2j"},
            "datetime": {"original": now, "to_parse": now.isoformat()},
            "time": {"original": now.time(), "to_parse": now.time().isoformat()},
            "date": {"original": now.date(), "to_parse": now.date().isoformat()},
            "object": {"original": {'1':2}, "to_parse": '{"1":2}'},
            "haplotype": {"original": dom.Haplotype(1, a=2), "to_parse": {"hap_id": 1, "a": 2}},
            "fact": {"original": dom.Fact(1, a=2), "to_parse": {"hap_id": 1, "a": 2}},
            "edge": {"original": dom.Edge(1, 2, 3), "to_parse": [1,2,3]},
        }
        for tname in qbj.TYPES.keys():
            self.assertIn(tname, comps,
                          "QBJ Type '{}' not tested".format(tname))
        for tname, tdata in comps.items():
            original = tdata["original"]
            to_parse = tdata["to_parse"]
            oparsed = qbj.cast(original, tname)
            tpparsed = qbj.cast(to_parse, tname)
            valuate = original == oparsed == tpparsed
            msg = "Diferences in: {}|{}|{}".format(original, oparsed, tpparsed)
            self.assertTrue(valuate, msg)

#===============================================================================
# QBJ
#===============================================================================

class QBJEngineTest(YatelTestCase):

    def setUp(self):
        super(QBJEngineTest, self).setUp()
        self.jnw = qbj.QBJEngine(self.nw)

    def test_valid_queries(self):
        queries = [
            {'function': {'name': 'describe'}, 'id': 1, 'type': 'object'}
        ]
        for q in queries:
            asstring = json.dumps(q)
            asstream = StringIO.StringIO(asstring)
            self.jnw.execute_dict(q)



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
