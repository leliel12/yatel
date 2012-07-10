#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

import random

import dom


#===============================================================================
# TOPOLOGICAL SORT
#===============================================================================

def to_dict_graph(edges):
    """Convert an iterable of edges in a dict with ``keys`` equals
    ``edge.haps_id[0]``, and ``value`` equals ``edge.haps_id[1:].
    The nodes without childs has values with empty list.

    **Example**

    ::
        >>> from yatel.dom import Edge
        >>> edges = (
            Edge(1, "id0", "id1"), Edge(1, "id2", "id3"), Edge(1, "id4", "id1")
        )
        >>> to_dict_graph(edges)
        {
            'id4': ['id1'], 'id2': ['id3'],
            'id3': ['id3'], 'id0': ['id1'], 'id1': ['id1']
        }

    """
    gd = {}
    for e in edges:
        assert isinstance(e, dom.Edge)
        stk = list(e.haps_id)
        key = stk.pop(0)
        if key not in gd:
            gd[key] = []
        gd[key].extend(stk)
    for dsts in gd.values():
        for d in dsts:
            if d not in gd:
                gd[d] = [d]
    return gd


def strongly_connected_components(edges):
    """ Find the strongly connected components in a graph using
    Tarjan's algorithm.

    Graph should be a dictionary mapping node names to
    lists of successor nodes.

    by Paul Harrison
    http://www.logarithmic.net/pfh-files/blog/01208083168/sort.py

    """

    graph = to_dict_graph(edges)

    result = [ ]
    stack = [ ]
    low = { }

    def visit(node):
        if node in low: return

        num = len(low)
        low[node] = num
        stack_pos = len(stack)
        stack.append(node)

        for successor in graph[node]:
            visit(successor)
            low[node] = min(low[node], low[successor])

        if num == low[node]:
            component = tuple(stack[stack_pos:])
            del stack[stack_pos:]
            result.append(component)
            for item in component:
                low[item] = len(graph)

    for node in graph:
        visit(node)

    return result


def topsort(edges):
    """First identify strongly connected components,
    then perform a topological sort on these components.

    by Paul Harrison
    http://www.logarithmic.net/pfh-files/blog/01208083168/sort.py

    """

    def topological_sort(graph):
        count = { }
        for node in graph:
            count[node] = 0
        for node in graph:
            for successor in graph[node]:
                count[successor] += 1
        ready = [ node for node in graph if count[node] == 0 ]
        result = [ ]
        while ready:
            node = ready.pop(-1)
            result.append(node)
            for successor in graph[node]:
                count[successor] -= 1
                if count[successor] == 0:
                    ready.append(successor)
        return result

    components = strongly_connected_components(edges)

    node_component = { }
    for component in components:
        for node in component:
            node_component[node] = component

    component_graph = { }
    for component in components:
        component_graph[component] = [ ]

    graph = to_dict_graph(edges)
    for node in graph:
        node_c = node_component[node]
        for successor in graph[node]:
            successor_c = node_component[successor]
            if node_c != successor_c:
                component_graph[node_c].append(successor_c)

    return topological_sort(component_graph)


def xymap_topsort(edges, bounds=(-100, 100, 100, -100), step=(20, 20)):
    """Topological sort of iterable of edges

    **Parameters**
        :edges:
            An iterable of edges.
        :bounds:
            x0, y0, x1, y1
            
            x0, y0
                +---------------+
                |               |
                +---------------+ x1, y1
                
        :step:
            Separation between nodes center in axis.

    """

    xymap = {}
    xstep, ystep = step
    xtop, ytop = bounds[2], bounds[3] 

    y = bounds[1]
    for row in topsort(edges):
        x = bounds[0]
        for c in row:
            xymap[c] = x, y
            if x + xstep < xtop:
                x += xstep
            elif y - ystep > ytop:
                y -= y
        if y - ystep > ytop:
            y -= ystep
    return xymap


#===============================================================================
# RANDOMSORT
#===============================================================================

def xymap_randomsort(edges, bounds=(-100, 100, 100, -100)):
    """Topological sort of iterable of edges

    **Parameters**
        :edges:
            An iterable of edges.
        :bounds:
            x0, y0, x1, y1
            
            x0, y0  +---------------+
                    |               |
                    +---------------+ x1, y1
        
    """

    ids = []
    for edge in edges:
        ids.extend(edge.haps_id)
    xymap = {}
    for hid in ids:
        x = random.randint(bounds[0], bounds[2])
        y = random.randint(bounds[3], bounds[1])
        xymap[hid] = (x, y)
    return xymap

#===============================================================================
# PUBLIC
#===============================================================================

def xy(edges, algorithm, bounds=(-100, 100, 100, -100),
        *args, **kwargs
    ):
    func = None
    if algorithm == "topsort":
        func = xymap_topsort
    elif algorithm == "randomsort":
        func = xymap_randomsort
    else:
        raise ValueError("Invalid algorithm")
    xymap = func(edges, bounds, *args, **kwargs)
    for hapid in sorted(xymap.keys()):
        x, y = xymap[hapid]
        yield x, y, hapid


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
