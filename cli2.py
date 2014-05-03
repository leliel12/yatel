#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pprint
import datetime
import argparse
import json

from flask.ext.script import Manager

from yatel import db, tests, server, etl
from yatel import io


#===============================================================================
# MANAGER
#===============================================================================

class _FlaskMock(object):
    """This class only mock the flask object to use flask script stand alone

    """
    def __init__(self, *a, **kw):
        if kw:
            self.options = kw
    def __getattr__(self, *a, **kw):
        return _FlaskMock()
    def __call__(self, *a, **kw):
        return _FlaskMock()
    def __exit__(self, *a, **kw):
        return _FlaskMock()
    def __enter__(self, *a, **kw):
        return _FlaskMock()

manager = Manager(_FlaskMock, with_default_commands=False)

#===============================================================================
# OPTIONS
#===============================================================================

manager.add_option(
    "-k", "--full-stack", dest="full-stack", required=False, action="store_true"
)

manager.add_option(
    "-l", "--log", dest="log", required=False, action="store_true"
)

#===============================================================================
# CONSTANTS
#===============================================================================
RETURNS = ""                                                                    # what is returns?
CONNECTION_STRING_HELP = """The given string is parsed according to the RFC 1738
spec.

"""

FILENAME_HELP = """Path al archivo de los datos.

El formato del contenido del archivo es determinado por la extension del mismo.
Las extensiones pueden ser: {}

""".format(", ".join(io.PARSERS.keys()))

CONFIG_STRING_HELP = """"""
WSGI_STRING_HELP = """"""
HOSTNAME_STRING_HELP = """"""
ETL_STRING_HELP = """ETL_FILENAME.py"""

DEFAULT_CONFIG = "config.json"
DEFAULT_WSGI = "filename.wsgi"
DEFAULT_FILENAME = "FILENAME.EXT"
DEFAULT_ETL = "ETL_FILENAME.py"

#===============================================================================
# COMMANDS
#===============================================================================

@manager.command
def list():
    """List all available connection strings in yatel"""
    for engine in db.ENGINES:
        print "{}: {}".format(engine, db.ENGINE_URIS[engine])


@manager.option(dest="level", help="the test level")
def test(level):
    """Run all yatel test suites

    """
    tests.run_tests(level)


@manager.option(dest="database", help=CONNECTION_STRING_HELP)
def describe(database):
    """Print information about the network. Based """
    nw = get_database(database)
    pprint.pprint(dict(nw.describe()))

    
@manager.option(dest="dump_file", default=DEFAULT_FILENAME, help=FILENAME_HELP,
                                                    type=argparse.FileType("w"))
@manager.option(dest="database", help=CONNECTION_STRING_HELP)
def dump(database, dump_file):
    """Export the given database to EXT format.

    """
    file_name, ext = dump_file.name.rsplit(".", 1)                              # it is mandatory to set them lower case?
    nw = get_database(database)
    io.dump(ext=ext, nw=nw, stream=dump_file)


@manager.option(dest="backup_file", default=DEFAULT_FILENAME, help=FILENAME_HELP)
@manager.option(dest="database", help=CONNECTION_STRING_HELP)
def backup(database, backup_file):
    """Like dump but always create a new file with the format
    'filename_template<TIMESTAMP>.EXT'.

    """
    fname, ext = backup_file.rsplit(".", 1)

    fpath = "{}{}.{}".format(fname, datetime.datetime.utcnow().isoformat(), ext)

    nw = get_database(database)

    with open(fpath, 'w') as fp:
        io.dump(ext=ext.lower(), nw=nw, stream=fp)


@manager.option(dest="load_file", default=DEFAULT_FILENAME, help=FILENAME_HELP,
                                                    type=argparse.FileType("r"))
@manager.option(dest="database", help=CONNECTION_STRING_HELP)
def load(database, load_file):
    """Import the given file to the given database.

    """
    ext = load_file.name.rsplit(".", 1)[-1].lower()
    nw = get_database(database)
    io.load(ext=ext, nw=nw, stream=load_file)                                   # donde le pasamos el modo (reemplazar|agregar)?
    nw.confirm_changes()

@manager.option(dest="database_orig", help=CONNECTION_STRING_HELP)
@manager.option(dest="database_dest", help=CONNECTION_STRING_HELP)
def copy(database_orig, database_dest):
    """Copy the database of `database` to this connection"""

    # _fail_if_no_force("--copy", to_conn_data)                                 # pasar esto a get_database
    to_nw = get_database(database_dest)
    from_nw = get_database(database_orig)
    db.copy(from_nw, to_nw)
    to_nw.confirm_changes()


