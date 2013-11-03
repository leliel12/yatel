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

from yatel.tests.core import YatelTestCase

from yatel import qbj


#===============================================================================
# BASE CLASS
#===============================================================================

class QBJsonTest(YatelTestCase):

    def setUp(self):
        super(QBJsonTest, self).setUp()
        self.nqbj = qbj.QBJson(self.nw)

    def test_all_functions(self):
        comps = {
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

            "slice": {"cto": lambda x, f, t: x[f:t],
                      "args": ["guilkmnbhgfyuiooijhg", 5, 8]}
        }
        for fname, cmpdata in comps.items():
            cto = cmpdata["cto"]
            precmp = cmpdata.get("precmp", lambda x: x)
            args = cmpdata.get("args", ())
            kwargs = cmpdata.get("kwargs", {})
            qbjvalue = precmp(self.nqbj.functions[fname].func(*args, **kwargs))
            ctovalue = precmp(cto(*args, **kwargs))
            self.assertEquals(qbjvalue, ctovalue)






#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
