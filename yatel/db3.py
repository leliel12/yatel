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
        lambda x: sql.String(512) if len(x) < 512 else sql.Text(),
    unicode:
        lambda x: sql.String(512) if len(x) < 512 else sql.Text(),
    decimal.Decimal:
        lambda x: sql.Numeric()
}

FK = "FK"


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
            self._create_network_base_tables()
        else:
            self._metadata.reflect()

    #===========================================================================
    # PRIVATE
    #===========================================================================

    def _create_network_base_tables(self):

        # first add the static tables
        self._yatel_fields = sql.Table(
            'yatel_fields', self._metadata,
            sql.Column("id", sql.Integer(), primary_key=True),
            sql.Column("tname", sql.String(20), nullable=False),
            sql.Column("fname", sql.String(512), nullable=False),
            sql.Column("ftype", sql.String(20), nullable=False),
            sql.Column("tname", sql.Boolean(), nullable=False),
            sql.Column("reference_to", sql.String(20), nullable=True)
        )

        self._yatel_versions = sql.Table(
            'yatel_versions', self._metadata,
            sql.Column("id", sql.Integer(), primary_key=True),
            sql.Column("tag", sql.String(512), unique=True,nullable=False),
            sql.Column("datetime", sql.DateTime(), nullable=False),
            sql.Column("comment", sql.Text(), nullable=False),
            sql.Column("data", sql.PickleType(), nullable=False),
        )

        self._creation_buff = sql.Table(
            "cration_buff", self._metadata,
            sql.Column("id", sql.Integer(), primary_key=True),
            sql.Column("data", sql.PickleType(), nullable=False)
        )

        self._metadata.create_all()
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
        select = self._yatel_fields.select(self._yatel_fields.tname == table)


        return set(attnames).difference(table.columns.keys())

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

        # if is an haplotypes
        if isinstance(elem, dom.Haplotype):
            new_attrs_names = self._new_attrs(elem.names_attrs(), "haplotypes")
            for fname in new_attrs_names:
                value = elem[fname]
                ftype = SQL_ALCHEMY_TYPES[value](value)
                self._yatel_fields.insert().execute(
                    tname='haplotypes', fname=fname,
                    ftype=type(ftype).__name__,
                    is_unique=False, reference_to=None
                )
            #~ if new_attrs:
                #~ self._dal.define_table(
                    #~ 'haplotypes',
                    #~ self._dal.haplotypes,
                    #~ redefine=True, *new_attrs
                #~ )
                #~ self._dal.yatel_fields.bulk_insert(attrs_descs)
#~
            #~ attrs = dict(elem.items_attrs())
            #~ attrs.update(hap_id=elem.hap_id)
            #~ self._dal.haplotypes.insert(**attrs)
#~
        #~ # if is a fact
        #~ elif isinstance(elem, dom.Fact):
            #~ new_attrs_names = self._new_attrs(elem.names_attrs(),
                                              #~ self._dal.facts)
            #~ new_attrs = []
            #~ attrs_descs = []
            #~ for fname in new_attrs_names:
                #~ ftype =  DAL_TYPES[type(elem[fname])](elem[fname])
                #~ field = dal.Field(fname, ftype, notnull=False)
                #~ desc = {"tname": 'facts', "fname": fname, "ftype": ftype,
                        #~ "is_unique": False, "reference_to": None}
                #~ new_attrs.append(field)
                #~ attrs_descs.append(desc)
            #~ if new_attrs:
                #~ self._dal.define_table(
                    #~ 'facts',
                    #~ self._dal.facts,
                    #~ redefine=True, *new_attrs
                #~ )
                #~ self._dal.yatel_fields.bulk_insert(attrs_descs)
#~
            #~ attrs = dict(elem.items_attrs())
            #~ attrs.update(hap=self._hapid2dbid(elem.hap_id))
            #~ self._dal.facts.insert(**attrs)
#~
        #~ # if is an edge
        #~ elif isinstance(elem, dom.Edge):
            #~ actual_haps_number = len(self._dal.edges.fields) - 2
            #~ need_haps_number = len(elem.haps_id)
#~
            #~ new_attrs = []
            #~ attrs_descs = []
            #~ while need_haps_number > actual_haps_number + len(new_attrs):
                #~ fname = "hap_{}".format(actual_haps_number + len(new_attrs))
                #~ field = dal.Field(fname, self._dal.haplotypes, notnull=False)
                #~ desc = {"tname": 'edges', "fname": fname, "ftype": FK,
                        #~ "is_unique": False, "reference_to": 'haplotypes'}
                #~ new_attrs.append(field)
                #~ attrs_descs.append(desc)
            #~ if new_attrs:
                #~ self._dal.define_table(
                    #~ 'edges',
                    #~ self._dal.edges,
                    #~ redefine=True, *new_attrs)
                #~ self._dal.yatel_fields.bulk_insert(attrs_descs)
#~
            #~ attrs = {}
            #~ for idx, hap_id in enumerate(elem.haps_id):
                #~ attrs["hap_{}".format(idx)] = self._hapid2dbid(hap_id)
            #~ attrs.update(weight=elem.weight)
            #~ self._dal.edges.insert(**attrs)
#~
        #~ # if is trash
        #~ else:
            #~ msg = "Object '{}' is not yatel.dom type".format(str(elem))
            #~ raise YatelNetworkError(msg)

    def end_creation(self):
        if self.created:
            raise YatelNetworkError("Network already created")
        #~ self._dal.commit()
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
