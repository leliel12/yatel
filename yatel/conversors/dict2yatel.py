#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This module is used for construct yatel.dom object using yatel yaml format
files

"""

#===============================================================================
# IMPORTS
#===============================================================================

import datetime

import yatel
from yatel import dom


#===============================================================================
# CONSTANTS
#===============================================================================

VERSIONS = ("0.1",)

DEFAULT_VERSION = "0.1"


#===============================================================================
# IO FUNCTIONS
#===============================================================================

def hap2dict(hap):
    """Convert a ``dom.Haplotype`` instance into a dict"""
    hd = {"hap_id": hap.hap_id}
    hd.update(hap.items_attrs())
    return hd


def dict2hap(hapd):
    """Convert a ``dict`` with haplotype data into a ``dom.Haplotype``
    instance

    """
    return dom.Haplotype(**hapd)


def fact2dict(fact):
    """Convert a ``dom.Fact`` instance into a dict"""
    hd = {"hap_id": fact.hap_id}
    hd.update(fact.items_attrs())
    return hd


def dict2fact(factd):
    """Convert a ``dict`` with Fact data into a ``dom.Fact``
    instance

    """
    return dom.Fact(**factd)


def edge2dict(edge):
    """Convert a ``dom.Edge`` instance into a dict"""
    ed = {"weight": edge.weight}
    ed["haps_id"] = list(edge.haps_id)
    return ed


def dict2edge(edged):
    """Convert a ``dict`` with Edge data into a ``dom.Edge``
    instance

    """
    return dom.Edge(edged["weight"], *edged["haps_id"])


def version_info2dict(version_info):
    """Convert a ``db.YatelConnection().versions_infos()` result entry into a
    ``dict``"""
    return {"id": version_info[0],
             "datetime": version_info[1].strftime(yatel.DATETIME_FORMAT),
             "tag": version_info[2]}


def dict2version_info(version_infod):
    """Convert a ``dict`` with version info data
    ``db.YatelConnection().versions_infos()` result entry

    """
    return (version_infod["id"],
             datetime.datetime.strptime(version_infod["datetime"],
                                        yatel.DATETIME_FORMAT),
             version_infod["tag"])


def version2dict(version):
    """Convert a ``db.YatelConnection().get_version()` result entry into a
    ``dict``"""
    topology = {}
    for k, v in version["data"]["topology"].items():
        topology[hap2dict(k)] = v
    version["data"]["topology"] = topology
    version["datetime"] = version["datetime"].strftime(yatel.DATETIME_FORMAT)
    return dict(version)


def dict2version(versiond):
    """Convert a ``dict`` with version data
    ``db.YatelConnection().get_version()` result entry

    """
    topology = {}
    for k, v in versiond["data"]["topology"]:
        topology[dict2hap(k)] = tuple(v)
    versiond["data"]["topology"] = topology
    versiond["datetime"] = datetime.datetime.strptime(versiond["datetime"],
                                                       yatel.DATETIME_FORMAT)
    return dict(versiond)


#===============================================================================
# HELPERS
#===============================================================================

def dump(haps, facts, edges, versions):
    """Convert dom objects into a dict with keys ``haplotypes``, ``facts``,
    ``edgest`` and ``version``

    """
    return {"version": DEFAULT_VERSION,
             "haplotypes": [hap2dict(hap) for hap in haps],
             "facts": [fact2dict(fact) for fact in facts],
             "edges": [edge2dict(edge) for edge in edges],
             "versions": [version2dict(version) for version in versions]}


def load(data):
    """Convert dict with keys ``haplotypes``, ``facts`` and ``edges`` stream
    into dom objects.

    """
    return (tuple(dict2hap(kw) for kw in data["haplotypes"]),
             tuple(dict2fact(kw) for kw in data["facts"]),
             tuple(dict2edge(kw) for kw in data["edges"]),
             tuple(version2dict(kw) for kw in data["versions"]))


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

