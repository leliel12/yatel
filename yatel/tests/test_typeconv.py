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

from yatel import typeconv
from yatel.tests.core import YatelTestCase


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class TestTypeConvFunctions(YatelTestCase):

    def test_verify_bidirection(self):
        c0 = typeconv.TO_SIMPLE_TYPES.keys()
        c1 = typeconv.TO_PYTHON_TYPES.keys()
        c0.sort()
        c1.sort()
        self.assertEquals(c0, c1)

    def test_simplifier(self):
        generators = (
            [self.nw.describe()],
            self.nw.enviroments(),
            self.nw.haplotypes(),
            self.nw.facts(),
            self.nw.edges()
        )
        for gen in generators:
            for thing in gen:
                typeconv.simplifier(thing)

    def test_parse(self):
        generators = (
            [self.nw.describe()],
            self.nw.enviroments(),
            self.nw.haplotypes(),
            self.nw.facts(),
            self.nw.edges()
        )
        for gen in generators:
            for thing in gen:
                simplified = typeconv.simplifier(thing)
                regenerated = typeconv.parse(simplified)
                self.assertEquals(thing, regenerated)

    def test_ignore(self):
        generators = (
            [self.nw.describe()],
            self.nw.enviroments(),
            self.nw.haplotypes(),
            self.nw.facts(),
            self.nw.edges()
        )
        for gen in generators:
            for thing in gen:
                simplified = typeconv.simplifier(thing)
                simplified["type"] = typeconv.LITERAL_TYPE
                regenerated = typeconv.parse(simplified)
                self.assertNotEquals(thing, regenerated)
                self.assertEquals(simplified["value"], regenerated)




#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
