#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#==============================================================================
# DOCS
#==============================================================================

"""Launcher of yatel cli tools

"""


#==============================================================================
# IMPORTS
#==============================================================================

import sys
import pprint
import datetime
import argparse
import json
import functools

from flask.ext.script import Manager, Command, Option
from flask.ext.script.commands import InvalidCommand

import yatel
from yatel import db, tests, server, etl
from yatel import yio


#===============================================================================
# MANAGER
#===============================================================================

class _FlaskMock(object):
    """This class only mock the flask object to use flask script stand alone

    """
    def __init__(self, *a, **kw):
        self.options = kw
    def __getattr__(self, *a, **kw):
        return _FlaskMock()
    def __call__(self, *a, **kw):
        return _FlaskMock(*a, **kw)
    def __exit__(self, *a, **kw):
        return _FlaskMock()
    def __enter__(self, *a, **kw):
        return _FlaskMock()

manager = Manager(
    _FlaskMock,
    description=yatel.SHORT_DESCRIPTION,
    with_default_commands=False
)


#==============================================================================
# DECOTATOR
#==============================================================================

def run_wrapper(func):
    """Convert any exception inside tun into flask script exception

    """
    @functools.wraps(func)
    def _dec(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            raise InvalidCommand(str(err))
    return _dec


def command(name):
    """Clean way to register class based commands

    """
    def _dec(cls):
        instance = cls()
        instance.run = run_wrapper(instance.run)
        manager.add_command(name, instance)
        return cls
    return _dec


#===============================================================================
# OPTIONS
#===============================================================================

manager.add_option(
    "-k", "--full-stack", dest="full-stack", required=False,
    action="store_true", help="If the command fails print all Python stack"
)

manager.add_option(
    "-l", "--log", dest="log", required=False,
    action="store_true", help="Enable engine logger"
)

manager.add_option(
    "-f", "--force", dest="log", required=False,
    action="store_true",
    help=("If a database is try to open in 'w' or 'a' and a Yatel Network "
          "is discovered overwrite it")
)


#==============================================================================
# CUSTOM TYPES
#==============================================================================

class Database(object):
    """This class parse and validate the open mode of a databases"""

    def __init__(self, mode):
        self.mode = mode

    def __call__(self, toparse):
        log = "--log" in sys.argv or "-l" in sys.argv
        force = "--force" in sys.argv or "-f" in sys.argv
        data = db.parse_uri(toparse)
        if self.mode in (db.MODE_WRITE, db.MODE_APPEND) and db.exists(**data):
            if not force:
                msg = (
                    "You are trying to open the db '{}' in '{}' mode, but "
                    "it contains a already existing network. Please use "
                    "-f/--force for ignore this warning and destroy the "
                    "existing data"
                ).format(toparse, self.mode)
                raise InvalidCommand(msg)

        data.update(log=log, mode=self.mode)
        return db.YatelNetwork(**data)


#===============================================================================
# COMMANDS
#===============================================================================

@command("list")
class List(Command):
    """List all available connection strings in yatel"""

    def run(self):
        for engine in db.ENGINES:
            print "{}: {}".format(engine, db.ENGINE_URIS[engine])


@command("test")
class Test(Command):
    """Run all yatel test suites

    """

    option_list = [
        Option(dest='level', type=int, help="Test level [0|1|2]")
    ]

    def run(self, level):
        tests.run_tests(level)


@command("describe")
class Describe(Command):
    """Print information about the network"""

    option_list = [
        Option(
            dest='database', type=Database(db.MODE_READ),
            help="Connection string to database according to the RFC 1738 spec."
        ),
    ]

    def run(self, database):
        lines = []
        desc = database.describe()
        lines.append(u"Haplotypes:")
        for k, v in desc.haplotype_attributes.items():
            lines.append(u"\t{}: {}".format(unicode(k), unicode(v)))
        lines.append(u"Edges:")
        for k, v in desc.edge_attributes.items():
            lines.append(u"\t{}: {}".format(unicode(k), unicode(v)))
        lines.append(u"Facts:")
        for k, v in desc.fact_attributes.items():
            lines.append(u"\t{}: {}".format(unicode(k), unicode(v)))
        lines.append("")

        print u"\n".join(lines)


@command("dump")
class Dump(Command):
    """Export the given database to file.
    The extension of a file determine the format

    """

    option_list = [
        Option(
            dest='database', type=Database(db.MODE_READ),
            help="Connection string to database according to the RFC 1738 spec."
        ),
        Option(
            dest='dumpfile', type=argparse.FileType("w"),
            help=("File path to dump al the content of the database. "
                  "Suported formats: {}".format(", ".join(yio.PARSERS.keys())))
        )
    ]

    def run(self, database, dumpfile):
        ext = dumpfile.name.rsplit(".", 1)[-1]
        yio.dump(ext=ext.lower(), nw=database, stream=dumpfile)


@command("backup")
class Backup(Command):
    """Like dump but always create a new file with the format
     'backup_file<TIMESTAMP>.EXT'.

     """

    option_list = [
        Option(
            dest='database', type=Database(db.MODE_READ),
            help="Connection string to database according to the RFC 1738 spec."
        ),
        Option(
            dest='backupfile',
            help=("File path template to dump al the content of the database. "
                  "Suported formats: {}".format(", ".join(yio.PARSERS.keys())))
        )
    ]

    def run(self, database, backupfile):
        fname, ext = backupfile.rsplit(".", 1)
        fpath = "{}{}.{}".format(
            fname, datetime.datetime.utcnow().isoformat(), ext
        )
        with open(fpath, 'w') as fp:
            yio.dump(ext=ext.lower(), nw=database, stream=fp)


@command("load")
class Load(Command):
    """Import the given file to the given database.

    """

    option_list = [
        Option(
            dest='database', type=Database(db.MODE_WRITE),
            help="Connection string to database according to the RFC 1738 spec."
        ),
        Option(
            dest='datafile', type=argparse.FileType("r"),
            help=("File path of the existing data file. "
                  "Suported formats: {}".format(", ".join(yio.PARSERS.keys())))
        )
    ]

    def run(self, database, datafile):
        ext = datafile.name.rsplit(".", 1)[-1]
        yio.load(ext=ext.lower(), nw=database, stream=datafile)
        database.confirm_changes()


@command("copy")
class Copy(Command):
    """Copy a yatel network to another database

    """

    option_list = [
        Option(
            dest='database_from', type=Database(db.MODE_READ),
            help="Connection string to database according to the RFC 1738 spec."
        ),
        Option(
            dest='database_to', type=Database(db.MODE_WRITE),
            help="Connection string to database according to the RFC 1738 spec."
        )
    ]

    def run(self, database_from, database_to):
        db.copy(database_from, database_to)
        database_to.confirm_changes()


@command("createconf")
class CreateConf(Command):
    """Create a new configuration file for yatel"""

    option_list = [
        Option(
            dest='config', type=argparse.FileType("w"),
            help=("File path of the config file. ie: config.json. "
                  "Suported formats: {}".format(", ".join(yio.PARSERS.keys())))
        ),

    ]

    def run(self, config):
       config.write(server.get_conf_template())


@command("createwsgi")
class CreateWSGI(Command):
    """Create a new wsgi file for a given configuration"""

    option_list = [
        Option(dest='config',
               help="File path of the config file. ie: config.json"),
        Option(
            dest='filename', type=argparse.FileType("w"),
            help="WSGI filepath. ie: my_wsgi.py"
        )
    ]

    def run(self, config, filename):
        filename.write(server.get_wsgi_template(config))


@command("runserver")
class Runserver(Command):
    """Run yatel as development http server with a given config file"""

    option_list = [
        Option(
            dest='config',  type=argparse.FileType("r"),
            help="File path of the config file. ie: config.json"
        ),
        Option(
            dest='host_port',
            help="Host and port to run yatel in format HOST:PORT"
        )
    ]

    def run(self, config, host_port):
        host, port = host_port.split(":", 1)
        data = json.load(config)
        srv = server.from_dict(data)
        srv.run(host=host, port=int(port), debug=data["CONFIG"]["DEBUG"])


@command("createetl")
class CreateETL(Command):
    """Create a template file for write yout own etl"""

    option_list = [
        Option(
            dest='etlfile', type=argparse.FileType("w"),
            help="Python ETL filepath. ie: my_new_etl.py"
        )
    ]

    def run(self, etlfile):
        ext = etlfile.name.rsplit(".", 1)[-1].lower()
        if ext != "py":
            raise ValueError(
                "Invalid extension '{}'. must be 'py'".format(ext)
            )
        tpl = etl.get_template()
        fp = etlfile
        fp.write(tpl)


@command("describeetl")
class DescribeETL(Command):
    """Return a list of parameters and documentation about the etl
    The argument is in the format path/to/module.py
    The BaseETL subclass must be named after ETL

    """

    option_list = [
        Option(dest='etlfile', help="Python ETL filepath. ie: my_new_etl.py")
    ]

    def run(self, etlfile):
        etl_cls = etl.etlcls_from_module(etlfile, "ETL")
        doc = etl_cls.__doc__ or "-"
        params = ", ".join(etl_cls.setup_args)
        print ("FILE: {path}\n"
               "DOC: {doc}\n"
               "PARAMETERS: {params}\n"
        ).format(path=etlfile,doc=doc, params=params)


@command("runetl")
class RunETL(Command):
    """Run one or more etl inside of a given script.

    The first argument is in the format path/to/module.py
    the second onwards parameter are parameters of the setup method of the
    given class.

    """

    option_list = [
        Option(dest='etlfile', help="Python ETL filepath. ie: my_new_etl.py"),
        Option(dest="args", help="Arguments for etl to excecute", nargs="+"),
        Option(
            dest='database', type=Database(db.MODE_WRITE),
            help="Connection string to database according to the RFC 1738 spec."
        )
    ]

    def run(self, database, etlfile, args):
        etl_cls = etl.etlcls_from_module(etlfile, "ETL")
        etl_instance = etl_cls()
        etl.execute(database, etl_instance, *args)
        database.confirm_changes()


#===============================================================================
# MAIN FUNCTION
#===============================================================================

def main():
    try:
        manager.run()
    except InvalidCommand as err:
        print(err)
        sys.exit(1)



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    main()
