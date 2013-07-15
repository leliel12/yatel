#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Database abstraction layer

This new backend has almost the same method than the original db.py and in the
future will be the only one.

Is developed over web2py ``dal.py``

for testing use:

::

    from yatel import db2 as db

"""


#===============================================================================
# IMPORTS
#===============================================================================

import datetime
import string
import decimal

from yatel.libs import dal
from yatel import dom


#===============================================================================
# EXCEPTIONS
#===============================================================================

# The order to show schema variables, if it not in this list put at the end
VARS_ORDER = ("dbname", "user", "password", "dsn", "host", "port")

SCHEMAS = (
    "sqlite",
    "mysql",
    "postgres",
    #~ "spatialite",
    #~ "sqlite:memory",
    #~ "spatialite:memory",
    #~ "jdbc:sqlite",
    #~ "postgres:psycopg2",
    #~ "postgres:pg8000",
    #~ "jdbc:postgres",
    #~ "mssql",
    #~ "mssql2", # alternate mappings
    #~ "oracle",
    #~ "firebird",
    #~ "db2",
    #~ "firebird_embedded",
    #~ "informix",
    #~ "informixu", # unicode informix
    #~ "google:datastore", # for google app engine datastore
    #~ "google:sql", # for google app engine with sql (mysql compatible)
    #~ "teradata", # experimental
    #~ "imap",
)


SCHEMA_URIS = {
    "sqlite": 'sqlite://${dbname}',
    "spatialite": 'spatialite://${dbname}',
    "sqlite:memory": 'sqlite:memory',
    "spatialite:memory": 'spatialite:memory',
    "jdbc:sqlite": 'jdbc:sqlite://${dbname}',
    "mysql": 'mysql://${user}:${password}@${host}:${port}/${dbname}',
    "postgres": 'postgres://${user}:${password}@${host}:${port}/${dbname}',
    "postgres:psycopg2": 'postgres:psycopg2://${user}:${password}@${host}:${port}/${dbname}',
    "postgres:pg8000": 'postgres:pg8000://${user}:${password}@${host}:${port}/${dbname}',
    "jdbc:postgres": 'jdbc:postgres://${user}:${password}@${host}:${port}/${dbname}',
    "mssql": 'mssql://${user}:${password}@${host}:${port}/${dbname}',
    "mssql2": 'mssql2://${user}:${password}@${host}:${port}/${dbname}',
    "oracle": 'oracle://${user}:${password}@${host}:${port}/${dbname}',
    "firebird": 'firebird://${user}:${password}@${host}:${port}/${dbname}',
    "db2": 'db2://DSN=${dsn};UID=${user};PWD=${password}',
    "firebird_embedded": 'firebird_embedded://${user}:${password}@${dbname}',
    "informix": 'informix://${user}:${password}@${host}:${port}/${dbname}',
    "informixu": 'informixu://${user}:${password}@${host}:${port}/${dbname}',
    "google:datastore": 'google:datastore',
    "google:sql": 'google:sql',
    "teradata": 'teradata://DSN=${dsn};UID=${user};PWD=${password};DATABASE=${dbname}',
    "imap": 'imap://${user}:${password}@${host}:${port}'
}


SCHEMA_VARS = {}
for schema in SCHEMAS:
    tpl = string.Template(SCHEMA_URIS[schema])
    variables = []
    for e, n, b, i in tpl.pattern.findall(tpl.template):
        if n or b:
            variables.append(n or b)
    variables.sort(key=lambda v: VARS_ORDER.index(v)
                                 if v in VARS_ORDER
                                 else len(VARS_ORDER))
    SCHEMA_VARS[schema] = variables


DAL_TYPES = {
    datetime.datetime:
        lambda x: "datetime",
    datetime.time:
        lambda x: "time",
    datetime.date:
        lambda x: "date",
    bool:
        lambda x: "boolean",
    int:
        lambda x: "integer",
    float:
        lambda x: "double",
    str:
        lambda x: "string" if len(x) < 512 else "text",
    unicode:
        lambda x: "string" if len(x) < 512 else "text",
    decimal.Decimal:
        lambda x: "decimal(10,10"
}



#===============================================================================
# ERROR
#===============================================================================

class YatelNetworkError(Exception):
    """Error for use when some *Yatel* logic fail in database."""
    pass


#===============================================================================
# NETWORK
#===============================================================================


class YatelNetwork(object):

    STATUS_CONECTED = "conected"
    STATUS_PREPARED = "prepared"
    STATUS_INITED = "inited"

    ALL_STATUS = (STATUS_CONECTED, STATUS_PREPARED, STATUS_INITED)

    def __init__(self, schema, **kwargs):
        tpl = string.Template(SCHEMA_URIS[schema])
        uri = tpl.substitute(kwargs)
        self._dal = dal.DAL(uri)
        self._status = self.STATUS_CONECTED
        self._base_tables()

    def _validate_status(self, *statuses):
        if self._status not in statuses:
            statuses = map(lambda s: "'{}'".format(s), statuses)
            valid_status = " or ".join(statuses)
            msg = "Network status invalid. Need {}, found '{}'"
            msg = msg.format(statuses, self._status)
            raise YatelNetworkError(msg)

    def _new_attrs(self, attnames, table):
        return set(attnames).difference(table.fields)

    def _base_tables(self):

        try:
            self._dal.define_table(
                'yatel_fields',
                dal.Field("name", "string", notnull=True),
                dal.Field("type", "string", notnull=True),
                dal.Field("is_unique", "boolean", notnull=True),
                dal.Field("reference_to", "string", notnull=False)
            )
        except:
            print self._dal._lastsql

        self._dal.define_table(
            'yatel_versions',
            dal.Field("tag", "string", notnull=True),
            dal.Field("datetime", "datetime", notnull=True),
            dal.Field("comment", "text", notnull=True),
            dal.Field("data", "text", notnull=True)
        )

        self._dal.define_table(
            'haplotypes',
            dal.Field("hap_id", "string", unique=True, notnull=True)
        )

        self._dal.define_table(
            'edges',
            dal.Field("weight", "double", notnull=True)
        )

        self._dal.define_table(
            'facts',
            dal.Field("haplotype", self._dal.haplotypes),
        )

    #===========================================================================
    # INIT FUNCTIONS
    #===========================================================================

    def prepare(self):
        self._validate_status(self.STATUS_CONECTED)
        self._status = self.STATUS_PREPARED

    def add_element(self, elem):
        self._validate_status(self.STATUS_PREPARED)

        # if is an haplotypes
        if isinstance(elem, dom.Haplotype):
            new_attrs_names = self._new_attrs(elem.names_attrs(),
                                              self._dal.haplotypes)
            new_attrs = []
            for aname in new_attrs_names:
                ftype =  DAL_TYPES[type(elem[aname])](elem[aname])
                field = dal.Field(aname, ftype, notnull=False)
                new_attrs.append(field)
            if new_attrs:
                self._dal.define_table(
                    'haplotypes',
                    self._dal.haplotypes,
                    redefine=True, *new_attrs
                )
            attrs = dict(elem.items_attrs())
            attrs.update(hap_id=elem.hap_id)
            self._dal.haplotypes.insert(**attrs)

        # is is a fact
        elif isinstance(elem, dom.Fact):
            new_attrs_names = self._new_attrs(elem.names_attrs(),
                                              self._dal.facts)
            new_attrs = []
            for aname in new_attrs_names:
                ftype =  DAL_TYPES[type(elem[aname])](elem[aname])
                field = dal.Field(aname, ftype, notnull=False)
                new_attrs.append(field)
            if new_attrs:
                self._dal.define_table(
                    'facts',
                    self._dal.facts,
                    redefine=True, *new_attrs
                )
            attrs = dict(elem.items_attrs())
            attrs.update(hap_id=elem.hap_id)
            self._dal.facts.insert(**attrs)

        # if is a edge
        elif isinstance(elem, dom.Edge):
            actual_haps_number = len(self._dal.edges.elements) - 2
            need_haps_number = len(elem.haps_id)
            new_attrs = []
            while need_haps_number > actual_haps_number + len(new_attrs):
                aname = "hap_{}".format(actual_haps_number + len(new_attrs))
                field = dal.Field(aname, db.haplotypes, notnull=False)
                new_attrs.append(field)
            if new_attrs:
                self._dal.define_table(
                    'edges',
                    self._dal.edges,
                    redefine=True, *new_attrs)
            attrs = {}
            for idx, hap_id in enumerate(elem.haps_id):
                attrs["hap_{}".format(idx)] = hap_id
            attrs.update(weight=elem.weight)
            self._dal.edges.insert(**attrs)
        else:
            msg = "Object '{}' is not yatel.dom type".format(str(elem))
            raise YatelNetworkError(msg)

    def init(self):
        self._validate_status(self.STATUS_PREPARED, self.STATUS_CONECTED)
        if self.status == self.STATUS_PREPARED:
            self._dal.commit()
        self._status = self.STATUS_INITED


    #===========================================================================
    # QUERIES
    #===========================================================================

    #===========================================================================
    # PROPERTIES
    #===========================================================================

    @property
    def status(self):
        return self._status

    @property
    def dal(self):
        self._validate_status(self.STATUS_INITED)
        return self._dal


#===============================================================================
# FUNCTIONS
#===============================================================================

def allin(l1, l2):
    """Returns ``True`` if all elements in ``l1`` is in ``l2``"""
    for l in l1:
        if l not in l2:
            return False
    return True


