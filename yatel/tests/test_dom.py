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

from yatel import dom
from yatel.tests.core import YatelTestCase


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class TestHaplatoype(YatelTestCase):

    def test_getattr(self):
        pass

    def test_eq(self):
        hap0 = dom.Haplotype(1)
        hap1 = dom.Haplotype(1, arg="foo")
        self.assertEquals(hap0, hap1)

    def test_ne(self):
        pass

    def test_hash(self):
        pass

    def test_is(self):
        pass

    def test_in(self):
        pass

    def test_none_values(self):
        pass


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
