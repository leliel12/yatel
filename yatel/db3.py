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
# DEVELOPER NOTES
#===============================================================================

# first see this video https://www.youtube.com/watch?v=woKYyhLCcnU
# then: http://docs.sqlalchemy.org/en/latest/core/tutorial.html
# and then: http://docs.sqlalchemy.org/en/latest/core/connections.html


#===============================================================================
# IMPORTS
#===============================================================================

import datetime
import string
import tempfile
import decimal
import os

from yatel import dom

import sqlalchemy as sa
from sqlalchemy import sql


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
        lambda x: sa.DateTime(),
    datetime.time:
        lambda x: sa.Time(),
    datetime.date:
        lambda x: sa.Date(),
    bool:
        lambda x: sa.Boolean(),
    int:
        lambda x: sa.Integer(),
    float:
        lambda x: sa.Float(),
    str:
        lambda x: sa.String(512) if len(x) < 512 else sa.Text,
    unicode:
        lambda x: sa.String(512) if len(x) < 512 else sa.Text,
    decimal.Decimal:
        lambda x: sa.Numeric()
}

HAPLOTYPES = "haplotypes"
FACTS = "facts"
EDGES = "edges"
VERSIONS = "versions"


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

        self._engine = sa.create_engine(self._uri)
        self._metadata = sa.MetaData(self._engine)

        self._hapid_buff = {}
        self._dbid_buff = {}
        self._create_mode = create

        if self._create_mode:
            tpl = string.Template(SCHEMA_URIS["sqlite"])
            self._column_buff = {HAPLOTYPES: [], FACTS: [], EDGES: []}
            self._tmp_dbfile = tempfile.NamedTemporaryFile(suffix="_yatel")
            self._tmp_meta = sa.MetaData(
                tpl.substitute(dbname=self._tmp_dbfile.name)
            )
            self._tmp_objects = sa.Table(
                'tmp_objects', self._tmp_meta,
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("tname", sa.String(length=15), nullable=False),
                sa.Column("data", sa.PickleType(), nullable=False),
            )
            self._tmp_meta.create_all()
            self._tmp_conn = self._tmp_meta.bind.connect()
            self._tmp_trans = self._tmp_conn.begin()
        else:
            self._metadata.reflect()
            self._versions_table = self._metadata.tables[VERSIONS]
            self._haplotypes_table = self._metadata.tables[HAPLOTYPES]
            self._facts_table = self._metadata.tables[FACTS]
            self._edges_table = self._metadata.tables[EDGES]

    #===========================================================================
    # PRIVATE
    #===========================================================================

    def _new_attrs(self, attnames, table):
        columns = [c.name for c in self._column_buff[table]]
        return set(attnames).difference(columns)

    def _row2hap(self, row):
        attrs = dict([
            (k, v) for k, v in row.items()
            if k != "hap_id" and v!= None
        ])
        hap_id = row["hap_id"]
        return dom.Haplotype(hap_id, **attrs)

    def _row2fact(self, row):
        attrs = dict([
            (k, v) for k, v in row.items()
            if k not in ("id", "hap_id") and v!= None
        ])
        hap_id = row["hap_id"]
        return dom.Fact(hap_id, **attrs)

    def _row2edge(self, row):
        haps = [v for k, v in row.items()
                if k not in ("id", "weight") and v!= None]
        weight = row["weight"]
        return dom.Edge(weight, *haps)

    #===========================================================================
    # CREATE METHODS
    #===========================================================================

    def add_element(self, elem):
        if self.created:
            raise YatelNetworkError("Network already created")

        data = None
        tname = None

        # determine the hap_id columns
        if isinstance(elem, (dom.Haplotype, dom.Fact)) \
           and not self._column_buff[HAPLOTYPES]:
                avalue = elem.hap_id
                atype = type(avalue)
                ctype = SQL_ALCHEMY_TYPES[atype](avalue)
                self._column_buff[HAPLOTYPES].append(
                    sa.Column("hap_id", ctype, primary_key=True)
                )
                self._column_buff[FACTS].append(
                    sa.Column("hap_id", ctype,
                              sa.ForeignKey('{}.hap_id'.format(HAPLOTYPES)),
                              nullable=False)
                )

        if isinstance(elem, dom.Haplotype):
            new_attrs_names = self._new_attrs(elem.names_attrs(), HAPLOTYPES)
            for aname in new_attrs_names:
                avalue = elem[aname]
                atype = type(avalue)
                ctype = SQL_ALCHEMY_TYPES[atype](avalue)
                column = sa.Column(aname, ctype, nullable=True)
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
                column = sa.Column(aname, ctype, nullable=True)
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
                column = sa.Column(
                    aname, sa.String(512),
                    sa.ForeignKey('{}.hap_id'.format(HAPLOTYPES)),
                    nullable=True
                )
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

        # first confirm all changes to the temp database
        self._tmp_trans.commit()

        # create te tables
        self._versions_table = sa.Table(
            VERSIONS, self._metadata,
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tag", sa.String(512), unique=True,nullable=False),
            sa.Column("datetime", sa.DateTime(), nullable=False),
            sa.Column("comment", sa.Text(), nullable=False),
            sa.Column("data", sa.PickleType(), nullable=False),
        )

        self._haplotypes_table = sa.Table(
            HAPLOTYPES, self._metadata, *self._column_buff[HAPLOTYPES]
        )

        self._facts_table = sa.Table(
            FACTS, self._metadata,
            sa.Column("id", sa.Integer(), primary_key=True),
            *self._column_buff[FACTS]
        )

        self._edges_table = sa.Table(
            EDGES, self._metadata,
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("weight", sa.Float(), nullable=False),
            *self._column_buff[EDGES]
        )
        self._metadata.create_all()

        # populate tables inside a transaction
        with self._metadata.bind.begin() as conn:
            query = self._tmp_objects.select()
            for row in self._tmp_conn.execute(query):
                table = None
                if row.tname == HAPLOTYPES:
                    table = self._haplotypes_table
                elif row.tname == FACTS:
                    table = self._facts_table
                elif row.tname == EDGES:
                    table = self._edges_table
                else:
                    msg = "Invalid tname '{}'".format(row.tname)
                    raise YatelNetworkError(msg)
                conn.execute(table.insert(), **row.data)

        # close all tmp references
        self._tmp_conn.close()
        self._tmp_trans.close()

        # destroy tmp file
        self._tmp_dbfile.close()

        # destroys the buffers
        del self._column_buff
        del self._tmp_objects
        del self._tmp_dbfile
        del self._tmp_conn
        del self._tmp_meta
        del self._tmp_trans

        self._create_mode = False

    #===========================================================================
    # QUERIES # use execute here
    #===========================================================================

    def execute(self, query):
        if not self.created:
            raise YatelNetworkError("Network not created")
        return self._engine.execute(query)

    def iter_haplotypes(self):
        """Iterates over all ``dom.Haplotype`` instances store in the database.

        """
        query = sql.select([self._haplotypes_table])
        for row in self.execute(query):
            yield self._row2hap(row)

    def iter_facts(self):
        """Iterates over all ``dom.Fact`` instances store in the database."""
        query = sql.select([self._facts_table])
        for row in self.execute(query):
            yield self._row2fact(row)

    def iter_edges(self):
        """Iterates over all ``dom.Edge`` instances store in the database."""
        query = sql.select([self._edges_table])
        for row in self.execute(query):
            yield self._row2edge(row)

    def haplotype_by_id(self, hap_id):
        """Return a ``dom.Haplotype`` instace store in the dabase with the
        giver ``hap_id``.

        **Params**
            :hap_id: An existing id of the ``haplotypes`` type table.

        **Return**
            ``dom.Haplotype`` instance.

        """
        query = sql.select([self._haplotypes_table]).where(
            self._haplotypes_table.c.hap_id == hap_id
        ).limit(1)
        row = self.execute(query).fetchone()
        return self._row2hap(row)

    def fact_attributes_names(self):
        """Return a ``iterator`` of all existing ``dom.Fact`` atributes."""
        for c in self._facts_table.c:
            if c.name not in ("id", "hap_id"):
                yield c.name


    def fact_attribute_values(self, att_name):
        """Return a ``iterator`` of all posible values of given ``dom.Fact``
        atribute.

        """
        att = self._facts_table.c[att_name]
        query = sql.select([att]).where(att != None).distinct()
        for row in self.execute(query):
            yield row[att_name]

    def facts_by_haplotype(self, hap):
        """Return a ``iterator`` of all facts of a given ``dom.Haplotype``"""
        query = sql.select([self._facts_table]).where(
            self._facts_table.c.hap_id==hap.hap_id
        ).distinct()
        for row in self.execute(query):
            yield self._row2fact(row)

    #===========================================================================
    # PROPERTIES
    #===========================================================================

    @property
    def name(self):
        """The name of the connection."""
        return self._uri

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
