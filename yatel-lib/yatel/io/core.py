#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This module is used for construct yatel.db.YatelNetwork using natives
dictionaries. This is the most low level representation for trandformations to
another formats.

"""

#===============================================================================
# IMPORTS
#===============================================================================

import datetime
import copy
import decimal

import yatel
from yatel import dom, db


#===============================================================================
# CONSTANTS
#===============================================================================

VERSIONS = ("0.3",)

DEFAULT_VERSION = "0.3"

IO_TYPES = {
    datetime.datetime: lambda x: x.isoformat(),
    datetime.time: lambda x: x.isoformat(),
    datetime.date: lambda x: x.isoformat(),
    bool: lambda x: x,
    int: lambda x: x,
    float: lambda x: x,
    str: lambda x: x,
    unicode: lambda x: x,
    decimal.Decimal: lambda x: str(x)
}

PYTHON_TYPES = {
    datetime.datetime:
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f"),
    datetime.time:
        lambda x: datetime.datetime.strptime(s, "%H:%M:%S.%f").time(),
    datetime.date:
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date(),
    bool: lambda x: x,
    int: lambda x: x,
    float: lambda x: x,
    str: lambda x: x,
    unicode: lambda x: x,
    decimal.Decimal: lambda x: decimal.Decimal(x)
}


TYPES_NAMES = dict((k, k.__name__) for k in IO_TYPES.keys())

NAMES_TYPES = dict((v, k) for k, v in TYPES_NAMES.items())

#===============================================================================
# ERROR
#===============================================================================

class ParserError(Exception):
    pass


#===============================================================================
# CLASS
#===============================================================================

class BaseParser(object):

    def validate_read(self, nw):
        if not isinstance(nw, db.YatelNetwork) or not nw.created:
            msg = "load need a db.YatelNetwork instance created"
            raise ParserError(msg)

    def validate_write(self, nw):
        if not isinstance(nw, db.YatelNetwork) or nw.created:
            msg = "load need a db.YatelNetwork instance not created"
            raise ParserError(msg)

    def types2str(self, types):
        return dict((k, TYPES_NAMES[v]) for k, v in types.items())

    def str2types(self, types):
        return dict((k, NAMES_TYPES[v]) for k, v in types.items())

    def hap2dict(self, hap, hap_id_type, types):
        """Convert a ``dom.Haplotype`` instance into a dict"""
        hd = {"hap_id": IO_TYPES[hap_id_type](hap.hap_id)}
        for k, v in hap.items_attrs():
            atype = types[k]
            hd[k] = IO_TYPES[atype](v) if v is not None else None
        return hd

    def dict2hap(self, hapd, hap_id_type, types):
        """Convert a ``dict`` with haplotype data into a ``dom.Haplotype``
        instance

        """
        params = {}
        for k, v in hapd.items():
            atype = hap_id_type if k == "hap_id" else types[k]
            params[k] = PYTHON_TYPES[atype](v) if v is not None else None
        return dom.Haplotype(**params)

    def fact2dict(self, fact, hap_id_type, types):
        """Convert a ``dom.Fact`` instance into a dict"""

        fd = {"hap_id": IO_TYPES[hap_id_type](fact.hap_id)}
        for k, v in fact.items_attrs():
            atype = types[k]
            fd[k] = IO_TYPES[atype](v) if v is not None else None
        return fd

    def dict2fact(self, factd, hap_id_type, types):
        """Convert a ``dict`` with Fact data into a ``dom.Fact``
        instance

        """
        params = {}
        for k, v in factd.items():
            atype = hap_id_type if k == "hap_id" else types[k]
            params[k] = PYTHON_TYPES[atype](v) if v is not None else None
        return dom.Fact(**params)

    def edge2dict(self, edge, hap_id_type):
        """Convert a ``dom.Edge`` instance into a dict"""
        ed = {"weight": edge.weight}
        haps_ids = []
        for v in edge.haps_id:
            v = IO_TYPES[hap_id_type](v) if v is not None else None
            haps_ids.append(v)
        ed["haps_id"] = haps_ids
        return ed

    def dict2edge(self, edged, hap_id_type):
        """Convert a ``dict`` with Edge data into a ``dom.Edge``
        instance

        """
        haps_ids = []
        for v in edged["haps_id"]:
            v = PYTHON_TYPES[hap_id_type](v) if v is not None else None
            haps_ids.append(v)
        return dom.Edge(edged["weight"], *haps_ids)

    #===========================================================================
    # MAIN METHODS
    #===========================================================================

    def dump(self, nw):
        """Convert dom objects into a dict with keys ``haplotypes``, ``facts``,
        and ``edgest``

        """
        self.validate_read(nw)
        hap_types = nw.haplotype_attributes_types()
        fact_types = nw.fact_attributes_types()
        hap_id_type = hap_types["hap_id"]
        return {
            "version": DEFAULT_VERSION,
            "types": {
                "haplotypes": self.types2str(hap_types),
                "facts": self.types2str(fact_types)
            },
            "haplotypes": [self.hap2dict(hap, hap_id_type, hap_types)
                           for hap in nw.haplotypes_iterator()],
            "facts": [self.fact2dict(fact, hap_id_type, fact_types)
                      for fact in nw.facts_iterator()],
            "edges": [self.edge2dict(edge, hap_id_type) for
                      edge in nw.edges_iterator()],
        }


    def load(self, nw, data):
        """Convert dict with keys ``haplotypes``, ``facts`` and ``edges`` stream
        into dom oobject and store it in the yatel.db.YatelNetwork instance.

        """
        self.validate_write(nw)

        hap_types = self.str2types(data["types"]["haplotypes"])
        fact_types = self.str2types(data["types"]["facts"])
        hap_id_type = hap_types["hap_id"]
        for kw in data["haplotypes"]:
            nw.add_element(self.dict2hap(kw, hap_id_type, hap_types))
        for kw in data["facts"]:
            nw.add_element(self.dict2fact(kw, hap_id_type, fact_types))
        for kw in data["edges"]:
            nw.add_element(self.dict2edge(kw, hap_id_type))


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

