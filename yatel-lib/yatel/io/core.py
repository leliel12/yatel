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

import yatel
from yatel import dom, db


#===============================================================================
# CONSTANTS
#===============================================================================

VERSIONS = ("0.2",)

DEFAULT_VERSION = "0.2"

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

    def version_info2dict(self,  version_info):
        """Convert a ``db.YatelConnection().versions_infos()` result entry
        into a ``dict``"""
        return {"id": version_info[0],
                "datetime": version_info[1].strftime(yatel.DATETIME_FORMAT),
                "tag": version_info[2]}

    def dict2version_info(self, version_infod):
        """Convert a ``dict`` with version info data
        ``db.YatelConnection().versions_infos()` result entry

        """
        return (version_infod["id"],
                datetime.datetime.strptime(version_infod["datetime"],
                                           yatel.DATETIME_FORMAT),
                version_infod["tag"])

    def version2dict(self, version):
        """Convert a ``db.YatelConnection().get_version()` result entry into a
        ``dict``"""
        version = copy.deepcopy(version)
        version["data"]["topology"] = [
            [k, v] for k, v in version["data"]["topology"].items()
        ]
        version["datetime"] = version["datetime"].strftime(yatel.DATETIME_FORMAT)
        return version

    def dict2version(self, versiond):
        """Convert a ``dict`` with version data
        ``db.YatelConnection().get_version()` result entry

        """
        versiond = copy.deepcopy(versiond)
        versiond["data"]["topology"] = dict(
            (k, tuple(v)) for k, v in versiond["data"]["topology"]
        )
        versiond["datetime"] = datetime.datetime.strptime(versiond["datetime"],
                                                          yatel.DATETIME_FORMAT)
        return versiond

    #===========================================================================
    # MAIN METHODS
    #===========================================================================

    def dump(self, nw):
        """Convert dom objects into a dict with keys ``haplotypes``, ``facts``,
        ``edgest`` and ``version``

        """
        self.validate_read(nw)
        return {
            "version": DEFAULT_VERSION,
            "haplotypes": [
                self.hap2dict(hap) for hap in nw.haplotypes_iterator()
            ],
            "facts": [self.fact2dict(fact) for fact in nw.facts_iterator()],
            "edges": [self.edge2dict(edge) for edge in nw.edges_iterator()],
            "versions": [
                self.version2dict(version) for version in nw.versions_iterator()
            ]
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
        for kw in data["versions"]:
            nw.add_element(self.dict2version(kw))


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

