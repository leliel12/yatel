

def to_dict_graph(*edges):
    gd = {}
    for e in edges:
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


def strongly_connected_components(*edges):
    """ Find the strongly connected components in a graph using
    Tarjan's algorithm.

    Graph should be a dictionary mapping node names to
    lists of successor nodes.
    
    by Paul Harrison 
    http://www.logarithmic.net/pfh-files/blog/01208083168/sort.py
    
    """
    
    graph = to_dict_graph(*edges)
    
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


def robust_topological_sort(*edges):
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

    components = strongly_connected_components(*edges)

    node_component = { }
    for component in components:
        for node in component:
            node_component[node] = component

    component_graph = { }
    for component in components:
        component_graph[component] = [ ]

    graph = to_dict_graph(*edges)
    for node in graph:
        node_c = node_component[node]
        for successor in graph[node]:
            successor_c = node_component[successor]
            if node_c != successor_c:
                component_graph[node_c].append(successor_c)

    return topological_sort(component_graph)


class Edge(object):
    def __init__(self, *haps_id):
        self.haps_id = haps_id

if __name__ == '__main__':
    
    edges = [
        Edge(4, 0),
        Edge(0, 1),
        Edge(1, 2),
        Edge(2, 1),
        Edge(2, 3),
        Edge(5, 6),
        
       
    ]   

    
    print robust_topological_sort(
        
        *edges
    )


