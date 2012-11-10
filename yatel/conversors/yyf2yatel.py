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

import yaml

from yatel import dom


#===============================================================================
# IO FUNCTIONS
#===============================================================================

def dump(haps, facts, edges, stream=None, **kwargs):
    """Convert dom objects into yyf stream

    """
    haps_data = []
    for hap in haps:
        hd = {"hap_id": hap.hap_id}
        hd.update(hap.items_attrs())
        haps_data.append(hd)
    facts_data = []
    for fact in facts:
        hd = {"hap_id": fact.hap_id}
        hd.update(fact.items_attrs())
        facts_data.append(hd)
    edges_data = []
    for edge in edges:
        ed = {"weight": edge.weight}
        ed["haps_id"] = list(edge.haps_id)
        edges_data.append(ed)
    data = {"haplotypes": haps_data, "facts": facts_data, "edges": edges_data}
    return yaml.dump(data, stream, **kwargs)


def load(stream, **kwargs):
    """Convert YYF stream into dom objects

    """
    data = yaml.load(stream, **kwargs)
    return (
        tuple(dom.Haplotype(**kw) for kw in data["haplotypes"]),
        tuple(dom.Fact(**kw) for kw in data["facts"]),
        tuple(dom.Edge(kw["weight"], *kw["haps_id"]) for kw in data["edges"])
    )


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

