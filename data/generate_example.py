#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yatel import db

DB_PATH = "example.db"
CONN = db.YatelConnection("sqlite", name=dbpath)

def generate_example(create):
    
    if create:
        
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
        print "--create or --load (over ../data/example.db)"
    generate_example(create)
