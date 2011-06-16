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
#from sqlalchemy.schema import MetaData

from yatel import util


#===============================================================================
# CONSTANTS
#===============================================================================

TYPE_PARSER = util.StringParser(
    int=(unicode, int),
    float=(unicode, float),
    bool=(unicode, lambda v: v == "True"),
    str=(unicode, str),
    unicode=(unicode, unicode),
    datetime=(unicode,
              lambda s: datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f"))
)

DB_SCHEMAS = {
    "memory": string.Template("sqlite:///:memory:"),
    "sqlite": string.Template("sqlite:///$path"),
    "mysql": string.Template("mysql://$user:$password@$host:$port/$name")
}

#===============================================================================
# ENTITIES
#===============================================================================

_et = set()

def register(cls):
    assert inspect.isclass(cls)
    _et.add(cls)
    return cls


def unregister(cls):
    _et.pop(cls)


def registered_list():
    return list(_et)


def create_entities(metadata, session):
    entities = {}
    for ent in _et:
        ename = ent.__name__
        edict = dict((k, v) for k, v in vars(ent).items()
                     if not k.startswith("_"))
        uop = dict(edict["using_options"])
        uop.update(metadata=metadata, session=session)
        print uop
        edict["using_options"] = elixir.using_options(**uop)
        entities[ename] = type(ename, (elixir.Entity, ), edict)
    return entities


#===============================================================================
# NETWORK
#===============================================================================

@register
class NetworkEntity(object):
    name = elixir.Field(elixir.UnicodeText)
    using_options = {"tablename": "networks"}


"""
#===============================================================================
# NETWORK DETAILS
#===============================================================================

class NetworkDetail(elixir.Entity):

    distance_value = elixir.Field(elixir.Float)

    network = elixir.ManyToOne("Network")
    seq_0 = elixir.ManyToOne("Sequence")
    seq_1 = elixir.ManyToOne("Sequence")


#===============================================================================
# DISTANCE
#===============================================================================

class Distance(elixir.Entity):

    name = elixir.Field(elixir.UnicodeText)
    description = elixir.Field(elixir.UnicodeText)

    details = elixir.OneToMany("DistanceDetail")


#===============================================================================
# DISTANCE DETAIL
#===============================================================================

class DistanceDetail(elixir.Entity):

    distance_value = elixir.Field(elixir.Float)

    seq_0 = elixir.ManyToOne("Sequence")
    seq_1 = elixir.ManyToOne("Sequence")
    metric = elixir.ManyToOne("Metric")
    distance = elixir.ManyToOne("Distance", inverse="details")


#===============================================================================
# METRIC
#===============================================================================

class Metric(elixir.Entity):

    name = elixir.Field(elixir.UnicodeText)
    description = elixir.Field(elixir.UnicodeText)

    distance_details = elixir.OneToMany("DistanceDetail")


#===============================================================================
# SEQUENCES
#===============================================================================

class Sequence(elixir.Entity):

    name = elixir.Field(elixir.UnicodeText)
    description = elixir.Field(elixir.UnicodeText)

    attributes = elixir.OneToMany("SequenceAttribute")
    distance_details = elixir.OneToMany("DistanceDetail")
    network_details = elixir.OneToMany("NetworkDetail")


#===============================================================================
# SEQUENCE ATTRIBUTES
#===============================================================================

class SequenceAttribute(elixir.Entity):

    _value = elixir.Field(elixir.UnicodeText, colname="value")
    att_type = elixir.Field(elixir.Enum(FORMATTER.valid_types))

    seq = elixir.ManyToOne("Sequence")

    @property
    def value(self):
        return FORMATTER.parse(self.att_type, self._value)

    @property
    def value(self, v):
        self.att_type, self._value = FORMATTER.format(v)


#===============================================================================
# FACT
#===============================================================================

class Fact(elixir.Entity):

    name = elixir.Field(elixir.UnicodeText)
    description = elixir.Field(elixir.UnicodeText)

    seq = elixir.ManyToOne("Sequence")
    attributes = elixir.OneToMany("FactAttribute")


#===============================================================================
# FACT ATTS
#===============================================================================

class FactAttribute(elixir.Entity):

    _value = elixir.Field(elixir.UnicodeText, colname="value")
    att_type = elixir.Field(elixir.Enum(FORMATTER.valid_types))

    seq = elixir.ManyToOne("Sequence")

    @property
    def value(self):
        return FORMATTER.parse(self.att_type, self._value)

    @property
    def value(self, v):
        self.att_type, self._value = FORMATTER.format(v)

"""


#===============================================================================
# ENTITY PROXY
#===============================================================================

class EntityProxy(object):

    def __init__(self, **kwargs):
        self._data = {}
        for k, v in kwargs.items():
            assert issubclass(v, elixir.Entity)
            self._data[k] = v

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
# Context
#===============================================================================

class Context(object):

    # INIT #####################################################################
    def __init__(self, db, create=False, echo=False, autoflush=True,
                 transactional=True, metadata=None, **kwargs):

        # retrieve schema
        try:
            stemplate = DB_SCHEMAS[db]
        except:
            msg = "Unknow schema '%s'" % schema
            raise ValueError(msg)

        # setup schema
        try:
            self._conn_str = stemplate.substitute(**kwargs)
        except KeyError as err:
            msg = "Schema '%s' need argument(s) '%s'" % (schema,
                                                         ", ".join(err.args))
            raise TypeError(msg)

        # The fourths steps of sqlalchemy
        self._engine = sqlalchemy.create_engine(self._conn_str, echo=echo)
        self._session = orm.scoped_session(orm.sessionmaker(autoflush=autoflush,
                                                            transactional=transactional,
                                                            bind=self._engine))
        self._metadata = metadata if metadata != None else schema.ThreadLocalMetaData()
        self._metadata.bind = self._engine

        # create entities and store it
        entities = create_entities(metadata=self._metadata, session=self._session)
        self._entities = EntityProxy(**entities)

        #create
        elixir.setup_all(create)

    # INIT #####################################################################

    @property
    def entities(self):
        return self._entities

    @property
    def connection_str(self):
        return self._conn_str


#===============================================================================
# FUNCTIONAL SUGAR
#===============================================================================

def connect(*args, **kwargs):
    return Context(*args, **kwargs)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

