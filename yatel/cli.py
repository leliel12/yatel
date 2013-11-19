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
import pprint
import datetime

import caipyrinha

import yatel
from yatel import db, dom, etl, tests
from yatel import yjf
from yatel import stats
from yatel import weight


#===============================================================================
# GROUPS
#===============================================================================

# this group represent an option to show information of something
GROUP_INFO = 0

# this group execute some operation over your network
GROUP_OP = GROUP_INFO  # information and operation is not allowed



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
parser.add_argument("--log", action="store_true",
                    help="log all backend info to stdio")


@parser.callback("--list-connection-strings", action="store_true",
                 exclusive=GROUP_INFO, exit=0)
def list_connection_strings(flags, returns):
    """List all available connection strings in yatel"""
    for engine in db.ENGINES:
        print "{}: {}".format(engine, db.ENGINE_URIS[engine])
    print ""


@parser.callback(action="store", metavar="CONNECTION_STRING")
def database(flags, returns):
        """database to be open with yatel (see yatel --list-conection-strings)

        """
        return db.parse_uri(flags.database, log=flags.log or None)


@parser.callback("--run-tests", metavar="LEVEL", action="store", type=int,
                 exclusive=GROUP_OP)
def run_tests(flags, returns):
        """Run all yatel test suites

        """
        tests.run_tests(flags.run_tests)


@parser.callback(action="store", metavar="[r|w|a]", default=db.MODE_READ)
def mode(flags, returns):
    """The mode to open the database [r|w|a]"""
    if flags.mode not in db.MODES:
        parser.error("{} is not a valid mode use 'r' 'w' or 'a'")
    if returns.database:
        returns.database["mode"] = flags.mode


@parser.callback("--describe", exclusive=GROUP_OP, action="store_true")
def describe(flags, returns):
    """Print information about the network"""
    conn_data = returns.database
    nw = db.YatelNetwork(**conn_data)
    pprint.pprint(dict(nw.describe()))


@parser.callback("--fake-network", exclusive=GROUP_OP, action="store", nargs=3)
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
        edge = dom.Edge(w, haps_id)
        nw.add_element(edge)
    nw.confirm_changes()


@parser.callback(exclusive=GROUP_OP, action="store", type=argparse.FileType("w"),
                 metavar="filename.json", exit=0)
def dump(flags, returns):
    """Export the given database to json format.

    """
    conn_data = returns.database
    nw = db.YatelNetwork(**conn_data)
    yjf.dump(nw=nw, stream=flags.dump)


@parser.callback(exclusive=GROUP_OP, action="store",
                 metavar="filename_template.json", exit=0)
def backup(flags, returns):
    """Like dump but always create a new file with the format
    'filename_template<TIMESTAMP>.json'.

    """
    fname, ext = flags.backup.rsplit(".", 1)

    fpath = "{}{}.{}".format(fname, datetime.datetime.utcnow().isoformat(), ext)

    conn_data = returns.database
    nw = db.YatelNetwork(**conn_data)

    with open(fpath, 'w') as fp:
        yjf.dump(nw=nw, stream=fp)


@parser.callback(exclusive=GROUP_OP, action="store", type=argparse.FileType(),
                 metavar="filename.json", exit=0)
def load(flags, returns):
    """Import the given file to the given database.

    """
    conn_data = returns.database
    nw = db.YatelNetwork(**conn_data)
    yjf.load(nw=nw, stream=flags.load)
    nw.confirm_changes()


@parser.callback(exclusive=GROUP_OP, action="store",
                 metavar="CONNECTION_STRING", exit=0)
def copy(flags, returns):
    """Copy the database of `database` to this connection"""

    to_conn_data = db.parse_uri(flags.copy, mode=db.MODE_WRITE, log=flags.log)
    _fail_if_no_force("--copy", flags, to_conn_data)

    to_nw = db.YatelNetwork(**to_conn_data)

    conn_data = returns.database
    from_nw = db.YatelNetwork(**conn_data)

    db.copy(from_nw, to_nw)
    to_nw.confirm_changes()


@parser.callback("--create-etl", exclusive=GROUP_OP, action="store",
                 metavar="etl_filename.py", type=argparse.FileType('w'),
                 exit=0)
def create_etl(flags, returns):
    """Create a template file for write yout own etl"""
    ext = flags.create_etl.name.rsplit(".", 1)[-1].lower()
    if ext != "py":
        raise ValueError("Invalid extension '{}'. must be 'py'".format(ext))
    tpl = etl.get_template()
    fp = flags.create_etl
    fp.write(tpl)


@parser.callback("--desc-etl", exclusive=GROUP_INFO, action="store", nargs=1,
                 metavar="ARG", exit=0)
def desc_etl(flags, returns):
    """Return a list of parameters and documentataton about the etl

    The argument is in the format path/to/module.py:ClassName

    """
    filepath, clsname = flags.desc_etl[0].split(":", 1)

    etl_cls = etl.etlcls_from_module(filepath, clsname)
    doc = etl_cls.__doc__ or "-"
    params = ", ".join(etl_cls.setup_args)
    print ("ETL CLASS: {cls}\n"
           "FILE: {path}\n"
           "DOC: {doc}\n"
           "PARAMETERS: {params}\n").format(cls=clsname, path=filepath,
                                            doc=doc, params=params)


#=================================================
# LAST ALWAYS!
#=================================================

@parser.callback("--run-etl", exclusive=GROUP_OP, action="store", nargs="+",
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

    _fail_if_no_force("--run-etl", flags, conn_data)

    nw = db.YatelNetwork(**conn_data)

    etl.execute(nw, etl_instance, *params)

    nw.confirm_changes()


#===============================================================================
# FUNCTION
#===============================================================================

def _fail_if_no_force(cmd, flags, conn_data):
    if not flags.force and db.exists(**conn_data):
        msg = ("There is an existing 'YatelNetwork' in the conection '{}' and "
               "the command '{}' will altered it. If you want to destroy it "
               "anyway use the option '-f' or '--force' along with "
               "the command '{}'").format(db.to_uri(**conn_data), cmd, cmd)
        parser.error(msg)


def main():
    """Run yatel cli tools

    """
    args = sys.argv[1:] or ["--help"]
    if "--full-stack" in args:
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
