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
        self.jnw = qbj.QBJEngine(self.nw)

    def test_ping(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_qbj(self):
        for query in queries.VALID:
            data = json.dumps(query)
            response = self.client.get('/qbj/{}'.format(self.testnw), data=data)
            self.assertEquals(response.status_code, 200)
            self.assertEquals(json.loads(response.data),
                              self.jnw.execute(query, True))


class TestYatelHttpServerFromDict(TestYatelHttpServer):

    def conn(self):
        self.fd, self.dbpath = tempfile.mkstemp("yatel_temp")
        return {"engine": "sqlite", "database": self.dbpath}

    def tearDown(self):
        os.close(self.fd)
        os.remove(self.dbpath)

    def setUp(self):
        super(TestYatelHttpServerFromDict, self).setUp()
        self.data = {
            "CONFIG": {"DEBUG": True},
            "NETWORKS": {
                self.testnw: {
                    "uri": self.nw.describe()["uri"],
                    "qbj": True,
                    "algo": "asi"
                }
            }
        }
        self.server = server.from_dict(self.data)
        self.client = self.server.test_client()


class TestFunctions(YatelTestCase):

    def setUp(self): pass

    def test_get_template(self):
        tpl = server.get_conf_template()
        self.assertEquals(json.loads(tpl), server.CONF_BASE)



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
