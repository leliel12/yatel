#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

import sys, os, random, hashlib

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
    
        choices = {
            int: lambda: random.randint(1, 100000),
            float: lambda: random.randint(1, 100000) + random.random(),
            str: lambda: hashlib.sha1(str(random.random)).hexdigest(),
            bool: lambda: bool(random.randint(0, 1)),
        }
        
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        
        CONN = db.YatelConnection("sqlite", name=DB_PATH)
        
        haps = []
        for idx in range(random.randint(10, 50)):
            name = "haplotype_" + str(idx)
            attrs = {}
            for jdx, func in enumerate(sorted(choices.values())):
                attrs["attr_" + str(jdx)] = func()
            haps.append(dom.Haplotype(name, **attrs))
            
        facts = []
        for _ in range(random.randint(10, 50)):
            hap_id = random.choice(haps).hap_id
            attrs = {}
            for jdx, func in enumerate(sorted(choices.values())):
                attrs["attr_" + str(jdx)] = func()
            facts.append(dom.Fact(hap_id, b=1, c=2, k=2))
            
        edges = []
        for _ in range(random.randint(10, 50)):
            weight = choices[float]()
            hap_0 = random.choice(haps).hap_id
            hap_1 = random.choice(haps).hap_id
            while hap_1 == hap_0:
                hap_1 = random.choice(haps).hap_id
            edges.append(dom.Edge(weight, hap_0, hap_1))

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
