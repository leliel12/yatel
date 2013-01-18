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
import urllib
import urllib2
import json
import datetime

import bottle

import yatel
from yatel import db, dom
from yatel.conversors import dict2yatel


#===============================================================================
# ERROR
#===============================================================================

class YatelRemoteError(Exception):

    def __init__(self, data):
        super(YatelRemoteError, self).__init__()
        self.data = data

    def __str__(self):
        return repr(self)

    def __repr__(self):
        msg = "<YatelRemoteError '{} - {}'>".format(self.remote_message,
                                                    self.remote_type)
        return msg

    @property
    def message(self):
        return self.data["error"]["message"]

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

    def __init__(self, connection, read_only=False, *args, **kwargs):
        super(YatelServer, self).__init__(*args, **kwargs)
        self._conn = connection
        self._read_only = read_only
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

    def call_fact_attributes_names(self):
        return list(self._conn.fact_attributes_names())

    def call_fact_attribute_values(self, att_name):
        return list(self._conn.fact_attribute_values(att_name))

    def call_minmax_edges(self):
        return map(dict2yatel.edge2dict, self._conn.minmax_edges())

    def call_filter_edges(self, minweight, maxweight):
        return map(dict2yatel.edge2dict,
                    self._conn.filter_edges(minweight, maxweight))

    def call_hap_sql(self, query):
        return map(dict2yatel.hap2dict, self._conn.hap_sql(query))

    def call_versions(self):
        return map(dict2yatel.version_descriptor2dict, self._conn.versions())

    def call_get_version(self, match=None):
        if match is not None and not isinstance(match, int):
            try:
                match = datetime.datetime.strptime(match, yatel.DATETIME_FORMAT)
            except ValueError:
                pass
        return dict2yatel.version2dict(self._conn.get_version(match))

    def call_save_version(self, tag, comment="", hap_sql="",
                           topology={}, weight_range=(None, None),
                           enviroments=()):
        topology = dict((self._conn.haplotype_by_id(k), v)
                         for k, v in topology.items())
        ver_desc = self._conn.save_version(tag, comment, hap_sql, topology,
                                           weight_range, enviroments)
        return dict2yatel.version_descriptor2dict(ver_desc)


#===============================================================================
# CLIENT
#===============================================================================

class YatelRemoteClient(object):
    """This class is used for conect to a remote instance of yatel

    """

    def __init__(self, host, port, protocol="http"):
        self._host = host
        self._port = port
        self._protocol = protocol
        self._url = "{protocol}://{host}:{port}/".format(protocol=protocol,
                                                          host=host,
                                                          port=port)
        self._call_url = "{}call".format(self._url)

    def _call(self, method, id=None, **kwargs):
        body = json.dumps({"id": id, "method": method, "arguments": kwargs})
        req = urllib2.Request(self._call_url, body,
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

    def fact_attributes_names(self, id=None):
        return iter(self._call("fact_attributes_names", id=id))

    def fact_attribute_values(self, att_name, id=None):
        return iter(self._call("fact_attribute_values",
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

    def versions(self, id=None):
        return iter(dict2yatel.dict2version_descriptor(e)
                      for e in self._call("versions", id=id))

    def get_version(self, match=None, id=None):
        if isinstance(match, datetime.datetime):
            match = match.strftime(yatel.DATETIME_FORMAT)
        return dict2yatel.dict2version(self._call("get_version",
                                                   id=id, match=match))

    def save_version(self, tag, comment="", hap_sql="", topology={},
                     weight_range=(None, None), enviroments=(), id=None):
        topology = dict((k.hap_id, v) for k, v in topology.items())
        ver_desc = self._call("save_version", tag=tag, comment=comment,
                             hap_sql=hap_sql, topology=topology,
                             weight_range=weight_range, enviroments=enviroments,
                             id=id)
        return ver_desc

    @property
    def name(self):
        return "REMOTE -> " + self._url

    @property
    def inited(self):
        return self.ping()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




