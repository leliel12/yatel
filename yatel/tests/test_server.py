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

import random, json, tempfile, os

from yatel import server, qbj
from yatel.tests.core import YatelTestCase


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
        self.jnw = qbj.QBJEngine(self.nw)


    def test_qbj(self):
        qid = random.randint(100, 200)
        query = {"id": qid, "function": {"name": "average"}}
        #~ data = json.dumps(query)
        #~ import ipdb; ipdb.set_trace()
        #~ response = self.client.get('/qbj/{}'.format(self.testnw), data=data)
        #~ self.assertEquals(response.status_code, 200)
        #~ self.assertEquals(json.loads(response.data),
                          #~ self.jnw.execute(query, True))



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
