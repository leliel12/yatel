#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

import sys, os

from yatel import db, dom


#===============================================================================
# CONSTANTS
#===============================================================================

DB_PATH = os.path.join("data", "example.db")

CONN = None


#===============================================================================
# FUNCTIONS
#===============================================================================

def connect(create=False):
    global CONN
    
    if create:
        
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        
        CONN = db.YatelConnection("sqlite", name=DB_PATH)
        
        haps = [
            dom.Haplotype("hola", a=1, b="h1", z=23),
            dom.Haplotype("hola2", a=4, b="h4"),
            dom.Haplotype("hola3", b="h"),
            dom.Haplotype("hola4", a=4,),
            dom.Haplotype("hola5", a=5, b="h3")
        ]

        facts = [
            dom.Fact("hola", b=1, c=2, k=2),
            dom.Fact("hola2", j=1, k=2, c=3)
        ]

        edges = [
            dom.Edge(23, "hola", "hola2"),
            dom.Edge(22, "hola", "hola2", "hola5")

        ]

        CONN.init_with_values(haps, facts, edges)
    else:
        CONN = db.YatelConnection("sqlite", name=DB_PATH)
        CONN.init_yatel_database()
            

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    create = False
    if "--create" in sys.argv:
        create = True
    elif "--load" in sys.argv:
        create = False
    else:
        print "--create or --load (over {})".format(DB_PATH)
        sys.exit(1)
    connect(create)
