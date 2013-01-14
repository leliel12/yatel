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
import urllib2
import json

import bottle

import yatel
from yatel import db, dom
from yatel.conversors import dict2yatel


#===============================================================================
# ERROR
#===============================================================================

class YatelRemoteError(BaseException):

    def __init__(self, data):
        super(YatelRemoteError, self).__init__()
        self.data = data

    def __repr__(self):
        msg = "<YatelRemoteError '{} - {}'>".format(self.remote_message,
                                                     self.remote_type)
        return msg

    @property
    def method(self):
        return self.data["method"]

    @property
    def call_id(self):
        return self.data["id"]

    @property
    def remote_message(self):
        return self.data["error"]["message"]

    @property
    def remote_type(self):
        return self.data["error"]["type"]


#===============================================================================
# SERVER
#===============================================================================

class YatelServer(bottle.Bottle):
    """

    """

    def __init__(self, connection, *args, **kwargs):
        super(YatelServer, self).__init__(*args, **kwargs)
        self._conn = connection
        self.post("/call", callback=self._call)

    def _call(self):
        id = None
        method = None
        try:
            data = bottle.request.json
            id = data["id"]
            method = data["method"]
            arguments = data["arguments"]
            internal_method = "call_{}".format(method)
            if hasattr(self, internal_method):
                response = getattr(self, internal_method)(**arguments)
                return {"id": id, "method": method, "response": response}
            else:
                msg = "No method '{}'".format(method)
                raise AttributeError(msg)
        except Exception as err:
            return {"id":id, "method": method,
                     "error": {"message": str(err),
                               "type": type(err).__name__}}

    def run(self, host, port, *args, **kwargs):
        super(YatelServer, self).run(host=host, port=int(port),
                                      *args, **kwargs)

    def call_ping(self):
        return True

    def call_iter_haplotypes(self):
        return map(dict2yatel.hap2dict, self._conn.iter_haplotypes())

    def call_iter_edges(self):
        return map(dict2yatel.edge2dict, self._conn.iter_edges())

    def call_iter_facts(self):
        return map(dict2yatel.fact2dict, self._conn.iter_facts())

    def call_haplotype_by_id(self, hap_id):
        return dict2yatel.hap2dict(self._conn.haplotype_by_id(hap_id))

    def call_enviroment(self, **env):
        return map(dict2yatel.hap2dict, self._conn.enviroment(**env))

    def call_facts_attributes_names(self):
        return self._conn.facts_attributes_names()

    def call_fact_attribute_values(self, att_name):
        return self._conn.fact_attribute_values(att_name)

    def call_minmax_edges(self):
        return map(dict2yatel.edge2dict, self._conn.minmax_edges())

    def call_filter_edges(self, minweight, maxweight):
        return map(dict2yatel.edge2dict,
                    self._conn.filter_edges(minweight, maxweight))

    def call_hap_sql(self, query):
        return map(dict2yatel.hap2dict, self._conn.hap_sql(query))


#===============================================================================
# CLIENT
#===============================================================================

class YatelClient(object):
    """This class is used for conect to a remote instance of yatel

    """

    def __init__(self, host, port, protocol="http"):
        self._host = host
        self._port = port
        self._protocol = protocol
        self._url = "{protocol}://{host}:{port}/call".format(protocol=protocol,
                                                              host=host,
                                                              port=port)
    def _call(self, method, id=None, **kwargs):
        body = json.dumps({"id": id, "method": method, "arguments": kwargs})
        req = urllib2.Request(self._url, body,
                              {'Content-Type': 'application/json'})
        data = json.load(urllib2.urlopen(req))
        if "error" in data:
            raise YatelRemoteError(data)
        else:
            return data["response"]

    def ping(self, id=None):
        return self._call(method="ping", id=id)

    def iter_haplotypes(self, id=None):
        for e in self._call("iter_haplotypes", id=id):
            yield dict2yatel.dict2hap(e)

    def iter_facts(self, id=None):
        for e in self._call("iter_facts", id=id):
            yield dict2yatel.dict2fact(e)

    def iter_edges(self, id=None):
        for e in self._call("iter_edges", id=id):
            yield dict2yatel.dict2edge(e)

    def haplotype_by_id(self, hap_id, id=None):
        return dict2yatel.dict2hap(self._call("haplotype_by_id",
                                               id=id, hap_id=hap_id))

    def enviroment(self, id=None, **env):
        for e in self._call("enviroment", id=id, **env):
            yield dict2yatel.dict2hap(e)

    def facts_attributes_names(self, id=None):
        return tuple(self._call("facts_attributes_names", id=id))

    def fact_attribute_values(self, att_name, id=None):
        return tuple(self._call("fact_attribute_values",
                                  att_name=att_name, id=id))

    def minmax_edges(self, id=None):
        return tuple(dict2yatel.dict2edge(e)
                       for e in self._call("minmax_edges", id=id))

    def filter_edges(self, minweight, maxweight, id=None):
        for e in self._call("filter_edges", id=id,
                             minweight=minweight, maxweight=maxweight):
            yield dict2yatel.dict2edge(e)

    def hap_sql(self, query, id=None):
        for e in self._call("hap_sql", id=id, query=query):
            yield dict2yatel.dict2hap(e)


if __name__ == "__main__":
    conn = YatelClient("localhost", 8080)
    print conn.facts_attributes_names()
    print conn.fact_attribute_values("k")
    print conn.minmax_edges()
    print list(conn.filter_edges(1, 40))
    print list(conn.hap_sql("select * from haplotypes where hap_id = 'haplotype_22'"))


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




