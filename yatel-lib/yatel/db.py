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

import uuid
import datetime
import string
import decimal
import os
import cPickle

import sqlalchemy as sa
from sqlalchemy import sql
from sqlalchemy.engine import url

from yatel import dom


#===============================================================================
# EXCEPTIONS
#===============================================================================

#: The order to show ENGINE variables, if it not in this list put at the end
VARS_ENGINE_ORDER = ("database", "user", "password", "dsn", "host", "port")


#: Available engines
ENGINES = (
    'sqlite',
    'memory',
    'mysql',
    'postgresql',
)


#: Connection uris for the existing engines
ENGINE_URIS = {
    'sqlite': "sqlite:///${database}",
    'memory': "sqlite://",
    'mysql': "mysql://${user}:${password}@${host}:${port}/${database}",
    'postgresql': "postgresql://${user}:${password}@${host}:${port}/${database}"
}


#: Variables of the uris
ENGINE_VARS = {}
for engine in ENGINES:
    tpl = string.Template(ENGINE_URIS[engine])
    variables = []
    for e, n, b, i in tpl.pattern.findall(tpl.template):
        if n or b:
            variables.append(n or b)
    variables.sort(key=lambda v: VARS_ENGINE_ORDER.index(v))
    ENGINE_VARS[engine] = variables


#: This dictionary maps a Python types to functions for convert
#: the a given type instance to a correct sqlalchemy column type.
#: For retrieve all suported types use db.SQL_ALCHEMY_TYPES.keys()
SQL_ALCHEMY_TYPES = {
    datetime.datetime: lambda x: sa.DateTime(),
    datetime.time: lambda x: sa.Time(),
    datetime.date: lambda x: sa.Date(),
    bool: lambda x: sa.Boolean(),
    int: lambda x: sa.Integer(),
    long: lambda x: sa.BigInteger(),
    float: lambda x: sa.Float(),
    str: lambda x: sa.String(500) if len(x) < 500 else sa.Text(),
    unicode: lambda x: sa.String(500) if len(x) < 500 else sa.Text(),
    decimal.Decimal: lambda x: sa.Numeric()
}


#: This dictionary maps a sqlalchemy Column types to functions for convert
#: the a given Column class to python type
#: For retrieve all suported columns use db.PYTHON_TYPES.keys()
PYTHON_TYPES = {
    sa.DateTime: lambda x: datetime.datetime,
    sa.Time: lambda x: datetime.time,
    sa.Date: lambda x: datetime.date,
    sa.Boolean: lambda x: bool,
    sa.BigInteger: lambda x: long,
    sa.Integer: lambda x: int,
    sa.Float: lambda x: float,
    sa.String: lambda x: str,
    sa.Text: lambda x: unicode,
    sa.Numeric: lambda x: decimal.Decimal,
}

# TABLE NAMES

#: The name of the haplotypes table
HAPLOTYPES = "haplotypes"

#: The name of the facts table
FACTS = "facts"

#: The name of the edges table
EDGES = "edges"

#: A collection tihe the 3 table names
TABLES = (HAPLOTYPES, FACTS, EDGES)

MODE_READ = "r"
MODE_WRITE = "w"
MODE_APPEND = "a"

