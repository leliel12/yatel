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
import argparse

import yatel
from yatel import db
from yatel import remote
from yatel.conversors import yyf2yatel, yjf2yatel

import caipyrinha


#===============================================================================
# CLI parser
#===============================================================================

parser = caipyrinha.Caipyrinha(prog=yatel.PRJ,
                               description=yatel.SHORT_DESCRIPTION)
parser.add_argument("--version", action='version',
                    version="%(prog)s {}".format(yatel.STR_VERSION))
parser.add_argument("--no-gui", action="store_true")


@parser.callback(action="store", metavar="CONNECTION")
def database(flags, returns):
        """database to be open with yatel

        The conn string is like: 'sqlite:///[DATABASE]' or
        'mysql://USER:PASSWORD@HOST:PORT/DATABASE' or
        'postgres://USER:PASSWORD@HOST:PORT/DATABASE'.

        """
        return db.parse_uri(flags.database, create=False)


@parser.callback(exclusive="ex0", action="store",
                   metavar="filename.<EXT>", exit=0)
def exportdb(flags, returns):
    """Export the given database to YYF or YJF format. Extension must be yyf,
    yaml, yml, json or yjf.

    """
    ext = os.path.splitext(flags.exportdb)[-1].lower()
    exporter = None
    kwargs = {}
    if ext in (".yjf", ".json"):
        exporter = yjf2yatel.dump
        kwargs["indent"] = 2
        kwargs["ensure_ascii"] = True
    elif ext in (".yyf", ".yaml", ".yml"):
        exporter = yyf2yatel.dump
        kwargs["default_flow_style"] = False
    else:
      parser.error("Invalid extension '{}'".format(ext))

    conn_data = returns.database
    conn_data["create"] = False
    conn = db.YatelNetwork(**conn_data)
    with open(flags.exportdb, "w") as fp:
        exporter(conn.haplotypes_iterator(), conn.facts_iterator(),
                 conn.edgest_iterator(), conn.versions_iterator(),
                 stream=fp, **kwargs)
        print("Dumped '{}' to '{}'".format(conn.name, flags.exportdb))


@parser.callback(exclusive="ex0", action="store",
                    metavar="filename.<EXT>", exit=0)
def importdb(flags, returns):
    """Import the given YYF or YJF format file to the given database. WARNING:
    Only local databases are allowed

    """
    conn_data = returns.database
    conn_data["create"] = True
    conn = db.YatelNetwork(**conn_data)

    ext = os.path.splitext(flags.importdb)[-1].lower()
    importer = None
    if ext in (".yjf", ".json"):
        importer = yjf2yatel.load
    elif ext in (".yyf", ".yaml", ".yml"):
        importer = yyf2yatel.load
    else:
      parser.error("Invalid extension '{}'".format(ext))
    with open(flags.importdb) as fp:
        for elemlist in importer(fp):
            for elem in elemlist:
                conn.add_element(elem)
    conn.end_creation()


#===============================================================================
# FUNCTION
#===============================================================================

def main():
    """Run yatel

    """
    if "--no-gui" in sys.argv or "--help" in sys.argv:
        parser(sys.argv[1:])
    else:
        from yatel import gui
        gui.run_gui(parser)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    main()
