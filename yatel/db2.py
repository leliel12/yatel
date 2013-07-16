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
        lambda x: "decimal(10,10)"
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

    def __init__(self, schema, create=False, **kwargs):
        tpl = string.Template(SCHEMA_URIS[schema])
        uri = tpl.substitute(kwargs)
        print create
        self._dal = dal.DAL(uri, migrate_enabled=True)
        self._create = create
        self._base_tables()
        if not create:
            self._init()

    def _init(self):
        for fld in self._dal(self._dal.yatel_fields).select():
            print fld

    def _new_attrs(self, attnames, table):
        return set(attnames).difference(table.fields)

    def _base_tables(self):

        self._dal.define_table(
            'yatel_fields',
            dal.Field("tname", "string", notnull=True),
            dal.Field("name", "string", notnull=True),
            dal.Field("type", "string", notnull=True),
            dal.Field("is_unique", "boolean", notnull=True),
            dal.Field("reference_to", "string", notnull=False)
            ,migrate=self._create
        )

        self._dal.define_table(
            'yatel_versions',
            dal.Field("tag", "string", notnull=True),
            dal.Field("datetime", "datetime", notnull=True),
            dal.Field("comment", "text", notnull=True),
            dal.Field("data", "text", notnull=True)
        )

        self._dal.define_table(
            'yatel_vars',
            dal.Field("name", "string", notnull=True),
            dal.Field("value", "string", notnull=True)
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
            dal.Field("hap", self._dal.haplotypes)
        )

    def _register_fields(self, new_attrs):
        regs = []
        for att in new_attrs:
            atype, rfto = None, ""
            splited =  att.type.split(" ", 1)
            atype = splited[0]
            if len(splited) == 2:
                rfto = splited[1]
            regs.append({"tname": att.tablename, "name": att.name,
                         "type": atype, "is_unique": att.unique,
                         "reference_to": rfto})
        self._dal.yatel_fields.bulk_insert(regs)

    def _hapid2dbid(self, hap_id):
        query = self._dal.haplotypes.hap_id == hap_id
        row = self._dal(query).select(self._dal.haplotypes.id).first()
        return row["id"]

    #===========================================================================
    # INIT FUNCTIONS
    #===========================================================================


    def add_element(self, elem):
        if self.created:
            raise YatelNetworkError("Network already created")
        if not len(self._dal.tables):
            self._base_tables()

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
                self._register_fields(new_attrs)
            attrs = dict(elem.items_attrs())
            attrs.update(hap_id=elem.hap_id)
            self._dal.haplotypes.insert(**attrs)

        # if is a fact
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
                self._register_fields(new_attrs)
            attrs = dict(elem.items_attrs())
            attrs.update(hap=self._hapid2dbid(elem.hap_id))
            self._dal.facts.insert(**attrs)

        # if is an edge
        elif isinstance(elem, dom.Edge):
            actual_haps_number = len(self._dal.edges.fields) - 2
            need_haps_number = len(elem.haps_id)
            new_attrs = []
            while need_haps_number > actual_haps_number + len(new_attrs):
                aname = "hap_{}".format(actual_haps_number + len(new_attrs))
                field = dal.Field(aname, self._dal.haplotypes, notnull=False)
                new_attrs.append(field)
            if new_attrs:
                self._dal.define_table(
                    'edges',
                    self._dal.edges,
                    redefine=True, *new_attrs)
                self._register_fields(new_attrs)
            attrs = {}
            for idx, hap_id in enumerate(elem.haps_id):
                attrs["hap_{}".format(idx)] = self._hapid2dbid(hap_id)
            attrs.update(weight=elem.weight)
            self._dal.edges.insert(**attrs)

        # if is trash
        else:
            msg = "Object '{}' is not yatel.dom type".format(str(elem))
            raise YatelNetworkError(msg)

    def end_creation(self):
        if self.created:
            raise YatelNetworkError("Network already created")
        self._dal.commit()
        self._create = False


    #===========================================================================
    # QUERIES
    #===========================================================================

    #===========================================================================
    # PROPERTIES
    #===========================================================================

    @property
    def created(self):
        return not self._create

    @property
    def dal(self):
        if not self.created:
            raise YatelNetworkError("Network still not created")
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


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
