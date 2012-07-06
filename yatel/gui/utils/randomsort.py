#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

import random

from yatel import dom

#===============================================================================
# FUNCTIONS
#===============================================================================


def xysort(edges, bounds=(-100, 100, 100, -100)):
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
        
    """

    ids = []
    for edge in edges:
        ids.extend(edge.haps_id)
    sortedids = {}
    for hid in ids:
        x = random.randint(bounds[0], bounds[2])
        y = random.randint(bounds[3], bounds[1])
        sortedids[hid] = (x, y)
    return sortedids
        

    


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
