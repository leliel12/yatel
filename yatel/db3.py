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

Is developed over sqlalchemy

for testing use:

::

    from yatel import db3 as db

"""


#===============================================================================
# IMPORTS
#===============================================================================

import datetime
import string
import tempfile
import decimal

from yatel import dom

import sqlalchemy as sql


#===============================================================================
# EXCEPTIONS
#===============================================================================

# The order to show schema variables, if it not in this list put at the end
VARS_SCHEMA_ORDER = ("dbname", "user", "password", "dsn", "host", "port")


SCHEMAS = (
    'sqlite',
    #"mysql",
    #"postgres",

)

SCHEMA_URIS = {
    'sqlite': "sqlite:///${dbname}",
}


SCHEMA_VARS = {}
for schema in SCHEMAS:
    tpl = string.Template(SCHEMA_URIS[schema])
    variables = []
    for e, n, b, i in tpl.pattern.findall(tpl.template):
        if n or b:
            variables.append(n or b)
    variables.sort(key=lambda v: VARS_SCHEMA_ORDER.index(v))
    SCHEMA_VARS[schema] = variables


SQL_ALCHEMY_TYPES = {
    datetime.datetime:
        lambda x: sql.DateTime(),
    datetime.time:
        lambda x: sql.Time(),
    datetime.date:
        lambda x: sql.Date(),
    bool:
        lambda x: sql.Boolean(),
    int:
        lambda x: sql.Integer(),
    float:
        lambda x: sql.Float(),
    str:
        lambda x: sql.String(512) if len(x) < 512 else sql.Text,
    unicode:
        lambda x: sql.String(512) if len(x) < 512 else sql.Text,
    decimal.Decimal:
        lambda x: sql.Numeric()
}

HAPLOTYPES = "haplotypes"
FACTS = "facts"
EDGES = "edges"


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
        self._uri = tpl.substitute(kwargs)
        self._metadata = sql.MetaData(self._uri)

        self._hapid_buff = {}
        self._dbid_buff = {}
        self._create_mode = create

        if self._create_mode:
            self._column_buff = {HAPLOTYPES: [], FACTS: [], EDGES: []}
            tpl = string.Template(SCHEMA_URIS["sqlite"])
            self._tmp_dbfile = tempfile.NamedTemporaryFile(suffix="_yatel")
            self._tmp_meta = sql.MetaData(
                tpl.substitute(dbname="cosito.db")
            )
            self._create_temp_database_tables()
            self._tmp_conn = self._tmp_meta.bind.connect()
            self._tmp_trans = self._tmp_conn.begin()
        else:
            self._metadata.reflect()

    #===========================================================================
    # PRIVATE
    #===========================================================================

    def _create_temp_database_tables(self):

        # temporaty table
        self._tmp_objects = sql.Table(
            'tmp_objects', self._tmp_meta,
            sql.Column("id", sql.Integer(), primary_key=True),
            sql.Column("tname", sql.String(length=15), nullable=False),
            sql.Column("data", sql.PickleType(), nullable=False),
        )
        self._tmp_meta.create_all()


        #~ # first static tables
        #~ self._yatel_versions = sql.Table(
            #~ 'yatel_versions', self._metadata,
            #~ sql.Column("id", sql.Integer(), primary_key=True),
            #~ sql.Column("tag", sql.String(512), unique=True,nullable=False),
            #~ sql.Column("datetime", sql.DateTime(), nullable=False),
            #~ sql.Column("comment", sql.Text(), nullable=False),
            #~ sql.Column("data", sql.PickleType(), nullable=False),
        #~ )

        #self._metadata.create_all()
        #~ # base struct
        #~ self._haplotypes = sql.Table(
            #~ 'haplotypes', self._metadata,
            #~ sql.Column("id", sql.Integer(), primary_key=True),
            #~ sql.Column("hap_id", sql.String(512), unique=True, nullable=False)
        #~ )
#~
        #~ self._facts = sql.Table(
            #~ 'facts', self._metadata,
            #~ sql.Column("id", sql.Integer(), primary_key=True),
            #~ sql.Column("hap", sql.Integer(), sql.ForeignKey('haplotypes.id')),
        #~ )
#~
        #~ self._facts = sql.Table(
            #~ 'edges', self._metadata,
            #~ sql.Column("id", sql.Integer(), primary_key=True),
            #~ sql.Column("weight", sql.Float(), nullable=False),
        #~ )


    #~ def _hapid2dbid(self, hap_id):
        #~ if hap_id not in self._hapid_buff:
            #~ query = self._dal.haplotypes.hap_id == hap_id
            #~ row = self._dal(query).select(self._dal.haplotypes.id).first()
            #~ self._hapid_buff[hap_id] = row["id"]
        #~ return self._hapid_buff[hap_id]
#~
    #~ def _dbid2hapid(self, db_id):
        #~ if db_id not in self._dbid_buff:
            #~ query = self._dal.haplotypes.id == db_id
            #~ row = self._dal(query).select(self._dal.haplotypes.hap_id).first()
            #~ self._dbid_buff[db_id] = row["hap_id"]
        #~ return self._dbid_buff[db_id]
#~
    def _new_attrs(self, attnames, table):
        columns = [c.name for c in self._column_buff[table]]
        return set(attnames).difference(columns)

#~
    #~ def _row2hap(self, row):
        #~ attrs = dict([
            #~ (k, v) for k, v in row.as_dict().items()
            #~ if k not in ("id", "hap_id") and v!= None
        #~ ])
        #~ hap_id = row["hap_id"]
        #~ return dom.Haplotype(hap_id, **attrs)
#~
    #~ def _row2fact(self, row):
        #~ attrs = dict([
            #~ (k, v) for k, v in row.as_dict().items()
            #~ if k not in ("id", "hap") and v!= None
        #~ ])
        #~ hap_id = self._dbid2hapid(row["hap"])
        #~ return dom.Fact(hap_id, **attrs)
#~
    #~ def _row2edge(self, row):
        #~ haps = [self._dbid2hapid(v)
                #~ for k, v in row.as_dict().items()
                #~ if k not in ("id", "weight") and v!= None]
        #~ weight = row["weight"]
        #~ return dom.Edge(weight, *haps)

    #===========================================================================
    # CREATE METHODS
    #===========================================================================

    def add_element(self, elem):
        if self.created:
            raise YatelNetworkError("Network already created")

        data = None
        tname = None

        if isinstance(elem, dom.Haplotype):
            new_attrs_names = self._new_attrs(elem.names_attrs(), HAPLOTYPES)
            for aname in new_attrs_names:
                avalue = elem[aname]
                atype = type(avalue)
                ctype = SQL_ALCHEMY_TYPES[atype](avalue)
                column = sql.Column(aname, ctype, nullable=True)
                self._column_buff[HAPLOTYPES].append(column)
            data = dict(elem.items_attrs())
            data["hap_id"] = elem.hap_id
            tname = HAPLOTYPES

        elif isinstance(elem, dom.Fact):
            new_attrs_names = self._new_attrs(elem.names_attrs(), FACTS)
            for aname in new_attrs_names:
                avalue = elem[aname]
                atype = type(avalue)
                ctype = SQL_ALCHEMY_TYPES[atype](avalue)
                column = sql.Column(aname, ctype, nullable=True)
                self._column_buff[FACTS].append(column)
            data = dict(elem.items_attrs())
            data["hap_id"] = elem.hap_id
            tname = FACTS

        elif isinstance(elem, dom.Edge):
            actual_haps_number = len(self._column_buff[EDGES])
            need_haps_number = len(elem.haps_id)
            columns = []
            while need_haps_number > actual_haps_number + len(columns):
                aname = "hap_{}".format(actual_haps_number + len(columns))
                column = sql.Column(aname, None,
                                    sql.ForeignKey('{}.id'.format(HAPLOTYPES)),
                                    nullable=True),
                columns.append(column)
            self._column_buff[EDGES].extend(columns)
            data = {}
            for idx, hap_id in enumerate(elem.haps_id):
                data["hap_{}".format(idx)] = hap_id
            data.update(weight=elem.weight)
            tname = EDGES

        # if is trash
        else:
            msg = "Object '{}' is not yatel.dom type".format(str(elem))
            raise YatelNetworkError(msg)
        self._tmp_conn.execute(self._tmp_objects.insert(),
                               tname=tname, data=data)

    def end_creation(self):
        if self.created:
            raise YatelNetworkError("Network already created")
        self._tmp_trans.commit()




        self._create_mode = False

    #===========================================================================
    # QUERIES # not use self._dal here!!!!
    #===========================================================================

    #~ def iter_haplotypes(self):
        #~ """Iterates over all ``dom.Haplotype`` instances store in the database.
