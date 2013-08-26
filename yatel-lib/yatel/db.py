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
import cPickle

from yatel import dom

import sqlalchemy as sa
from sqlalchemy import sql
from sqlalchemy.engine import url


#===============================================================================
# EXCEPTIONS
#===============================================================================

# The order to show ENGINE variables, if it not in this list put at the end
VARS_ENGINE_ORDER = ("database", "user", "password", "dsn", "host", "port")


ENGINES = (
    'sqlite',
    'memory',
    'mysql',
    'postgresql',
)


ENGINE_URIS = {
    'sqlite': "sqlite:///${database}",
    'memory': "sqlite://",
    'mysql': "mysql://${user}:${password}@${host}:${port}/${database}",
    'postgresql': "postgresql://${user}:${password}@${host}:${port}/${database}"
}


ENGINE_VARS = {}
for engine in ENGINES:
    tpl = string.Template(ENGINE_URIS[engine])
    variables = []
    for e, n, b, i in tpl.pattern.findall(tpl.template):
        if n or b:
            variables.append(n or b)
    variables.sort(key=lambda v: VARS_ENGINE_ORDER.index(v))
    ENGINE_VARS[engine] = variables


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

# TABLE NAMES

HAPLOTYPES = "haplotypes"

FACTS = "facts"

EDGES = "edges"

VERSIONS = "versions"

