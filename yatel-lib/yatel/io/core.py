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

VERSIONS = ("0.2",)

DEFAULT_VERSION = "0.2"

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

    def hap2dict(self, hap):
        """Convert a ``dom.Haplotype`` instance into a dict"""
        hd = {"hap_id": hap.hap_id}
        hd.update(hap.items_attrs())
        return hd

    def dict2hap(self, hapd):
        """Convert a ``dict`` with haplotype data into a ``dom.Haplotype``
        instance

        """
        return dom.Haplotype(**hapd)

    def fact2dict(self, fact):
        """Convert a ``dom.Fact`` instance into a dict"""
        hd = {"hap_id": fact.hap_id}
        hd.update(fact.items_attrs())
        return hd

    def dict2fact(self, factd):
        """Convert a ``dict`` with Fact data into a ``dom.Fact``
        instance

        """
        return dom.Fact(**factd)

    def edge2dict(self, edge):
        """Convert a ``dom.Edge`` instance into a dict"""
        ed = {"weight": edge.weight}
        ed["haps_id"] = list(edge.haps_id)
        return ed

    def dict2edge(self, edged):
        """Convert a ``dict`` with Edge data into a ``dom.Edge``
        instance

        """
        return dom.Edge(edged["weight"], *edged["haps_id"])

    #===========================================================================
    # MAIN METHODS
    #===========================================================================

    def dump(self, nw):
        """Convert dom objects into a dict with keys ``haplotypes``, ``facts``,
        and ``edgest``

        """
        self.validate_read(nw)
        return {
            "version": DEFAULT_VERSION,
            "haplotypes": [
                self.hap2dict(hap) for hap in nw.haplotypes_iterator()
            ],
            "facts": [self.fact2dict(fact) for fact in nw.facts_iterator()],
            "edges": [self.edge2dict(edge) for edge in nw.edges_iterator()],
        }


    def load(self, nw, data):
        """Convert dict with keys ``haplotypes``, ``facts`` and ``edges`` stream
        into dom oobject and store it in the yatel.db.YatelNetwork instance.

        """
        self.validate_write(nw)
        for kw in data["haplotypes"]:
            nw.add_element(self.dict2hap(kw))
        for kw in data["facts"]:
            nw.add_element(self.dict2fact(kw))
        for kw in data["edges"]:
            nw.add_element(self.dict2edge(kw))


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

