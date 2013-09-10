#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Launcher of yatel cli tools

"""


#===============================================================================
# IMPORTS
#===============================================================================

import sys
import os
import random
import imp
import argparse
import inspect
import traceback
import datetime

import caipyrinha

import yatel
from yatel import db, dom, etl
from yatel import io
from yatel import stats
from yatel import weight


#===============================================================================
# CLI parser
#===============================================================================

parser = caipyrinha.Caipyrinha(prog=yatel.PRJ,
                               description=yatel.SHORT_DESCRIPTION)
parser.add_argument("--version", action='version',
                    version="%(prog)s {}".format(yatel.STR_VERSION))
parser.add_argument("-f", "--force", action="store_true",
                    help=("If you perform some action like import or"
                          "copy this option destroy"
                          "a network in this connection"))
parser.add_argument("--full-stack", action="store_true",
                    help="If yatel fails, show all the stack trace of the error")

@parser.callback(action="store", metavar="CONNECTION_STRING")
def database(flags, returns):
        """database to be open with yatel

        The conn string is like: 'sqlite:///[DATABASE]' or
        'mysql://USER:PASSWORD@HOST:PORT/DATABASE' or
        'postgres://USER:PASSWORD@HOST:PORT/DATABASE'.

        """
        return db.parse_uri(flags.database, create=False)


@parser.callback("--fake-network", exclusive="ex0", action="store", nargs=3)
def fake_network(flags, returns):
    """Create a new fake full conected network with on given connection string.

    The first parameter is the number of haplotypes, the second one is
    the number of maximun facts of every haplotype and the third is the
    algoritm to calculate the distance

    """

    _fail_if_no_force("--fake-network", flags, returns.database)


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

    haps_n = int(flags.fake_network[0])
    facts_n = int(flags.fake_network[1])
    weight_calc = flags.fake_network[2]

    if weight_calc not in weight.calculators():
        msg = "Invalid calculator '{}'. Please use one of: '{}'"
        msg = msg.format(weight_calc, "|".join(weight.calculators()))
        parser.error(msg)

    conn_data = returns.database
    conn_data["create"] = True
    conn_data["log"] = True
    nw = db.YatelNetwork(**conn_data)

    haps = []
    for hap_id in range(haps_n):
        attrs = gime_fake_hap_attrs()
        hap = dom.Haplotype(hap_id, **attrs)
        nw.add_element(hap)
        haps.append(hap)

    for hap_id in range(haps_n):
        for _ in range(random.randint(0, facts_n)):
            attrs = gimme_fake_fact_attrs()
            fact = dom.Fact(hap_id, **attrs)
            nw.add_element(fact)

    for hs, w in weight.weights(weight_calc, haps):
        haps_id = map(lambda h: h.hap_id, hs)
        edge = dom.Edge(w, *haps_id)
        nw.add_element(edge)
    nw.end_creation()


@parser.callback(exclusive="ex0", action="store", type=argparse.FileType("w"),
                 metavar="filename.<EXT>", exit=0)
def dump(flags, returns):
    """Export the given database to YYF or YJF format. Extension must be yyf,
    yaml, yml, json or yjf.

    """
    ext = flags.dump.name.rsplit(".", 1)[-1].lower()
    if ext not in io.parsers():
        raise ValueError("Invalid type '{}'".format(ext))

    conn_data = returns.database
    conn_data["create"] = False
    conn_data["log"] = True
    nw = db.YatelNetwork(**conn_data)

    io.dump(rtype=ext, nw=nw, stream=flags.dump)


@parser.callback(exclusive="ex0", action="store",
                 metavar="filename_template.<EXT>", exit=0)
def backup(flags, returns):
    """Like dump but always create a new file with the format
    'filename_template<TIMESTAMP>.<EXT>'

    """
    fname, ext = flags.backup.rsplit(".", 1)

    if ext.lower() not in io.parsers():
        raise ValueError("Invalid type '{}'".format(ext))

    fpath = "{}{}.{}".format(fname, datetime.datetime.utcnow().isoformat(), ext)

    conn_data = returns.database
    conn_data["create"] = False
    conn_data["log"] = True
    nw = db.YatelNetwork(**conn_data)

    with open(fpath, 'w') as fp:
        io.dump(rtype=ext.lower(), nw=nw, stream=fp)


@parser.callback(exclusive="ex0", action="store", type=argparse.FileType(),
                 metavar="filename.<EXT>", exit=0)
def load(flags, returns):
    """Import the given YYF or YJF format file to the given database. WARNING:
    Only local databases are allowed

    """
    _fail_if_no_force("--load", flags, returns.database)

    ext = flags.load.name.rsplit(".", 1)[-1].lower()
    if ext not in io.parsers():
        raise ValueError("Invalid type '{}'".format(ext))

    conn_data = returns.database
    conn_data["create"] = True
    conn_data["log"] = True
    nw = db.YatelNetwork(**conn_data)

    io.load(rtype=ext, nw=nw, stream=flags.load)

    nw.end_creation()


@parser.callback(exclusive="ex0", action="store",
                 metavar="CONNECTION_STRING", exit=0)
def copy(flags, returns):
    """Copy the database (of `database` to this connection"""

    to_conn_data = db.parse_uri(flags.copy, create=True, log=True)
    _fail_if_no_force("--copy", flags, to_conn_data)

    to_nw = db.YatelNetwork(**to_conn_data)

    conn_data = returns.database
    conn_data["create"] = False
    conn_data["log"] = True
    from_nw = db.YatelNetwork(**conn_data)

    db.copy(from_nw, to_nw)
    to_nw.end_creation()


@parser.callback("--create-etl", exclusive="ex0", action="store",
                 metavar="etl_filename.py", type=argparse.FileType('w'),
                 exit=0)
def create_etl(flags, returns):
    """Create a template file for write yout own etl"""
    tpl = etl.get_template()
    fp = flags.create_etl
    fp.write(tpl)


@parser.callback("--etl-desc", exclusive="ex0", action="store", nargs=2,
                 metavar="ARG", exit=0)
def etl_desc(flags, returns):
    """Return a list of parameters and documentataton abot the etl

    The first two aruments are the module of the etl and the etl class name,

    """
    filepath = flags.etl_desc[0]
    clsname = flags.etl_desc[1]

    etl_cls = etl.etlcls_from_module(filepath, clsname)
    doc = etl_cls.__doc__
    params = ", ".join(etl_cls.setup_args)
    print ("ETL CLASS: {cls}\n"
           "FILE: {path}\n"
           "DOC: {doc}\n"
           "PARAMETERS: {params}\n").format(cls=clsname, path=filepath,
                                          doc=doc, params=params)


#=================================================
# LAST ALWAYS!
#=================================================

@parser.callback("--run-etl", exclusive="ex0", action="store", nargs="+",
                 metavar="ARG", exit=0)
def run_etl(flags, returns):
    """Run one or more etl inside of a given script.

    The first argument is in the format path/to/module.py:ClassName
    the second onwards parameter are parameters of the setup method of the
    given class.

    """
    filepath, clsname = flags.run_etl[0].split(":", 1)
    params = flags.run_etl[1:]

    etl_cls = etl.etlcls_from_module(filepath, clsname)
    etl_instance = etl_cls()

    conn_data = returns.database
    conn_data["create"] = True
    conn_data["log"] = True

    _fail_if_no_force("--run-etl", flags, conn_data)

    nw = db.YatelNetwork(**conn_data)

    etl.execute(nw, etl_instance, *params)

    nw.end_creation()


#===============================================================================
# FUNCTION
#===============================================================================

def _fail_if_no_force(cmd, flags, conn_data):
    if not flags.force and db.exists(**conn_data):
        msg = ("There is an existing 'YatelNetwork' in the conection '{}' and "
               "the command '{}' will destroy it. If you want to destroy it "
               "anyway use the option '-f' or '--force' along with "
               "the command '{}'").format(db.to_uri(**conn_data), cmd, cmd)
        parser.error(msg)


def main():
    """Run yatel cli tools

    """
    args = sys.argv[1:] or ["--help"]
    if "--full-tack" in args:
        parser(args)
    else:
        try:
            parser(args)
        except Exception as err:
            parser.error(str(err))
            print_error()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    main()