#~
        #~ """
        #~ for row in self.dal(self.dal.haplotypes).select():
            #~ yield self._row2hap(row)
#~
    #~ def iter_facts(self):
        #~ """Iterates over all ``dom.Fact`` instances store in the database."""
        #~ for row in self.dal(self.dal.facts).select():
            #~ yield self._row2fact(row)
#~
    #~ def iter_edges(self):
        #~ """Iterates over all ``dom.Edge`` instances store in the database."""
        #~ for row in self.dal(self.dal.edges).select():
            #~ yield self._row2edge(row)
#~
    #~ def haplotype_by_id(self, hap_id):
        #~ """Return a ``dom.Haplotype`` instace store in the dabase with the
        #~ giver ``hap_id``.
#~
        #~ **Params**
            #~ :hap_id: An existing id of the ``haplotypes`` type table.
#~
        #~ **Return**
            #~ ``dom.Haplotype`` instance.
#~
        #~ """
        #~ query = self.dal.haplotypes.id == self._hapid2dbid(hap_id)
        #~ row = self.dal(query).select(limitby=(0, 1)).first()
        #~ return self._row2hap(row)


    #===========================================================================
    # PROPERTIES
    #===========================================================================

    @property
    def created(self):
        return not self._create_mode




#===============================================================================
# FUNCTIONS
#===============================================================================

#~ def allin(l1, l2):
    #~ """Returns ``True`` if all elements in ``l1`` is in ``l2``"""
    #~ for l in l1:
        #~ if l not in l2:
            #~ return False
    #~ return True


#===============================================================================
# MAIN
#===============================================================================



if __name__ == "__main__":
    print(__doc__)