#: Collection of tri modes to open the networks
MODES = (MODE_READ, MODE_WRITE, MODE_APPEND)

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

    def __init__(self, engine, mode=MODE_READ, log=None, **kwargs):

        self._uri = to_uri(engine, **kwargs)

        self._engine = sa.create_engine(self._uri, echo=bool(log))
        self._metadata = sa.MetaData(self._engine)

        self._mode = mode

        if self._mode == MODE_READ:
            self._metadata.reflect(only=TABLES)
            self.haplotypes_table = self._metadata.tables[HAPLOTYPES]
            self.facts_table = self._metadata.tables[FACTS]
            self.edges_table = self._metadata.tables[EDGES]
        else:

            if self._mode == MODE_WRITE:
                self._metadata.reflect()
                self._metadata.drop_all()
                self._metadata.clear()

            self._column_buff = {HAPLOTYPES: [], FACTS: [], EDGES: 0}
            self._create_objects = sa.Table(
                "_tmp_yatel_objs_{}".format(uuid.uuid4()), self._metadata,
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("tname", sa.String(length=15), nullable=False),
                sa.Column("data", sa.PickleType(), nullable=False),
                prefixes=['TEMPORARY'],
            )
            self._create_conn = self._metadata.bind.connect()
            self._create_objects.create(self._create_conn)
            self._create_trans = self._create_conn.begin()

            if self._mode == MODE_APPEND:
                self._creation_append = True
                self._metadata.reflect(only=TABLES)
                self.haplotypes_table = self._metadata.tables[HAPLOTYPES]
                self.facts_table = self._metadata.tables[FACTS]
                self.edges_table = self._metadata.tables[EDGES]
                self.add_elements(self.haplotypes_iterator())
                self.add_elements(self.facts_iterator())
                self.add_elements(self.edges_iterator())
                self._metadata.drop_all(
                    self._create_conn,
                    tables=[self.haplotypes_table,
                            self.facts_table,
                            self.edges_table]
                )
                self._metadata.remove(self.haplotypes_table)
                self._metadata.remove(self.facts_table)
                self._metadata.remove(self.edges_table)
                del self.haplotypes_table
                del self.facts_table
                del self.edges_table
                del self._creation_append


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
    # DDL METHODS
    #===========================================================================

    def add_elements(self, elems):
        map(self.add_element, elems)

    def add_element(self, elem):
        if self.mode == MODE_READ:
            raise YatelNetworkError("Network in read-only mode")

        data = None
        tname = None

        # determine the hap_id columns
        if isinstance(elem, (dom.Haplotype, dom.Fact)) \
           and not self._column_buff[HAPLOTYPES]:
                avalue = elem.hap_id
                atype = type(avalue)
                ctype = SQL_ALCHEMY_TYPES[atype](avalue)
                if isinstance(ctype, sa.Text):
                    ctype = sa.String(500)
                extra_params = {}
                if isinstance(ctype, sa.Integer):
                    extra_params["autoincrement"] = False
                self._column_buff[HAPLOTYPES].append(
                    sa.Column("hap_id", ctype,
                              index=True, primary_key=True, **extra_params)
                )
                self._column_buff[FACTS].append(
                    sa.Column("hap_id", ctype,
                              sa.ForeignKey('{}.hap_id'.format(HAPLOTYPES)),
                              index=True, nullable=False)
                )

        if isinstance(elem, dom.Haplotype):
            new_attrs_names = self._new_attrs(elem.names_attrs(), HAPLOTYPES)
            for aname in new_attrs_names:
                avalue = elem[aname]
                atype = type(avalue)
                ctype = SQL_ALCHEMY_TYPES[atype](avalue)
                column = sa.Column(aname, ctype, index=True, nullable=True)
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
                column = sa.Column(aname, ctype, index=True, nullable=True)
                self._column_buff[FACTS].append(column)
            data = dict(elem.items_attrs())
            data["hap_id"] = elem.hap_id
            tname = FACTS

        elif isinstance(elem, dom.Edge):
            if len(elem.haps_id) > self._column_buff[EDGES]:
                self._column_buff[EDGES] = len(elem.haps_id)
            data = {}
            for idx, hap_id in enumerate(elem.haps_id):
                data["hap_{}".format(idx)] = hap_id
            data["weight"] = elem.weight
            tname = EDGES

        # if is trash
        else:
            msg = "Object '{}' is not yatel.dom type".format(str(elem))
            raise TypeError(msg)
        self._create_conn.execute(self._create_objects.insert(),
                                  tname=tname, data=data)

    def confirm_changes(self):

        if self.mode == MODE_READ:
            raise YatelNetworkError("Network in read-only mode")

        # create te tables
        self.haplotypes_table = sa.Table(
            HAPLOTYPES, self._metadata, *self._column_buff[HAPLOTYPES]
        )

        self.facts_table = sa.Table(
            FACTS, self._metadata,
            sa.Column("id", sa.Integer(), primary_key=True),
            *self._column_buff[FACTS]
        )

        edges_columns = [
            sa.Column("hap_{}".format(idx),
                      self.haplotypes_table.c.hap_id.type,
                      sa.ForeignKey(HAPLOTYPES + '.hap_id'),
                      index=True, nullable=True)
            for idx in range(self._column_buff[EDGES])
        ]
        self.edges_table = sa.Table(
            EDGES, self._metadata,
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("weight", sa.Float(), nullable=False),
            *edges_columns
        )

        self._metadata.create_all(self._create_conn)

        try:
            query = sql.select([self._create_objects])
            for row in self._create_conn.execute(query):
                table = None
                if row.tname == HAPLOTYPES:
                    table = self.haplotypes_table
                elif row.tname == FACTS:
                    table = self.facts_table
                elif row.tname == EDGES:
                    table = self.edges_table
                else:
                    msg = "Invalid tname '{}'".format(row.tname)
                    raise YatelNetworkError(msg)
                self._create_conn.execute(table.insert(), **row.data)
        except Exception as err:
            self._create_trans.rollback()
            raise err
        else:
            self._create_trans.commit()

        # close all tmp references
        self._create_trans.close()
        self._create_conn.close()

        self._metadata.remove(self._create_objects)

        # destroys the buffers
        del self._column_buff
        del self._create_objects
        del self._create_conn
        del self._create_trans

        self._mode = MODE_READ

    #===========================================================================
    # QUERIES # use execute here
    #===========================================================================

    def validate_read(self):
        """Raise a ``YatelNetworkError`` if the network is in read mode"""
        if not getattr(self, "_creation_append", None):
            if self.mode != MODE_READ:
                raise YatelNetworkError("Network in {} mode".format(self.mode))

    def execute(self, query):
        """Execute a given query to the backend"""
        self.validate_read()
        return self._engine.execute(query)

    def enviroments_iterator(self, facts_attrs=[]):
        """Iterates over all convinations of enviroments of the given attrs

        """
        if "hap_id" in facts_attrs:
            raise ValueError("Invalid fact attr: 'hap_id'")
        if "id" in facts_attrs:
            raise ValueError("Invalid fact attr: 'id'")
        attrs = facts_attrs if facts_attrs else self.fact_attributes_names()
        query = sql.select(
            [self.facts_table.c[k] for k in attrs]
        ).distinct()
        for row in self.execute(query):
            yield dict(row)

    #===========================================================================
    # HAPLOTYPE QUERIES
    #===========================================================================

    def haplotype_attributes_types(self):
        """Maps a fact attribute name to python type of the atttribute

        """
        self.validate_read()
        types = {}
        for att_name, column in self.haplotypes_table.c.items():
            pptype = None
            for satype in type(column.type).__mro__:
                if satype in PYTHON_TYPES:
                    pptype = PYTHON_TYPES[satype](satype)
                    break
            if pptype:
                types[att_name] = pptype
            else:
                msg = "Hierarchy of '{}' of column '{}' is not valid in yatel"
                raise YatelNetworkError(msg.format(str(column.type), att_name))
        return types

    def haplotypes_ids(self):
        """Iterates only over all existings hap_id"""
        column = self.haplotypes_table.c["hap_id"]
        query = sql.select([column]).order_by(column)
        for row in self.execute(query):
            yield row[0]

    def haplotypes_iterator(self):
        """Iterates over all ``dom.Haplotype`` instances store in the database.

        """
        query = sql.select([self.haplotypes_table])
        for row in self.execute(query):
            yield self._row2hap(row)

    def haplotypes_by_ids(self, haps_ids):
        """Iterates over all ``dom.Haplotype`` instances with a given ids"""
        query = sql.select([self.haplotypes_table]).where(
            self.haplotypes_table.c.hap_id.in_(haps_ids)
        )
        for row in self.execute(query):
            yield self._row2hap(row)

    def haplotype_by_id(self, hap_id):
        """Return a ``dom.Haplotype`` instace store in the dabase with the
        giver ``hap_id``.

        **Params**
            :hap_id: An existing id of the ``haplotypes`` type table.

        **Return**
            ``dom.Haplotype`` instance.

        """
        query = sql.select([self.haplotypes_table]).where(
            self.haplotypes_table.c.hap_id == hap_id
        ).limit(1)
        row = self.execute(query).fetchone()
        return self._row2hap(row)

    def haplotype_links(self, hap):
        """iterates over all ``hap`` conected *haplotypes*

        **WARNING:** This method execute one query for every edge of the given
        haplotype

        **Params**
          :hap: ``dom.Haplotype`` instance
        **Return**
            An iterable with 2 components: A distance as ``float`` and a
            ``list`` with the conected haplotypes.

        """
        for edge in self.edges_by_haplotype(hap):
            haps_ids = [hap_id
                        for hap_id in edge.haps_id
                        if hap_id != hap.hap_id]
            if haps_ids:
                yield edge.weight, tuple(self.haplotypes_by_ids(haps_ids))
            else:
                yield edge.weight, (hap,)

    def haplotypes_by_sql(self, query, **kwargs):
        """Try to execute an arbitrary *sql* and return an iterable of
        ``dom.Haplotype`` instances selected by the query.

        NOTE: Init all queries with ``select * from haplotype``

        **Params**
            :query: The *sql* query.
            :kwargs: Argument to replace the ``:varname`` in the query.

        **Returns**
            A ``iterator`` of ``dom.Haplotype`` instance.

        For more information see: http://docs.sqlalchemy.org/en/rel_0_8/core/tutorial.html#using-text

        """
        if not query.lower().startswith("select * from haplotype"):
            msg = "'query' must start with 'select * from 'haplotype'"
            raise ValueError(msg)
        query = sql.text(query)
        for row in self.execute(query, **kwargs):
            yield self._row2hap(row)

    def haplotypes_ids_enviroment(self, env=None, **kwargs):
        """Like haplotypes_enviroments but only return an iterator over hap_ids

        """
        env = dict(env) if env else {}
        env.update(kwargs)
        where = sql.and_(*[self.facts_table.c[k] == v
                           for k, v in env.items()])
        query = sql.select([self.haplotypes_table.c["hap_id"]]).select_from(
            self.haplotypes_table.join(
                self.facts_table,
                self.facts_table.c.hap_id == self.haplotypes_table.c.hap_id
            )
        ).where(where).distinct()
        for row in self.execute(query):
            yield row[0]

    def haplotypes_enviroment(self, env=None, **kwargs):
        """Return a iterator of ``dom.Haplotype`` related to a ``dom.Fact`` with
        attribute and value specified in ``kwargs``

        **Params**
            :env: Keys are ``dom.Fact`` attribute name and value a posible
                  value of the given attribte.
            :kwargs: Keys are ``dom.Fact`` attribute name and value a posible
                     value of the given attribte.

        **Return**
            ``iterator`` of ``dom.Haplotype``.

        **Example**

            ::

                >>> from yatel import db, dom
                >>> conn = db.YatelNetwork("sqlite", create=True,
                                           dbname="yateldatabase.db")
                >>> conn.add_elements([dom.Haplotype("hap1"),
                                       dom.Haplotype("hap2"),
                                       dom.Fact("hap1", a=1, c="foo"),
                                       dom.Fact("hap2", a=1, b=2),
                                       dom.Edge(1, "hap1", "hap2")])
                >>> conn.haplotypes_enviroment(a=1)
                (<Haplotype 'hap1' at 0x2463250>, <Haplotype 'hap2' at 0x2463390>)
                >>> conn.haplotypes_enviroment({"c": "foo"})
                (<Haplotype 'hap1' at 0x2463250>, )
                >>> conn.haplotypes_enviroment({"a": 1}, b=2)
                (<Haplotype 'hap2' at 0x2463390>, )

        """
        env = dict(env) if env else {}
        env.update(kwargs)
        where = sql.and_(*[self.facts_table.c[k] == v
                           for k, v in env.items()])
        query = sql.select([self.haplotypes_table]).select_from(
            self.haplotypes_table.join(
                self.facts_table,
                self.facts_table.c.hap_id == self.haplotypes_table.c.hap_id
            )
        ).where(where).distinct()
        for row in self.execute(query):
            yield self._row2hap(row)

    #===========================================================================
    # EDGES QUERIES
    #===========================================================================

    def edges_iterator(self):
        """Iterates over all ``dom.Edge`` instances store in the database."""
        query = sql.select([self.edges_table])
        for row in self.execute(query):
            yield self._row2edge(row)

    def edges_enviroment(self, env=None, **kwargs):
        """Iterates over all ``dom.Edge`` instances of a given enviroment"""
        env = dict(env) if env else {}
        env.update(kwargs)
        where = sql.and_(*[self.facts_table.c[k] == v
                           for k, v in env.items()])

        joins = sql.or_(*[v == self.facts_table.c.hap_id
                          for k, v in self.edges_table.c.items()
                          if k.startswith("hap_")])

        query = sql.select([self.edges_table]).select_from(
            self.edges_table.join(self.facts_table, joins)
        ).where(where).distinct()
        for row in self.execute(query):
            yield self._row2edge(row)

    def edges_min_and_max_weights(self):
        """Return a ``tuple`` with ``len == 2`` containing the  edgest with
        minimum ane maximun *weight*

        """
        query = sql.select([self.edges_table]).order_by(
                    self.edges_table.c.weight.asc()
                ).limit(1)
        mine = self._row2edge(self.execute(query).fetchone())
        query = sql.select([self.edges_table]).order_by(
                    self.edges_table.c.weight.desc()
                ).limit(1)
        maxe = self._row2edge(self.execute(query).fetchone())
        return mine, maxe

    def edges_by_weight(self, minweight, maxweight):
        """Iterates of a the ``dom.Edge`` instance with *weight* value between
        ``minweight`` and ``maxwright``

        """
        query = sql.select([self.edges_table]).where(
            self.edges_table.c.weight.between(minweight, maxweight)
        )
        for row in self.execute(query):
            yield self._row2edge(row)

    def edges_by_haplotypes(self, haps):
        """Iterates over all nodes of a given list of haplotypes without
           repetitions

        """
        haps_id = tuple(hap.hap_id for hap in haps)
        where = sql.or_(*[v.in_(haps_id)
                          for k, v in self.edges_table.c.items()
                          if k.startswith("hap_")])
        query = sql.select([self.edges_table]).where(where).distinct()
        for row in self.execute(query):
            yield self._row2edge(row)

    def edges_by_haplotype(self, hap):
        """Iterates over all the edges of a given dom.Haplotype.

        """
        where = sql.or_(*[v == hap.hap_id
                          for k, v in self.edges_table.c.items()
                          if k.startswith("hap_")])
        query = sql.select([self.edges_table]).where(where).distinct()
        for row in self.execute(query):
            yield self._row2edge(row)

    #===========================================================================
    # FACTS QUERIES
    #===========================================================================

    def facts_iterator(self):
        """Iterates over all ``dom.Fact`` instances store in the database."""
        query = sql.select([self.facts_table])
        for row in self.execute(query):
            yield self._row2fact(row)

    def fact_attributes_types(self):
        """Maps a fact attribute name to python type of the atttribute

        """
        self.validate_read()
        types = {}
        for att_name in self.fact_attributes_names():
            column = self.facts_table.c[att_name]
            pptype = None
            for satype in type(column.type).__mro__:
                if satype in PYTHON_TYPES:
                    pptype = PYTHON_TYPES[satype](satype)
                    break
            if pptype:
                types[att_name] = pptype
            else:
                msg = "Hierarchy of '{}' of column '{}' is not valid in yatel"
                raise YatelNetworkError(msg.format(str(column.type), att_name))
        return types

    def fact_attributes_names(self):
        """Return an ``iterator`` of all existing ``dom.Fact`` atributes."""
        self.validate_read()
        for c in sorted(self.facts_table.c.keys()):
            if c not in ("id", "hap_id"):
                yield c

    def fact_attribute_values(self, att_name):
        """Return an ``iterator`` of all posible values of given ``dom.Fact``
        atribute.

        """
        att = self.facts_table.c[att_name]
        query = sql.select([att]).where(att != None).distinct()
        for row in self.execute(query):
            yield row[att_name]

    def facts_by_haplotype(self, hap):
        """Return a ``iterator`` of all facts of a given ``dom.Haplotype``"""
        query = sql.select([self.facts_table]).where(
            self.facts_table.c.hap_id==hap.hap_id
        ).distinct()
        for row in self.execute(query):
            yield self._row2fact(row)

    #===========================================================================
    # PROPERTIES
    #===========================================================================

    @property
    def uri(self):
        """The name of the connection."""
        return self._uri

    @property
    def mode(self):
        return self._mode


