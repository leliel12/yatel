#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.


#===============================================================================
# DOCS
#===============================================================================

"""This module is used for construct yatel.dom object using CSVCool instances

"""

#===============================================================================
# IMPORTS
#===============================================================================

import csv

import dom


#===============================================================================
# CONSTANTS
#===============================================================================

#: this is the default dialect of csv readed by yatel
EXCEL_DIALECT = dialect = csv.get_dialect("excel")


#===============================================================================
# FUNCTION
#===============================================================================

def construct_facts(cool, column_haplotype):
    assert column_haplotype in cool.columnnames
    facts = []
    for row in cool:
        hap_id = None
        atts = {}
        for cname, cvalue in row.items():
            if cname == column_haplotype:
                hap_id = str(cvalue)
            else:
                atts[cname] = cvalue
        facts.append(dom.Fact(hap_id, **atts))
    return tuple(facts)


def construct_haplotypes(cool, column_id):
    assert column_id in cool.columnnames
    haps = []
    for row in cool:
        hap_id = None
        atts = {}
        for cname, cvalue in row.items():
            if cname == column_id:
                hap_id = str(cvalue)
            else:
                atts[cname] = cvalue
        haps.append(dom.Haplotype(hap_id, **atts))
    return tuple(haps)
    
    
def construct_edges(cool, column_weight):
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
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




