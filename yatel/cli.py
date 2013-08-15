#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Launcher of yatel gui client

"""

#===============================================================================
# IMPORTS
#===============================================================================

import sys
import os
import random
import imp
import argparse

import caipyrinha

import yatel
from yatel import db, dom, etl
from yatel import conv


#===============================================================================
# CLI parser
#===============================================================================

parser = caipyrinha.Caipyrinha(prog=yatel.PRJ,
                               description=yatel.SHORT_DESCRIPTION)
parser.add_argument("--version", action='version',
                    version="%(prog)s {}".format(yatel.STR_VERSION))
parser.add_argument("--no-gui", action="store_true")


@parser.callback(action="store", metavar="CONNECTION_STRING")
def database(flags, returns):
        """database to be open with yatel

        The conn string is like: 'sqlite:///[DATABASE]' or
        'mysql://USER:PASSWORD@HOST:PORT/DATABASE' or
        'postgres://USER:PASSWORD@HOST:PORT/DATABASE'.

        """
        return db.parse_uri(flags.database, create=False)


@parser.callback("--fake-network", action="store_true")
def fake_network(flags, returns):
    """Create a new fake full conected network with 25 haplotypes on
    given connection string.

    Every haplotype has betweetn 0 and 10 facts.

    """

    lorem_ipsum = [
        'takimata', 'sea', 'ametlorem', 'magna', 'ea', 'consetetur', 'sed',
        'accusam', 'et', 'diamvoluptua', 'labore', 'diam', 'sit', 'dolores',
        'sadipscing', 'aliquyam', 'dolore', 'stet', 'lorem', 'elitr',
        'elitr', 'est', 'no', 'dolor', 'kasd', 'invidunt', 'amet', 'vero',
        'ipsum', 'rebum', 'erat', 'gubergren', 'duo', 'justo', 'tempor',
        'eos', 'sanctus', 'at', 'clita', 'ut', 'nonumyeirmod', 'amet'
    ]

    def gime_fake_hap_attrs():

        attrs_generator = {
            "name": lambda: random.choice(lorem_ipsum).title(),
            "number": lambda: random.choice(range(10, 100)),
            "color": lambda: random.choice('rgbcmyk'),
            "special": lambda: random.choice([True, False]),
            "size": lambda: random.choice(range(10, 100)) + random.random(),
            "height": lambda: random.choice(range(10, 100)) + random.random(),
            "description": lambda: (
                random.choice(lorem_ipsum).title() + " ".join(
                    [random.choice(lorem_ipsum) for _
                     in range(random.randint(10, 50))]
                )
            )

        }

        attrs = {}
        for k, v in attrs_generator.items():
            if random.choice([True, False]):
                attrs[k] = v()
        if not attrs:
            k, v = random.choice(attrs_generator.items())
            attrs[k] = v()
        return attrs

    def gimme_fake_fact_attrs():
        attrs_generator = {
            "place": lambda: random.choice(['Mordor', 'Ankh-Morpork', 'Genosha',
                                            'Gotham City', 'Hogwarts', 'Heaven',
                                            'Tatooine', 'Vulcan', 'Valhalla']),
            "category": lambda: random.choice('SABCDEF'),
            "native": lambda: random.choice([True, False]),
            "align": lambda: random.choice([-1, 0, 1]),
            "variance": lambda: random.choice(range(10, 100)) + random.random(),
            "coso": lambda: random.choice(lorem_ipsum),
        }
        attrs = {}
        for k, v in attrs_generator.items():
            if random.choice([True, False]):
                attrs[k] = v()
        if not attrs:
            k, v = random.choice(attrs_generator.items())
            attrs[k] = v()
        return attrs

    conn_data = returns.database
    conn_data["create"] = True
    conn_data["log"] = True
    nw = db.YatelNetwork(**conn_data)
    for hap_id in range(25):
        attrs = gime_fake_hap_attrs()
        hap = dom.Haplotype(hap_id, **attrs)
        nw.add_element(hap)

    for hap_id in range(25):
        for _ in range(random.randint(0, 10)):
            attrs = gimme_fake_fact_attrs()
            fact = dom.Fact(hap_id, **attrs)
            nw.add_element(fact)

    for hap_id0 in range(25):
        for hap_id1 in range(hap_id0, 25):
            edge = dom.Edge(random.randint(1, 10), hap_id0, hap_id1)
            nw.add_element(edge)
    nw.end_creation()


@parser.callback(exclusive="ex0", action="store",
                   metavar="filename.<EXT>", exit=0)
def exportdb(flags, returns):
    """Export the given database to YYF or YJF format. Extension must be yyf,
    yaml, yml, json or yjf.

    """
    ext = flags.exportdb.rsplit(".", 1)[-1].lower()
    if ext not in conv.convs():
        raise ValueError("Invalid type '{}'".format(ext))

    conn_data = returns.database
    conn_data["create"] = False
    conn_data["log"] = True
    nw = db.YatelNetwork(**conn_data)

    with open(flags.exportdb, "w") as fp:
        conv.dump(rtype=ext, nw=nw, stream=fp)


@parser.callback(exclusive="ex0", action="store",
                 metavar="filename.<EXT>", exit=0)
def importdb(flags, returns):
    """Import the given YYF or YJF format file to the given database. WARNING:
    Only local databases are allowed

    """

    ext = flags.exportdb.rsplit(".", 1)[-1].lower()
    if ext not in conv.convs():
        raise ValueError("Invalid type '{}'".format(ext))

    conn_data = returns.database
    conn_data["create"] = True
    conn_data["log"] = True
    nw = db.YatelNetwork(**conn_data)

    with open(flags.importdb) as fp:
        conv.load(rtype=ext, nw=nw, stream=fp)
    nw.end_creation()


@parser.callback("--run-etl", exclusive="ex0", action="store",
                 metavar="filename.py", exit=0)
def run_etl(flags, returns):
    """Run one or more etl inside of a given script"""
    dirname, filename = os.path.split(flags.etl)
    modname = os.path.splitext(filename)[0]
    found = imp.find_module(modname, [dirname])

    if modname in sys.modules:
        idx = 1
        tpl = "etl_" + modname + "_{}"
        while tpl.format(idx) in sys.modules:
            idx += 1
        modname =  tpl.format(idx)

    etlmodule = imp.load_module(modname, *found)

    conn_data = returns.database
    conn_data["create"] = not db.exists(conn_data)
    conn_data["log"] = True

    nw = db.YatelNetwork(**conn_data)
    for k, v in vars(etlmodule).items():
        if not k.startswith("_") \
        and inspect.isclass(v) and issubclass(v, etl.ETL):
            etl.run_etl(nw, v)


@parser.callback("--create-etl", exclusive="ex0", action="store",
                 metavar="etl_filename.py", type=argparse.FileType('w'), exit=0)
def create_etl(flags, returns):
    """Create a template file for write yout own etl"""
    fp = flags.create_etl
    fp.write(etl.get_template())



#===============================================================================
# FUNCTION
#===============================================================================

def main():
    """Run yatel

    """
    if "--no-gui" in sys.argv or "--help" in sys.argv:
        parser(sys.argv[1:])
    else:
        pass
        # from yatel import gui
        # gui.run_gui(parser)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    main()
