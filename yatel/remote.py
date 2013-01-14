#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""A http server and client for a yatel conection.

**Warning** By default the yatel server not mange any security related features


"""


#===============================================================================
# IMPORT
#===============================================================================

import hashlib
import time
import urllib

import bottle

import yatel
from yatel import db, dom
from yatel.conversors import dict2yatel


#===============================================================================
# FACT
#===============================================================================

class YatelServer(bottle.Bottle):
    """

    """

    def __init__(self, connection, *args, **kwargs):
        super(YatelServer, self).__init__(*args, **kwargs)
        self._conn = connection

        self.post("/call", callback=self.call)

        """self.get("/ping", callback=self.ping)
        self.get("/iter_haplotypes", callback=self.iter_haplotypes)
        self.get("/iter_edges", callback=self.iter_edges)
        self.get("/iter_facts", callback=self.iter_facts)
        self.get("/haplotype_by_id", callback=self.haplotype_by_id)
        self.get("/enviroment", callback=self.enviroment)
        self.get("/facts_attributes_names", callback=self.facts_attributes_names)
        self.get("/fact_attribute_values", callback=self.fact_attribute_values)
        self.get("/minmax_edges", callback=self.minmax_edges)
        self.get("/filter_edges", callback=self.filter_edges)
        self.get("/hap_sql", callback=self.hap_sql)"""

    def run(self, host, port, *args, **kwargs):
        super(YatelServer, self).run(host=host, port=int(port), *args, **kwargs)

    def call(self):
        id = None
        method = None
        try:
            data = bottle.request.json
            id = data["id"]
            method = data["method"]
            arguments = data["arguments"]

            if method in PUBLIC_METHODS:
                pass

                return {"id": id, "method": method, "response": response}
        except Exception as err:
            return {
                "id":id, "method": method,
                "error": {
                    "message": str(err),
                    "type": type(err).__name__
                    }
                }

    def ping(self):
        return {yatel.PRJ: "PONG"}

    def iter_haplotypes(self):
        return map(dict2yatel.hap2dict, self._conn.iter_haplotypes())

    def iter_edges(self):
        return map(dict2yatel.edge2dict, self._conn.iter_edges())

    def iter_facts(self):
        return map(dict2yatel.fact2dict, self._conn.iter_facts())

    def haplotype_by_id(self, hap_id):
        return dict2yatel.hap2dict(self._conn.haplotype_by_id(hap_id))

    def enviroment(self, **env):
        return map(dict2yatel.hap2dict, self._conn.enviroment(**env))

    def facts_attributes_names(self):
        return self._conn.facts_attributes_names()

    def fact_attribute_values(self, att_name):
        return self._conn.fact_attribute_values(att_name)

    def minmax_edges(self):
        return map(dict2yatel.edge2dict, self._conn.minmax_edges())

    def filter_edges(self, minweight, maxweight):
        return map(dict2yatel.edge2dict,
                    self._conn.filter_edges(minweight, maxweight))

    def hap_sql(self, query):
        return map(dict2yatel.hap2dict, self._conn.hap_sql(query))


#===============================================================================
# CLIENT
#===============================================================================

class YatelClient(object):
    """This class is used for conect to a remote instance of yatel

    """

    def __init__(self, host, port):
        pass


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




