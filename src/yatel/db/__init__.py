#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.


#===============================================================================
# FUTURE
#===============================================================================


from __future__ import absolute_import


#===============================================================================
# DOCS
#===============================================================================

"""


"""


#===============================================================================
# META
#===============================================================================

__version__ = "0.1"
__license__ = "GPL3"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2010-09-14"


#===============================================================================
# IMPORTS
#===============================================================================

import string
import datetime
import inspect

import elixir

import sqlalchemy
from sqlalchemy import orm, schema

from yatel import util
from yatel import haps, nd, facts


#===============================================================================
# CONSTANTS
#===============================================================================

DB_SCHEMAS = {
    "memory": string.Template("sqlite:///:memory:"),
    "sqlite": string.Template("sqlite:///$path"),
    "mysql": string.Template("mysql://$user:$password@$host:$port/$name")
}


#===============================================================================
# ENTITY PROXY
#===============================================================================

class _EntityProxy(object):

    def __init__(self, **kwargs):
        self._data = {}
        for k, v in kwargs.items():
            assert issubclass(v, elixir.Entity)
            self._data[k] = v

    def __repr__(self):
        return "<Entities: %s>" % ", ".join(self.keys())

    def __getattr__(self, k):
        return self._data[k]

    def __getitem__(self, k):
        return self._data[k]

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()


#===============================================================================
# CONNECTION
#===============================================================================

class Connection(object):

    def __init__(self, db, create=False, echo=False,
                 autoflush=True, metadata=None, **kwargs):

        # Retrieve schema and setup schema
        try:
            stemplate = DB_SCHEMAS[db]
        except:
            msg = "Unknow schema '%s'" % schema
            raise ValueError(msg)
        try:
            self._conn_str = stemplate.substitute(**kwargs)
        except KeyError as err:
            msg = "DB '%s' need argument(s) '%s'" % (db, ", ".join(err.args))
            raise TypeError(msg)

        # The fourths steps of sqlalchemy
        self._engine = sqlalchemy.create_engine(self._conn_str, echo=echo)
        self._session = orm.scoped_session(orm.sessionmaker(autoflush=autoflush,
                                                            bind=self._engine))
        self._metadata = metadata if metadata != None else schema.MetaData()
        self._metadata.bind = self._engine

        # Entities
        from yatel.db import entities
        ents = entities.create(self._session, self._metadata)
        self._entities = _EntityProxy(**ents)
        del entities

        # Create
        elixir.setup_all(create)

    def __repr__(self):
        return "<Connection (%s) at %s>" % (self._conn_str, hex(id(self)))

    def write(self, force_insert=False, force_update=False, **yatel_objs):
        """Store NetworkDescriptor and Facts instances in this Database"""
        
        def write_nd(nd):
            pass
        
        def write_hap(hap):
            pass
        
        def write_fact(fact):
            pass
        
        for obj in yatel_objs:
            if isinstance(obj, nd.NetworkDescriptor):
                write_nd(obj)
            elif isinstance(obj, haps.Haplotype):
                write_hap(obj)
            elif isinstance(obj, facts.Fact):
                write_fact(obj)
            else:
                msg = "Invalid type '%s'" % str(type(obj))
                raise TypeError(msg)
             
            
    def read(self):
        pass
    
    def delete(self, nw):
        pass

    # session proxies
    def execute(self, *args, **kwargs):
        self._session.execute(*args, **kwargs)
        
    def commit(self, *args, **kwargs):
        self._session.commit(*args, **kwargs)

    def rollback(self, *args, **kwargs):
        self._session.rollback(*args, **kwargs)
        
    def close(self, *args, **kwargs):
        self._session.close(*args, **kwargs)
        
    @property
    def session(self):
        return self._session

    @property
    def metadata(self):
        return self._metadata

    @property
    def engine(self):
        return self._engine

    @property
    def entities(self):
        return self._entities

    @property
    def connection_str(self):
        return self._conn_str


#===============================================================================
# FUNCTIONS
#===============================================================================

def connect(*args, **kwargs):
    return Connection(*args, **kwargs)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

