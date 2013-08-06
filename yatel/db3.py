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
    'memory',
    #"mysql",
    #"postgres",

)

SCHEMA_URIS = {
    'sqlite': "sqlite:///${dbname}",
    'memory': "sqlite://",
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

    def __init__(self, schema, create=False, log=None, **kwargs):
        tpl = string.Template(SCHEMA_URIS[schema])
        self._uri = tpl.substitute(kwargs)

        self._engine = sa.create_engine(self._uri, echo=bool(log))
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

    def add_elements(self, elems):
        map(self.add_element, elems)

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
            query = sql.select([self._tmp_objects])
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
        self.save_version(tag="init", comment="-* AUTO CREATED *-")

    #===========================================================================
    # QUERIES # use execute here
    #===========================================================================

    def execute(self, query):
        """Execute a given query to the backend"""
        if not self.created:
            raise YatelNetworkError("Network not created")
        return self._engine.execute(query)

    #===========================================================================
    # HAPLOTYPE QUERIES
    #===========================================================================

    def haplotypes_iterator(self):
        """Iterates over all ``dom.Haplotype`` instances store in the database.

        """
        query = sql.select([self._haplotypes_table])
        for row in self.execute(query):
            yield self._row2hap(row)

    def haplotypes_by_ids(self, haps_ids):
        query = sql.select([self._haplotypes_table]).where(
            self._haplotypes_table.c.hap_id.in_(haps_ids)
        ).limit(1)
        for row in row = self.execute(query):
            yield self._row2hap(row)

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
                >>> conn.enviroment(a=1)
                (<Haplotype 'hap1' at 0x2463250>, <Haplotype 'hap2' at 0x2463390>)
                >>> conn.enviroment({"c": "foo"})
                (<Haplotype 'hap1' at 0x2463250>, )
                >>> conn.enviroment({"a": 1}, b=2)
                (<Haplotype 'hap2' at 0x2463390>, )

        """
        env = env or {}
        env.update(kwargs)
        where = sql.and_(*[self._facts_table.c[k] == v
                           for k, v in env.items()])
        query = sql.select([self._haplotypes_table]).select_from(
            self._haplotypes_table.join(
                self._facts_table,
                self._facts_table.c.hap_id == self._haplotypes_table.c.hap_id
            )
        ).where(where).distinct()
        for row in self.execute(query):
            yield self._row2hap(row)

    #===========================================================================
    # EDGES QUERIES
    #===========================================================================

    def edges_iterator(self):
        """Iterates over all ``dom.Edge`` instances store in the database."""
        query = sql.select([self._edges_table])
        for row in self.execute(query):
            yield self._row2edge(row)

    def edges_enviroment(self, env=None, **kwargs):
        """Iterates over all ``dom.Edge`` instances of a given enviroment"""
        env = env or {}
        env.update(kwargs)
        where = sql.and_(*[self._facts_table.c[k] == v
                           for k, v in env.items()])

        joins = sql.or_(*[v == self._facts_table.c.hap_id
                          for k, v in self._edges_table.c.items()
                          if k.startswith("hap_")])

        query = sql.select([self._edges_table]).select_from(
            self._edges_table.join(self._facts_table, joins)
        ).where(where).distinct()
        for row in self.execute(query):
            yield self._row2edge(row)

    def edges_top_weights(self):
        """Return a ``tuple`` with ``len == 2`` containing the  edgest with
        minimum ane maximun *weight*

        """
        query = sql.select([self._edges_table]).order_by(
                    self._edges_table.c.weight.asc()
                ).limit(1)
        mine = self._row2edge(self.execute(query).fetchone())
        query = sql.select([self._edges_table]).order_by(
                    self._edges_table.c.weight.desc()
                ).limit(1)
        maxe = self._row2edge(self.execute(query).fetchone())
        return mine, maxe

    def edges_by_weight(self, minweight, maxweight):
        """Iterates of a the ``dom.Edge`` instance with *weight* value between
        ``minweight`` and ``maxwright``

        """
        query = sql.select([self._edges_table]).where(
            self._edges_table.c.weight.between(minweight, maxweight)
        )
        for row in self.execute(query):
            yield self._row2edge(row)

    def edges_by_haplotypes(self, haps):
        """Iterates over all nodes of a given list of haplotypes without
           repetitions

        """
        haps_id = tuple(hap.hap_id for hap in haps)
        where = sql.or_(*[v.in_(haps_id)
                          for k, v in self._edges_table.c.items()
                          if k.startswith("hap_")])
        query = sql.select([self._edges_table]).where(where).distinct()
        for row in self.execute(query):
            yield self._row2edge(row)

    def edges_by_haplotype(self, hap):
        """Iterates over all the edges of a given dom.Haplotype.

        """
        where = sql.or_(*[v == hap.hap_id
                          for k, v in self._edges_table.c.items()
                          if k.startswith("hap_")])
        query = sql.select([self._edges_table]).where(where).distinct()
        for row in self.execute(query):
            yield self._row2edge(row)

    #===========================================================================
    # FACTS QUERIES
    #===========================================================================

    def facts_iterator(self):
        """Iterates over all ``dom.Fact`` instances store in the database."""
        query = sql.select([self._facts_table])
        for row in self.execute(query):
            yield self._row2fact(row)

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
    # VERSIONS QUERIES
    #===========================================================================

    def versions_infos_interator(self):
        """A ``iterator`` with all existing versions.

        Each element contains 3 elements: the  version ``id``, the  version
        ``datetime`` of creation, and the  version ``tag``

        """
        query = sql.select([self._versions_table.c.id,
                            self._versions_table.c.datetime,
                            self._versions_table.c.tag])
        for row in self.execute(query):
            yield dict(row)

    def versions_iterator(self):
        """This function iterate over all versions

        WARNING: this is used only with dump propuses, use get_version for
        retrieve a particular version

        """
        query = sql.select([self._versions_table])
        for row in self.execute(query):
            yield dict(row)

    def save_version(self, tag, comment="", hap_sql="",
                     topology={}, weight_range=(None, None), enviroments=()):
        """Store a new exploration status version in the database.

        **Params**
            :tag: The tag of the new version (unique).
            :comment: A comment about the new version.
            :hap_sql: For execute in ``YatelConnection.hap_sql``.
            :topology: A dictionary with hap_ids as keys and a *iterable*
                       with (x, y) position as value.
            :weight_tange: A *iterable* with two ``int`` or ``float``
                           representing the relevante ``dom.Edge`` instance.
            :enviroments: A *iterable* with 2 values: **1** a ``bool``
                          representing if the enviroment is active or not;
                          **2** A ``dict`` with ``dom.Fact`` attribute name
                          as keys, and attribute value as value.

        **Returns**
            A ``tuple`` with 3 values: the new version ``id``, the new version
            ``datetime`` of creation, and the new version ``tag``.

        """
        td = {}
        for hap_id, xy in topology.items():
            # validate if this hap is in this network
            self.haplotype_by_id(hap_id)
            td[hap_id] = list(xy)

        if not all(weight_range):
            weight_range = [e.weight for e in self.edges_top_weights()]
        minw, maxw = weight_range
        nwmin, nwmax = [e.weight for e in self.edges_top_weights()]
        if minw > maxw \
           or minw < nwmin \
           or minw > nwmax \
           or maxw > nwmax \
           or maxw < nwmin:
            raise ValueError("Invalid range: ({}, {})".format(minw, maxw))
        wrl = [minw, maxw]

        envl = []
        for active, enviroment in enviroments:
            active = bool(active)
            for varname, varvalue in enviroment.items():
                if varname not in self.fact_attributes_names():
                    msg = "Invalid fact attribute: '{}'".format(varname)
                    raise ValueError(msg)
                if (varvalue is not None
                    and varvalue not in self.fact_attribute_values(varname)):
                        msg = "Invalid value '{}' for fact attribute '{}'"
                        msg = msg.format(varvalue, varname)
                        raise ValueError(msg)
            envl.append([active, enviroment])

        data = {"topology": td, "weight_range": wrl,
                "enviroments": envl, "hap_sql": hap_sql}

        try:
            old_data = self.get_version()["data"]
        except:
            pass
        else:
            if data == old_data:
                msg = "Nothing changed from the last version '{}'"
                msg = msg.format(vdbo.tag)
                raise ValueError(msg)

        query = sql.insert(self._versions_table).values(
            tag=tag, datetime=format_date(datetime.datetime.now()),
            comment=comment, data=data)
        self.execute(query)


    def get_version(self, match=None):
        """Return a version by the given filter.

        Behavior:
            * If ``match`` is ``None``: The last version is returned.
            * If ``match`` is instance of ``int``: The search is by version
              *id*.
            * If ``match`` is instance of ``datetime``: The search is by
              version creation *datetime*.
            * If ``match`` is instance of ``str``: The search is by version
              *tag*.

        """
        query = sql.select([self._versions_table])
        if match is None:
            query = query.order_by(self._versions_table.c.datetime.desc())
        elif isinstance(match, int):
            query = query.where(self._versions_table.c.id==match)
        elif isinstance(match, datetime.datetime):
            match = format_date(match)
            query = query.where(self._versions_table.c.datetime==match)
        elif isinstance(match, basestring):
            query = query.where(self._versions_table.c.tag==match)
        else:
            msg = "Match must be None, int, str, unicode or datetime instance"
            raise TypeError(msg)
        query = query.limit(1)
        row = self.execute(query).fetchone()
        return dict(row)

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

def format_date(dt):
    """This function prepare the  datetime instance to be stored in the
    database by removing all unused data

    """
    dtf = "%Y-%m-%dT%H:%M:%S"
    return datetime.datetime.strptime(dt.strftime(dtf), dtf)


#===============================================================================
# MAIN
#===============================================================================

def _test():
    conn = YatelNetwork("memory", create=True)
    conn.add_elements([dom.Haplotype("hap1"),
                       dom.Haplotype("hap2"),
                       dom.Fact("hap1", a=1, c="foo"),
                       dom.Fact("hap2", a=1, b=2),
                       dom.Edge(1, "hap1", "hap2")])
    conn.end_creation()
    return conn

if __name__ == "__main__":
    print(__doc__)
