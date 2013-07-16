#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Creates a default test database in data directory.

"""


#===============================================================================
# IMPORTS
#===============================================================================

import sys, os, random, hashlib

from yatel import db2 as db
from yatel import dom


#===============================================================================
# CONSTANTS
#===============================================================================

DB_PATH = os.path.join("data", "example2.db")


#===============================================================================
# FUNCTIONS
#===============================================================================

def connect(create=False):
    """Connect to the *data/example.db* database.

    **Params**
        :create: ``bool``; if true a new database is created; otherwise connect
                 to the existing one.

    **Return**
        A ``yatel.db.YatelConnection`` instance

    """
    conn = None

    if create:

        choices = {
            int: lambda: random.randint(1, 100),
            float: lambda: random.randint(1, 100) + random.random(),
            str: lambda: hashlib.sha1(str(random.random)).hexdigest(),
            bool: lambda: bool(random.randint(0, 1)),
        }

        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

        conn = db.YatelNetwork("sqlite", dbname=DB_PATH, create=True)

        haps_id = []
        for idx in range(random.randint(10, 50)):
            name = "haplotype_" + str(idx)
            attrs = {}
            for jdx, func in enumerate(sorted(choices.values())):
                attrs["attr_" + str(jdx)] = func()
            hap = dom.Haplotype(name, **attrs)
            haps_id.append(name)
            conn.add_element(hap)
#~
        for _ in range(random.randint(10, 50)):
            hap_id = random.choice(haps_id)
            attrs = {}
            for jdx, func in enumerate(sorted(choices.values())):
                attrs["attr_" + str(jdx)] = func()
            conn.add_element(dom.Fact(hap_id, b=1, c=2, k=2))
#~
        for _ in range(random.randint(10, 50)):
            weight = choices[float]()
            hap_0 = random.choice(haps_id)
            hap_1 = random.choice(haps_id)
            while hap_1 == hap_0:
                hap_1 = random.choice(haps_id)
            conn.add_element(dom.Edge(weight, hap_0, hap_1))
    else:
        conn = db.YatelNetwork("sqlite", dbname=DB_PATH)
    return conn


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    create = True
    if "--create" in sys.argv:
        create = True
    elif "--load" in sys.argv:
        create = False
    else:
        print "--create or --load (over {})".format(DB_PATH)
        sys.exit(1)
    connect(create)

