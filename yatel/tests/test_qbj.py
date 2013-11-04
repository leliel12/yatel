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

import random

import jsonschema

from yatel import qbj, stats
from yatel.tests.core import YatelTestCase


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class ValidateFunctionTest(YatelTestCase):

    def setUp(self):
        pass

    def test_validquery(self):
        valid_query = {
            "id": 1545454845,
            "function": {
                "name": "haplotype_by_id",
                "args": [
                    {
                        "type": "int",
                        "function": {
                            "name": "slice",
                            "kwargs": {
                                "iterable": {"type": "str", "value": "id_21_"},
                                "f": {"type": "int", "value": "-1"},
                                "t": {"type": "int", "value": "-3"}
                            }
                        }
                    }
                ]
            }
        }
        qbj.validate(valid_query)

    def test_invalid_extra_property(self):
        invalid_query = {
            "id": 1545454845,
            "extra": "don't work",
            "function": {
                "name": "haplotypes_by",
                "args": [
                    {
                        "type": "int",
                        "function": {
                            "name": "slice",
                            "kwargs": {
                                "iterable": {"type": "str", "value": "id_21_"},
                                "f": {"type": "int", "value": "-1"},
                                "t": {"type": "int", "value": "-3"}
                            }
                        }
                    }
                ]
            }
        }
        self.assertRaises(jsonschema.ValidationError,
                          qbj.validate, invalid_query)


    def test_invalid_function_name(self):
        invalid_query = {
            "id": 1545454845,
            "function": {
                "name": "haplsdsdotypes_by",
                "args": [
                    {
                        "type": "int",
                        "function": {
                            "name": "slice",
                            "kwargs": {
                                "iterable": {"type": "str", "value": "id_21_"},
                                "f": {"type": "int", "value": "-1"},
                                "t": {"type": "int", "value": "-3"}
                            }
                        }
                    }
                ]
            }
        }
        self.assertRaises(jsonschema.ValidationError,
                          qbj.validate, invalid_query)




#===============================================================================
# QBJ TEST
#===============================================================================

class QBJsonTest(YatelTestCase):

    def setUp(self):
        super(QBJsonTest, self).setUp()
        self.nqbj = qbj.QBJson(self.nw)

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
                      "args": ["guilkmnbhgfyuiooijhg", 5, 8]}
        }
        for impfunc in self.nqbj.functions.keys():
            self.assertIn(impfunc, comps,
                          "QBJ Function '{}' not tested".format(impfunc))
        for fname, cmpdata in comps.items():
            cto = cmpdata["cto"]
            precmp = cmpdata.get("precmp", lambda x: x)
            args = cmpdata.get("args", ())
            kwargs = cmpdata.get("kwargs", {})
            qbjvalue = precmp(self.nqbj.functions[fname].func(*args, **kwargs))
            ctovalue = precmp(cto(*args, **kwargs))
            self.assertEquals(qbjvalue, ctovalue, "Failed '{}'".format(fname))






#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
