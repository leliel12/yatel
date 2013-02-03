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
import urlparse
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

        The conn string is like: 'sqlite://[DATABASE]' or
        'mysql://USER:PASSWORD@HOST:PORT/DATABASE' or
        'postgres://USER:PASSWORD@HOST:PORT/DATABASE'. If you want to connect
        to a remote yatel use 'yatel://HOST@PORT'

        """
        parsed = urlparse.urlparse(flags.database)
        engine = parsed.scheme
        conf = {}
        if engine == "yatel":
            fullpath = parsed.netloc + parsed.path
            host, port = [p for p in fullpath.split(":", 1)]
            conf = {"engine": engine, "host": host, "port": int(port)}
        elif engine not in db.ENGINES:
            raise ValueError(db.ENGINES)
        elif engine in db.FILE_ENGINES:
            dbname = parsed.netloc + parsed.path
            conf = {"engine": engine, "dbname": dbname}
        else:
            dbname = parsed.path[1:]
            auth, loc = parsed.netloc.split("@", 1)
            user, password = [p for p in auth.split(":")]
            host, port = [p for p in loc.split(":")]
            conf = {"engine": engine, "dbname": dbname, "user": user,
                     "host": host, "port": int(port), "password": password}
        engine = conf.pop("engine")
        if engine != "yatel":
            name = conf.pop("dbname")
            conn = db.YatelConnection(engine, name, **conf)
            return conn
        else:
            return remote.YatelRemoteClient(host=conf["host"],
                                             port=conf["port"])


@parser.callback(exclusive="ex0", action="store", metavar="HOST:PORT", exit=0)
def serve(flags, returns):
    """serve the given yatel connection via web server via JSON-RPC

    """
    def serve_parser(p):
        host, port = p.split(":")
        port = int(port)
        if not 0 <= port <= 65535:
            raise ValueError("port must be 0-65535")
        return {"host": host, "port": int(port)}


    serve_args = serve_parser(flags.serve)
    conn = returns.database
    if isinstance(conn, remote.YatelRemoteClient):
        parser.error("you can't serve a yatel remote instance")
    if not conn.inited:
        conn.init_yatel_database()
    server = remote.YatelServer(conn)
    server.run(**serve_args)


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
    conn = returns.database
    with open(flags.exportdb, "w") as fp:
        conn.init_yatel_database()
        exporter(conn.iter_haplotypes(), conn.iter_facts(),
                 conn.iter_edges(), conn.iter_versions(),
                 stream=fp, **kwargs)
        print("Dumped '{}' to '{}'".format(conn.name, flags.exportdb))


@parser.callback(exclusive="ex0", action="store",
                    metavar="filename.<EXT>", exit=0)
def importdb(flags, returns):
    """Import the given YYF or YJF format file to the given database. WARNING:
    Only local databases are allowed

    """
    conn = returns.database
    if not isinstance(conn, db.YatelConnection):
        parser.error("Remote yatel are not allowed here")
    ext = os.path.splitext(flags.importdb)[-1].lower()
    importer = None
    if ext in (".yjf", ".json"):
        importer = yjf2yatel.load
    elif ext in (".yyf", ".yaml", ".yml"):
        importer = yyf2yatel.load
    else:
      parser.error("Invalid extension '{}'".format(ext))
    with open(flags.importdb) as fp:
        conn.init_with_values(*importer(fp))




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
