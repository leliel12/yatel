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
#===============================================================================ç

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

app = _FlaskMock()

manager = Manager(app, with_default_commands=False)

#===============================================================================
# OPTIONS
#===============================================================================

# manager.add_option(
#     "-k", "--full-stack", dest="full-stack", required=False, type=bool
# )

# manager.add_option(
#     "-l", "--log", dest="log", required=False, type=bool
# )

#===============================================================================
# COMMANDS
#===============================================================================
RETURNS = ""                                                                    # what is returns?


@manager.command
def list():
    """List all available connection strings in yatel"""
    for engine in db.ENGINES:
        print "{}: {}".format(engine, db.ENGINE_URIS[engine])


@manager.option(dest="database", help="the database host")
def database(database):
    """Database to be open with yatel (see yatel list)

    """
    return db.parse_uri(database, log=log or None)                          # how to use log?


@manager.option(dest="level", help="the test level")
def test(level):
    """Run all yatel test suites

    """
    tests.run_tests(level)


@manager.option(dest="mode", choices=("r", "w", "a"), help="the option to open database")
def mode(mode):
    """The mode to open the database [r|w|a]"""
    if RETURNS.database:
        RETURNS.database["mode"] = mode


@manager.command
def describe():
    """Print information about the network"""
    conn_data = RETURNS.database
    nw = db.YatelNetwork(**conn_data)
    pprint.pprint(dict(nw.describe()))

    
@manager.option(dest="filename", default="FILENAME.EXT", help="the filename", type=argparse.FileType("w"))
def dump(dump_file):
    """Export the given database to EXT format.

    """
    file_name, ext = dump_file.name.rsplit(".", 1)                              # it is mandatory to set them lower case?
    conn_data = RETURNS.database
    nw = db.YatelNetwork(**conn_data)
    io.dump(ext=ext, nw=nw, stream=dump_file)


@manager.option(dest="filename", default="FILENAME.json", help="the filename")
def backup(filename):
    """Like dump but always create a new file with the format 'filename_template<TIMESTAMP>.EXT'.

    """
    fname, ext = filename.rsplit(".", 1)

    fpath = "{}{}.{}".format(fname, datetime.datetime.utcnow().isoformat(), ext)

    conn_data = RETURNS.database
    nw = db.YatelNetwork(**conn_data)

    with open(fpath, 'w') as fp:
        io.dump(ext=ext.lower(), nw=nw, stream=fp)


@manager.option(dest="load_file", default="FILENAME.EXT", help="the filename", type=argparse.FileType())
def load(load_file):
    """Import the given file to the given database.

    """
    ext = load_file.name.rsplit(".", 1)[-1].lower()
    conn_data = RETURNS.database
    nw = db.YatelNetwork(**conn_data)
    io.load(ext=ext, nw=nw, stream=load_file)
    nw.confirm_changes()


@manager.option(dest="database", default="database", help="the connection string")
def copy(database):
    """Copy the database of `database` to this connection"""

    to_conn_data = db.parse_uri(database, mode=db.MODE_WRITE, log=flags.log)    # how we use the flags.log?
    _fail_if_no_force("--copy", to_conn_data)

    to_nw = db.YatelNetwork(**to_conn_data)

    conn_data = RETURNS.database
    from_nw = db.YatelNetwork(**conn_data)

    db.copy(from_nw, to_nw)
    to_nw.confirm_changes()


@manager.option(dest="config", default="config.json", help="the config file")
@manager.option(dest="filename", default="filename.wsgi", help="the file name")
def createwsgi(config, filename):
    """Create a new wsgi file for a given configuration"""
    filename_ext = filename.rsplit(".", 1)[-1].lower()
    if filename_ext != "wsgi":
        msg = "Invalid extension '{}'. must be 'wsgi'".format(filename_ext)
        raise ValueError(msg)
    with open(filename, "w") as fp:
        fp.write(server.get_wsgi_template(config))


@manager.option(dest="config_file", default="config.json", help="the file name", type=argparse.FileType('w'))
def createconf(config_file):
    """Create a new configuration file for runserver"""
    ext = config_file.name.rsplit(".", 1)[-1].lower()
    if ext != "json":
        raise ValueError("Invalid extension '{}'. must be 'json'".format(ext))
    tpl = server.get_conf_template()
    fp = config_file                                                                 # this must be a file?
    fp.write(tpl)


@manager.option(dest="config", default="config.json", help="the config file")
@manager.option(dest="host_port", help="the host:port")
def runserver(config, host_port):
    """Run yatel as http server with a given config file"""
    host, port = host_port.split(":", 1)
    with open(config) as fp:
        data = json.load(fp)
    srv = server.from_dict(data)
    srv.run(host=host, port=int(port), debug=data["CONFIG"]["DEBUG"])


@manager.option(dest="etl_file", default="ETL_FILENAME.py", help="the file name", type=argparse.FileType('w'))
def createetl(etl_file):
    """Create a template file for write yout own etl"""
    ext = etl_file.name.rsplit(".", 1)[-1].lower()
    if ext != "py":
        raise ValueError("Invalid extension '{}'. must be 'py'".format(ext))
    tpl = etl.get_template()
    fp = etl_file
    fp.write(tpl)


@manager.option(dest="module_path_file", help="path/to/the/module.py")
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
@manager.option(dest="module_path_file", help="path/to/the/module.py")
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


#===============================================================================
# MAIN FUNCTION
#===============================================================================

def main():
    args = sys.argv[1:] or ["--help"]
    if "--full-stack" in args:
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
