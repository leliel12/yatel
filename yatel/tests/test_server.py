#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#===============================================================================
# DOC
#===============================================================================

"""yatel.server module tests"""


#===============================================================================
# IMPORTS
#===============================================================================

import random

from yatel import server
from yatel.tests.core import YatelTestCase


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class TestYatelHttpServer(YatelTestCase):

    def setUp(self):
        super(TestYatelHttpServer, self).setUp()
        self.server = server.YatelHttpServer()
        self.client = self.server.test_client()
        self.server.add_nw("testnw", self.nw, enable_qbj=True)

    def test_query(self):
        pass



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
