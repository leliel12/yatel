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

import random, json

from yatel import server
from yatel.tests.core import YatelTestCase
from yatel.tests import queries


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class TestYatelHttpServer(YatelTestCase):

    def setUp(self):
        super(TestYatelHttpServer, self).setUp()
        self.testnw = "testnw"
        self.server = server.YatelHttpServer(DEBUG=True)
        self.server.add_nw(self.testnw, self.nw, enable_qbj=True)
        self.client = self.server.test_client()

    def test_ping(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_qbj(self):
        for query in queries.VALID:
            data = json.dumps(query)
            response = self.client.get('/qbj/{}'.format(self.testnw), data=data)




#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
