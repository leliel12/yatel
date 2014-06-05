#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#===============================================================================
# DOC
#===============================================================================

"""yatel.yio package tests"""


#===============================================================================
# IMPORTS
#===============================================================================

import itertools

from yatel import yio, db
from yatel.tests.core import YatelTestCase


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class TestYio(YatelTestCase):

    def get_new_nw(self):
        return db.YatelNetwork("memory", mode="w")

    def test_synonyms(self):
        for syns in yio.SYNONYMS:
            generator = itertools.combinations_with_replacement(syns, 2)
            for parser0, parser1 in generator:
                dump0 = yio.dump(parser0, self.nw)
                dump1 = yio.dump(parser1, self.nw)
                self.assertEquals(dump0, dump1)

                nw0 = self.get_new_nw()
                nw1 = self.get_new_nw()

                yio.load(parser1, nw0, dump0)
                yio.load(parser0, nw1, dump1)
                nw0.confirm_changes()
                nw1.confirm_changes()

                self.assertEquals(self.nw.describe(), nw0.describe())
                self.assertEquals(self.nw.describe(), nw1.describe())
                self.assertEquals(nw0.describe(), nw1.describe())

    def test_crossed_formats(self):
        for parser0 in yio.PARSERS.keys():
            for parser1 in yio.PARSERS.keys():
                dump0 = yio.dump(parser0, self.nw)
                dump1 = yio.dump(parser1, self.nw)

                nw0 = self.get_new_nw()
                nw1 = self.get_new_nw()

                yio.load(parser0, nw0, dump0)
                yio.load(parser1, nw1, dump1)
                nw0.confirm_changes()
                nw1.confirm_changes()

                self.assertEquals(self.nw.describe(), nw0.describe())
                self.assertEquals(self.nw.describe(), nw1.describe())
                self.assertEquals(nw0.describe(), nw1.describe())



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
