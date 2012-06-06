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

"""This module is used for construct yatel.dom object using csvcool.CSVCool
instances

"""

#===============================================================================
# IMPORTS
#===============================================================================

from graph_tool import Graph

from yatel import dom


#===============================================================================
# IO FUNCTIONS
#===============================================================================

def dump(haps, facts, edges):
    nodebuff = {}
    ug = Graph(directed=False)
    
    hap_prop = ug.new_vertex_property("object")
    for hap in haps:
        assert isinstance(hap, dom.Haplotype)
        vertex = ug.add_vertex()
        hap_prop[vertex] = hap
        nodebuff[hap.hap_id] = vertex
    ug.vertex_properties["haplotypes"] = hap_prop
    
    fact_prop = ug.new_vertex_property("object")
    for fact in facts:
        assert isinstance(fact, dom.Fact)
        fact_prop[nodebuff[fact.hap_id]] = fact
    ug.vertex_properties["facts"] = fact_prop
    
    edge_prop = ug.new_vertex_property("object")
    for edge in edges:
        assert isinstance(edge, dom.Edge)
        if len(edge.haps_id) != 2:
            msg = "grap-tool not support hypergraphs"
            raise ValueError(msg)
        nodefrom = nodebuff[edge.haps_id[0]]
        nodeto = nodebuff[edge.haps_id[1]]
        ug_edge = ug.add_edge(nodefrom, nodeto)
        edge_prop[ug_edge] = edge
    ug.edge_properties["edges"] = edge_prop
    
    return ug
        
    

def load(graph):
    pass

    
#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

