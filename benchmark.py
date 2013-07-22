#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <jbc.develop@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a WISKEY in return Juan BC

#===============================================================================
# IMPORTS
#===============================================================================

import os, random, collections, hashlib, time, pprint

from yatel import db, db2, db3, dom

import numpy as np

#===============================================================================
# PRE CONFIG
#===============================================================================

path = os.path.dirname(os.path.abspath(__file__))
peewee_path = os.path.join(path, "data", "bench_pewee.db")
dal_path = os.path.join(path, "data", "bench_dal.db")
sa_path = os.path.join(path, "data", "bench_sa.db")

if os.path.exists(peewee_path):
    os.remove(peewee_path)
if os.path.exists(dal_path):
    os.remove(dal_path)
if os.path.exists(sa_path):
    os.remove(sa_path)


#===============================================================================
# BENCH DEC
#===============================================================================

benchs = collections.OrderedDict()
funcs = []

def bench(times=1):
    def _bench(func):
        funcs.append((func, times))
        return func
    return _bench


def run():
    for func, times in funcs:
        results = []
        for _ in range(times):
            start = time.time()
            func()
            end = time.time()
            results.append(end-start)
        benchs[func.__name__] = np.average(results)


#===============================================================================
# CREATE SOME NETWORKS
#===============================================================================

def create_network():
    choices = {
        int: lambda: random.randint(1, 100),
        float: lambda: random.randint(1, 100) + random.random(),
        str: lambda: hashlib.sha1(str(random.random)).hexdigest(),
        bool: lambda: bool(random.randint(0, 1)),
    }

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

    return (haps, facts, edges)

#===============================================================================
# THE NETWORK
#===============================================================================

haps, facts, edges = create_network()

#===============================================================================
# CREATE THE two db
#===============================================================================

peewee_db = None
dal_db = None
sa_db = None

@bench()
def create_peewee():
    conn = db.YatelConnection("sqlite", name=peewee_path)
    conn.init_with_values(haps, facts, edges)

@bench()
def create_dal():
    conn = db2.YatelNetwork("sqlite", dbname=dal_path, create=True)
    map(conn.add_element, haps)
    map(conn.add_element, facts)
    map(conn.add_element, edges)
    conn.end_creation()

@bench()
def create_sa():
    conn = db3.YatelNetwork("sqlite", dbname=dal_path, create=True)
    map(conn.add_element, haps)
    map(conn.add_element, facts)
    map(conn.add_element, edges)
    conn.end_creation()

@bench()
def connect_peewee():
    global peewee_db
    peewee_db = db.YatelConnection("sqlite", name=peewee_path)
    peewee_db.init_yatel_database()

@bench()
def connect_dal():
    global dal_db
    dal_db = db2.YatelNetwork("sqlite", dbname=dal_path)

@bench(100)
def iter_haplotypes_peewee():
    list(peewee_db.iter_haplotypes())

@bench(100)
def iter_haplotypes_dal():
    list(dal_db.iter_haplotypes())

@bench(100)
def iter_facts_peewee():
    list(peewee_db.iter_facts())

@bench(100)
def iter_facts_dal():
    list(dal_db.iter_facts())

@bench(100)
def iter_edges_peewee():
    list(peewee_db.iter_edges())

@bench(100)
def iter_edges_dal():
    list(dal_db.iter_edges())


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    run()
    for k, v in benchs.items():
        print "{} -> {}".format(k, v)
