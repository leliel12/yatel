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

from yatel import db, dom
from yatel.tests.core import YatelTestCase


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class TestFunctions(YatelTestCase):

    def test_to_simple_types(self):
        generators = (
            [self.nw.describe()],
            self.nw.enviroments(),
            self.nw.haplotypes(),
            self.nw.facts(),
            self.nw.edges()
        )
        for gen in generators:
            for thing in gen:
                self.assertEquals(
                    thing.as_simple_dict(), dom.to_simple_type(thing)
                )


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
