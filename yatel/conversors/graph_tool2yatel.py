#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice 
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This module is used for bidirectional conversions between 
yatel.dom objects and graph-tool Graph's instances

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
    """Create graph-tool Graph object from a list of haplotypes, facts and
    edges.
    
    The original objects are stores in internal properties:
    
        - ``haps`` -> ``graph.vertex_properties["haplotypes"]``
        - ``facts`` -> ``graph.vertex_properties["facts"]``
        - ``edges`` -> ``graph.edge_properties["edges"]``
        
    """
    
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
        prop = fact_prop[nodebuff[fact.hap_id]]
        if prop == None:
            prop = []
            fact_prop[nodebuff[fact.hap_id]] = prop
        prop.append(fact)
    ug.vertex_properties["facts"] = fact_prop
    
    edge_prop = ug.new_edge_property("object")
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
    """Create yatel DOM objects from a graph-tool Graph.
    
    The original objects are stores in internal properties:
    
        - ``haps`` <- ``graph.vertex_properties["haplotypes"]``
        - ``facts`` <- ``graph.vertex_properties["facts"]``
        - ``edges`` <- ``graph.edge_properties["edges"]``
        
    """
    haps = []
    facts = []
    for v in graph.vertices():
        haps.append(
            graph.vertex_properties["haplotypes"][v]
        )
        factlist = graph.vertex_properties["facts"][v]
        if factlist:
            facts.extend(factlist)
    edges = []
    for e in graph.edges():
        edges.append(
            graph.edge_properties["edges"][e]
        )
    return tuple(haps), tuple(facts), tuple(edges)
        
    
#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
    
    
    
    
    

