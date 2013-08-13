#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This module is used for construct yatel.dom object using csvcool.CSVCool
instances

"""

#===============================================================================
# IMPORTS
#===============================================================================

import csv

import csvcool

from yatel import dom
from yatel import util


#===============================================================================
# CONSTANTS
#===============================================================================

# : this is the default dialect of csv readed by yatel
EXCEL_DIALECT = csv.get_dialect("excel")


#===============================================================================
# FUNCTION
#===============================================================================

def construct_facts(cool, column_haplotype):
    """Create a tuple of instances of yatel.dom.Fact

    Params:

        :cool:
            csvcool.CSVCool instance that containing information on all known
            Facts.
        :column_haplotype:
            Name of the column containing the id of the instance of the
            yate.dom.Haplotype to which reference this Fact.

    """
    assert column_haplotype in cool.columnnames
    facts = []
    for row in cool:
        hap_id = None
        atts = util.UniqueNonUnicodeKey()
        for cname, cvalue in row.items():
            if cname == column_haplotype:
                hap_id = cvalue
            else:
                cname = cname if cname != "hap_id" else cname + "_"
                atts[cname] = cvalue

        facts.append(dom.Fact(hap_id, **atts))
    return tuple(facts)


def construct_haplotypes(cool, column_id):
    """Create a tuple of instances of yatel.dom.Haplotypes

    Params:

        :cool:
            csvcool.CSVCool instance that containing information on all known
            Haplotypes.
        :column_id:
            Name of the column containing the id of the instance of the
            Haplotype; if it None the id will be auto generated.

    """
    assert column_id in cool.columnnames or column_id == None
    haps = []
    for hap_id, row in enumerate(cool):
        atts = util.UniqueNonUnicodeKey()
        for cname, cvalue in row.items():
            if cname == column_id:
                hap_id = cvalue
            else:
                cname = cname if cname != "hap_id" else cname + "_"
                atts[cname] = cvalue
        haps.append(dom.Haplotype(hap_id, **atts))
    return tuple(haps)


def construct_edges(cool, column_weight):
    """Create a tuple of instances of yatel.dom.Edges

    Params:

        :cool:
            csvcool.CSVCool instante that containing information on all known edges.
        :column_haplotype:
            Name of the column containing the weight of the edge.

    """
    assert column_weight in cool.columnnames
    edges = []
    for row in cool:
        weight = None
        haps_id = []
        for cname, cvalue in row.items():
            if cname == column_weight:
                weight = cvalue
            else:
                haps_id.append(cvalue)
        edges.append(dom.Edge(weight, *haps_id))
    return tuple(edges)


#===============================================================================
# IO FUNCTIONS
#===============================================================================

def dump(haps, facts, edges):
    """Convert dom objects into CSVCool instances

    """

    keys = set(["hap_id"])
    for h in haps:
        assert isinstance(h, dom.Haplotype)
        keys = keys.union(f.names_attrs())
    keys = list(keys)
    rows = []
    for h in haps:
        row = []
        for k in keys:
            row.append(getattr(h, k, None))
        rows.append(row)
    cool_haps = csvcool.CSVCool(keys, rows)

    keys = set(["hap_id"])
    for f in facts:
        assert isinstance(f, dom.Fact)
        keys = keys.union(f.names_attrs)
    keys = list(keys)
    rows = []
    for f in facts:
        row = []
        for k in keys:
            row.append(getattr(f, k, None))
        rows.append(row)
    cool_facts = csvcool.CSVCool(keys, rows)

    nodes = 0
    for e in edges:
        assert isinstance(e, dom.Edge)
        nodes = len(e.haps_id) if len(haps_id) > nodes else nodes
    keys = ["weight"] + ["hap_id_" + str(i) for i in range(nodes)]
    rows = []
    for e in edges:
        row = [e.weight]
        for i in range(nodes):
            try:
                row.append(e.haps_id[i])
            except IndexError:
                row.append(None)
        rows.append(row)
    cool_edges = csvcool.CSVCool(keys, rows)

    return col_haps, cool_facts, cool_edges



def load(cool_haps, cool_facts, cool_edges):
    """Convert CSVCool instances into dom objects

    """
    haps = construct_haplotypes(cool_haps)
    facts = construct_facts(cool_facts)
    edges = construct_edges(cool_edges)
    dom.validate(haps, facts, edges)
    return haps, facts, edges


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