#===============================================================================
# FUNCTIONS
#===============================================================================

def format_date(dt):
    """This function prepare the  datetime instance to be stored in the
    database by removing all unused data

    """
    dtf = "%Y-%m-%dT%H:%M:%S"
    return datetime.datetime.strptime(dt.strftime(dtf), dtf)


def parse_uri(uri, mode=MODE_READ, log=None):
    """Create a dictionary for use in creation of YatelNetwork

    ::

        parsed = db.parse_uri("mysql://tito:pass@localhost:2525/mydb",
                               create=True, log=None)
        nw = db.YatelNetwork(**parsed)

    is equivalent to

    ::
        nw = db.YatelNetwork("mysql", database="mydb", user="tito",
                             password="pass", host="localhost", port=2525,
                             create=True, log=None)

    """
    urlo = url.make_url(uri)
    return {"mode": mode, "log": log,
            "engine": urlo.drivername, "database": urlo.database,
            "user": urlo.username, "password": urlo.password,
            "host": urlo.host, "port": urlo.port}


def to_uri(engine, **kwargs):
    """Create a correct uri for a given engine ignorin all unused parameters"""
    tpl = string.Template(ENGINE_URIS[engine])
    engine_vars = ENGINE_VARS[engine]
    kwargs = dict((k, v) for k, v in kwargs.items() if k in engine_vars)
    return tpl.substitute(kwargs)


def exists(engine, **kwargs):
    """Returns true if exists a db.YatelNetwork database in that connection

    """
    kwargs.pop("mode", None)
    try:

        nw = YatelNetwork(engine, mode=MODE_READ, **kwargs)
        hap_id_type = type(nw.haplotypes_table.c.hap_id.type)

        if not (nw.facts_table.c.hap_id.type, hap_id_type):
            raise Exception()

        if not (isinstance(nw.edges_table.c.weight.type, sa.Float)
                and all(isinstance(cv.type, hap_id_type)
                        for cn, cv in nw.edges_table.c.items()
                        if cn not in ("weight", "id"))):
            raise Exception()

    except Exception as err:
        return False
    else:
        return True


def copy(from_nw, to_nw):
    """Copy all the network in ``from_nw`` to the network ``to_nw``.

    ``from_nw`` must be in  read-only mode and ``to_nw`` in write or append mode.
    Is your responsability to call ``to_nw.confirm_changes()`` after the copy

    """
    to_nw.add_elements(from_nw.haplotypes_iterator())
    to_nw.add_elements(from_nw.facts_iterator())
    to_nw.add_elements(from_nw.edges_iterator())


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