TABLES = (HAPLOTYPES, FACTS, EDGES, VERSIONS)


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

    def __init__(self, engine, create=False, log=None, **kwargs):

        self._uri = to_uri(engine, **kwargs)

        self._engine = sa.create_engine(self._uri, echo=bool(log))
        self._metadata = sa.MetaData(self._engine)

        self._hapid_buff = {}
        self._dbid_buff = {}
        self._create_mode = create

        if self._create_mode:
            tpl = string.Template(ENGINE_URIS["sqlite"])
            self._column_buff = {HAPLOTYPES: [], FACTS: [], EDGES: 0}
            self._tmp_dbfile = tempfile.NamedTemporaryFile(suffix="_yatel")
            self._tmp_meta = sa.MetaData(
                tpl.substitute(database=self._tmp_dbfile.name)
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
            self._metadata.reflect(only=TABLES)
            self.versions_table = self._metadata.tables[VERSIONS]
            self.haplotypes_table = self._metadata.tables[HAPLOTYPES]
            self.facts_table = self._metadata.tables[FACTS]
            self.edges_table = self._metadata.tables[EDGES]

    #===========================================================================
    # PRIVATE
    #===========================================================================

    def _is_version(self, obj):
        columns = {'comment': basestring, 'data': object,
                   'datetime': datetime.datetime,
                   'id': int, 'tag': basestring}
        is_version = True
        if isinstance(obj, dict) and len(obj) == len(columns) \
           and sorted(obj.keys()) == sorted(columns.keys()):
               for c, ct in columns.items():
                    if not isinstance(obj[c], ct):
                        is_version = False
                        break
        else:
            is_version = False
        return is_version

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

    def _row2version(self, row):
        ver = dict(row)
        if isinstance(row.data, basestring):
            ver["data"] = cPickle.loads(row.data)
        return ver

    #===========================================================================
    # DDL METHODS
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
            if len(elem.haps_id) > self._column_buff[EDGES]:
                self._column_buff[EDGES] = len(elem.haps_id)
            data = {}
            for idx, hap_id in enumerate(elem.haps_id):
                data["hap_{}".format(idx)] = hap_id
            data["weight"] = elem.weight
            tname = EDGES

        # version dictionary
        elif self._is_version(elem):
            data = elem
            data.update(datetime=format_date(elem["datetime"]))
            tname = VERSIONS

        # if is trash
        else:
            msg = "Object '{}' is not yatel.dom type".format(str(elem))
            raise TypeError(msg)
        self._tmp_conn.execute(self._tmp_objects.insert(),
                               tname=tname, data=data)

    def end_creation(self):

        if self.created:
            raise YatelNetworkError("Network already created")

        # first confirm all changes to the temp database
        self._tmp_trans.commit()

        with self._metadata.bind.begin() as conn:

            self._metadata.reflect(conn, only=lambda n, m: n in TABLES)
            self._metadata.drop_all(conn)
            self._metadata.clear()

            # create te tables
            self.versions_table = sa.Table(
                VERSIONS, self._metadata,
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("tag", sa.String(512), unique=True, nullable=False),
                sa.Column("datetime", sa.DateTime(), nullable=False),
                sa.Column("comment", sa.Text(), nullable=False),
                sa.Column("data", sa.PickleType(), nullable=False),
            )

            self.haplotypes_table = sa.Table(
                HAPLOTYPES, self._metadata, *self._column_buff[HAPLOTYPES]
            )

            self.facts_table = sa.Table(
                FACTS, self._metadata,
                sa.Column("id", sa.Integer(), primary_key=True),
                *self._column_buff[FACTS]
            )

            edges_columns = [
                sa.Column("hap_{}".format(idx), self.haplotypes_table.c.hap_id.type,
                          sa.ForeignKey(HAPLOTYPES + '.hap_id'), nullable=True)
                for idx in range(self._column_buff[EDGES])
            ]
            self.edges_table = sa.Table(
                EDGES, self._metadata,
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("weight", sa.Float(), nullable=False),
                *edges_columns
            )

            self._metadata.create_all(conn)

            query = sql.select([self._tmp_objects])
            for row in self._tmp_conn.execute(query):
                table = None
                if row.tname == HAPLOTYPES:
                    table = self.haplotypes_table
                elif row.tname == FACTS:
                    table = self.facts_table
                elif row.tname == EDGES:
                    table = self.edges_table
                elif row.tname == VERSIONS:
                    table = self.versions_table
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
        if not self.versions_count():
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
        query = sql.select([self.haplotypes_table])
        for row in self.execute(query):
            yield self._row2hap(row)

    def haplotypes_by_ids(self, haps_ids):
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

    def fact_attributes_names(self):
        """Return a ``iterator`` of all existing ``dom.Fact`` atributes."""
        for c in self.facts_table.c:
            if c.name not in ("id", "hap_id"):
                yield c.name

    def fact_attribute_values(self, att_name):
        """Return a ``iterator`` of all posible values of given ``dom.Fact``
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
    # VERSIONS QUERIES
    #===========================================================================

    def versions_infos_interator(self):
        """A ``iterator`` with all existing versions.

        Each element contains 3 elements: the  version ``id``, the  version
        ``datetime`` of creation, and the  version ``tag``

        """
        query = sql.select([self.versions_table.c.id,
                            self.versions_table.c.datetime,
                            self.versions_table.c.tag])
        for row in self.execute(query):
            yield dict(row)

    def versions_iterator(self):
        """This function iterate over all versions

        WARNING: this is used only with dump propuses, use get_version for
        retrieve a particular version

        """
        query = sql.select([self.versions_table])
        for row in self.execute(query):
            yield self._row2version(row)

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
            weight_range = [e.weight for e in self.edges_min_and_max_weights()]
        minw, maxw = weight_range
        nwmin, nwmax = [e.weight for e in self.edges_min_and_max_weights()]
        if minw > maxw or minw < nwmin \
           or minw > nwmax or maxw > nwmax or maxw < nwmin:
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

        query = sql.insert(self.versions_table).values(
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
        query = sql.select([self.versions_table])
        if match is None:
            query = query.order_by(self.versions_table.c.datetime.desc())
        elif isinstance(match, int):
            query = query.where(self.versions_table.c.id==match)
        elif isinstance(match, datetime.datetime):
            match = format_date(match)
            query = query.where(self.versions_table.c.datetime==match)
        elif isinstance(match, basestring):
            query = query.where(self.versions_table.c.tag==match)
        else:
            msg = "Match must be None, int, str, unicode or datetime instance"
            raise TypeError(msg)
        query = query.limit(1)
        row = self.execute(query).fetchone()
        return self._row2version(row)

    def versions_count(self):
        """Return how many versions are stored"""
        return sql.select([self.versions_table.c.id]).count().scalar()

    #===========================================================================
    # PROPERTIES
    #===========================================================================

    @property
    def uri(self):
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


def parse_uri(uri, create=False, log=None):
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
    return {"create": create, "log": log,
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
    kwargs.pop("create", None)
    try:

        nw = YatelNetwork(engine, create=False, **kwargs)
        hap_id_type = type(nw.haplotypes_table.c.hap_id.type)

        if not (nw.facts_table.c.hap_id.type, hap_id_type):
            raise Exception()

        if not (isinstance(nw.edges_table.c.weight.type, sa.Float)
                and all(isinstance(cv.type, hap_id_type)
                        for cn, cv in nw.edges_table.c.items()
                        if cn not in ("weight", "id"))):
            raise Exception()

        if not (isinstance(nw.versions_table.c.id.type, sa.Integer)
                and isinstance(nw.versions_table.c.tag.type, sa.String)
                and isinstance(nw.versions_table.c.comment.type, sa.Text)
                and isinstance(nw.versions_table.c.datetime.type, sa.DateTime)
                and nw.versions_table.c.data.type):
            raise Exception()
    except Exception as err:
        return False
    else:
        return True


def copy(from_nw, to_nw):
    """Copy all the network in ``from_nw`` to the network ``to_nw``.

    ``from_nw`` must be created and ``to_nw`` in create mode. Is your
    responsability to call ``to_nw.end_creation()`` after the copy

    """
    to_nw.add_elements(from_nw.haplotypes_iterator())
    to_nw.add_elements(from_nw.facts_iterator())
    to_nw.add_elements(from_nw.edges_iterator())
    to_nw.add_elements(from_nw.versions_iterator())



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