@manager.option(dest="config", default=DEFAULT_CONFIG, help=CONFIG_STRING_HELP)
@manager.option(dest="filename", default=DEFAULT_WSGI, help=WSGI_STRING_HELP)
def createwsgi(config, filename):
    """Create a new wsgi file for a given configuration"""
    filename_ext = filename.rsplit(".", 1)[-1].lower()
    if filename_ext != "wsgi":
        msg = "Invalid extension '{}'. must be 'wsgi'".format(filename_ext)
        raise ValueError(msg)
    with open(filename, "w") as fp:
        fp.write(server.get_wsgi_template(config))


@manager.option(dest="config_file", default=DEFAULT_CONFIG,
                        help=CONFIG_STRING_HELP, type=argparse.FileType('w'))
def createconf(config_file):
    """Create a new configuration file for runserver"""
    ext = config_file.name.rsplit(".", 1)[-1].lower()
    if ext != "json":
        raise ValueError("Invalid extension '{}'. must be 'json'".format(ext))
    tpl = server.get_conf_template()
    fp = config_file                                                                 # this must be a file?
    fp.write(tpl)


@manager.option(dest="config", default=DEFAULT_CONFIG, help=CONFIG_STRING_HELP)
@manager.option(dest="host_port", help=HOSTNAME_STRING_HELP)
def runserver(config, host_port):
    """Run yatel as http server with a given config file"""
    host, port = host_port.split(":", 1)
    with open(config) as fp:
        data = json.load(fp)
    srv = server.from_dict(data)
    srv.run(host=host, port=int(port), debug=data["CONFIG"]["DEBUG"])


@manager.option(dest="etl_file", default=DEFAULT_ETL, help=ETL_STRING_HELP,
                                                    type=argparse.FileType('w'))
def createetl(etl_file):
    """Create a template file for write yout own etl"""
    ext = etl_file.name.rsplit(".", 1)[-1].lower()
    if ext != "py":
        raise ValueError("Invalid extension '{}'. must be 'py'".format(ext))
    tpl = etl.get_template()
    fp = etl_file
    fp.write(tpl)


@manager.option(dest="module_path_file", help=ETL_STRING_HELP)
def describeetl(module_path_file):
    """Return a list of parameters and documentataton about the etl

    The argument is in the format path/to/module.py

    The BaseETL subclass must be names after ETL

    """
    etl_cls = etl.etlcls_from_module(module_path_file, "ETL")
    doc = etl_cls.__doc__ or "-"
    params = ", ".join(etl_cls.setup_args)
    print ("ETL CLASS: {cls}\n"
           "FILE: {path}\n"
           "DOC: {doc}\n"
           "PARAMETERS: {params}\n").format(cls=clsname, path=module_path_file, # what is clsname???
                                            doc=doc, params=params)


@manager.option(dest="args", help="Arguments for etl excecute", nargs="+")
@manager.option(dest="module_path_file", help=ETL_STRING_HELP)
def runetl(module_path_file, args):
    """Run one or more etl inside of a given script.

    The first argument is in the format path/to/module.py
    the second onwards parameter are parameters of the setup method of the
    given class.

    """
    etl_cls = etl.etlcls_from_module(module_path_file, "ETL")
    etl_instance = etl_cls()

    conn_data = RETURNS.database

    _fail_if_no_force("--run-etl", conn_data)

    nw = db.YatelNetwork(**conn_data)

    etl.execute(nw, etl_instance, *args)

    nw.confirm_changes()


def _fail_if_no_force(cmd, conn_data):
    if db.exists(**conn_data):
        msg = ("There is an existing 'YatelNetwork' in the conection '{}' and "
               "the command '{}' will altered it. If you want to destroy it "
               "anyway use the option '-f' or '--force' along with "
               "the command '{}'").format(db.to_uri(**conn_data), cmd, cmd)
        print msg                                                               # this should be a logger


def get_database(database):
    log = manager.app.options['log']
    #                                                                           # aca no se deberia comprobar con _fail_if_no_force?
    return db.YatelNetwork(**db.parse_uri(database, log=log))


#===============================================================================
# MAIN FUNCTION
#===============================================================================

def main():
    args = sys.argv[1:] or ["--help"]
    if set(args).intersection(["--full-stack", "-k"]):
        manager.run()
    else:
        try:
            manager.run()
        except Exception as err:
            print unicode(err)



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    main()
