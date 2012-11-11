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
# IMPORTS
#===============================================================================

import datetime
import cPickle
import decimal

import peewee

import dom


#===============================================================================
# CONSTANTS
#===============================================================================

#: Default configuration values for various rdbms supported by ``peewee``.
ENGINES_CONF = {
    "sqlite": {
        "class": peewee.SqliteDatabase,
        "name_isfile": True,
        "params": {}
    },
    "mysql": {
        "class": peewee.MySQLDatabase,
        "name_isfile": False,
        "params": {
            "user": "root",
            "passwd": "",
            "host": "localhost",
            "port": 3306
        }
    },
    "postgres": {
        "class": peewee.PostgresqlDatabase ,
        "name_isfile": False,
        "params": {
            "user": "root",
            "password": "",
            "host": "localhost",
            "port": 5432
        }
    }
}

#: Names of engines supported by ``peewee``.
ENGINES = ENGINES_CONF.keys()

#: ``dict``  with ``peewee`` *field names* as *keys* and *fields* as values.
NAME2FIELD = {
    "CharField": peewee.CharField,
    "TextField": peewee.TextField,
    "DateTimeField": peewee.DateTimeField,
    "IntegerField": peewee.IntegerField,
    "BooleanField": peewee.BooleanField,
    "FloatField": peewee.FloatField,
    "DoubleField": peewee.DoubleField,
    "BigIntegerField": peewee.BigIntegerField,
    "DecimalField": peewee.DecimalField,
    "PrimaryKeyField": peewee.PrimaryKeyField,
    "ForeignKeyField": peewee.ForeignKeyField,
    "DateField": peewee.DateField,
    "TimeField": peewee.TimeField,
}

#: ``dict``  with ``peewee`` *field* as *keys* and *fields names* as values.
FIELD2NAME = dict((v, k) for k, v in NAME2FIELD.items())

#: The name of *haplotype* table type.
HAPLOTYPES_TABLE = "haplotypes"

#: The name of *fact* table type.
FACTS_TABLE = "facts"

#: The name of *edges* table type.
EDGES_TABLE = "edges"

#: The name of all table types.
TABLES = (HAPLOTYPES_TABLE, FACTS_TABLE, EDGES_TABLE)


#===============================================================================
# ERROR
#===============================================================================

class YatelConnectionError(BaseException):
    """Error for use when some *Yatel* logic fail in database."""
    pass


#===============================================================================
# CONNECTION
#===============================================================================

class YatelConnection(object):
    """A database abstraction layer for *Yatel*"""

    def __init__(self, engine, name, **kwargs):
        """Creates a new instance of ``YatelConnection``.

        **NOTE:** Remember to init the database with one of the methods:
            * ``init_with_values``.
            * ``init_yatel_database``.

        **Params**
            :engine: some value specified in ``db.Engines``.
            :name: A database name (or path if ``engine`` is *sqlite*.
            :kwargs: Configuration parameters for the engine (specified in
                     ``db.ENGINES_CON[engine]``.

        """
        try:
            self.database = ENGINES_CONF[engine]["class"](name, **kwargs)
            self.database.connect()
            self._name = "{}://{}/{}".format(engine, kwargs.get("host", "localhost"), name)
            self._inited = False

            class Meta:
                database = self.database
            self.model_meta = Meta

        except KeyError:
            msg = "'engine' must be any of {}, found '{}'"
            raise ValueError(msg.format(ENGINES.keys(), engine))

    def __getattr__(self, k):
        """x.__getattr__('k') <==> x.database.k"""
        if not self._inited:
            msg = "Connection not inited"
            raise YatelConnectionError(msg)
        return getattr(self.database, k)

    #===========================================================================
    # INTERNAL
    def _generate_meta_tables_dbo(self):
        """Generate a internal use tables.

        This tables are used for store the structure to map ``dom`` objects and
        the version status.

        """
        cls_name = property(lambda self: str(self.type[:-1].title() + "DBO"))
        self.YatelTableDBO = type(
            "_yatel_tables", (peewee.Model,), {
                "type": peewee.CharField(unique=True,
                                         choices=[(t, t) for t in TABLES]),
                "name": peewee.CharField(unique=True),
                "cls_name": cls_name,
                "Meta": self.model_meta,
            }
        )
        self.YatelFieldDBO = type(
            "_yatel_fields", (peewee.Model,), {
                "name": peewee.CharField(),
                "table": peewee.ForeignKeyField(self.YatelTableDBO),
                "type": peewee.CharField(),
                "reference_to": peewee.ForeignKeyField(self.YatelTableDBO,
                                                       null=True),
                "is_pk": peewee.BooleanField(default=False),
                "Meta": self.model_meta,
            }
        )
        self.YatelVersionDBO = type(
            "_yatel_versions", (peewee.Model,), {
                "datetime": peewee.DateTimeField(uniqe=True),
                "tag": peewee.CharField(unique=True),
                "data": peewee.TextField(),
                "comment": peewee.TextField(default=""),
                "Meta": self.model_meta,
            }
        )

    def _add_field_metadata(self, name, table, field):
        """Relate a field of existing table to internal structure.

        For example: If the table *A* has identified by yatel as the
        *haplotype table* and we need to use a integer attribute *A.a1*;
        you can use:

        .. code-block:: python

            x._add_field_metadata("a1", "haplotypes", peeweee.IntegerField)

        """
        nf = self.YatelFieldDBO()
        nf.name = name
        nf.table = table
        nf.type = FIELD2NAME[type(field)]
        if isinstance(field, peewee.ForeignKeyField):
            reference_name = field.rel_model.__name__
            nf.reference_to = self.YatelTableDBO.get(name=reference_name)
        nf.is_pk = field.primary_key
        nf.save()

    #===========================================================================
    # INITS
    def init_with_values(self, haps, facts, edges):
        """Init the empety yatel database with the given objects.

        This method:
            * Creates all default tables (for exploration and internal).
            * Maps all attributes of haps, facts and edges.
            * Create a first version (called *init*).

        **Params**
            :haps: A ``list`` of ``dom.Haplotype`` instances.
            :facts: A ``list`` of ``dom.Fact`` instances.
            :edges: A ``list`` of ``dom.Edge`` instances.

        """

        if self._inited:
            msg = "Connection already inited"
            raise YatelConnectionError(msg)

        with self.database.transaction():
            self._generate_meta_tables_dbo()
            self.YatelTableDBO.create_table(fail_silently=False)
            self.YatelFieldDBO.create_table(fail_silently=False)
            self.YatelVersionDBO.create_table(fail_silently=False)

            metatable_haps = self.YatelTableDBO(type=HAPLOTYPES_TABLE,
                                                name=HAPLOTYPES_TABLE)
            metatable_haps.save()
            metatable_facts = self.YatelTableDBO(type=FACTS_TABLE,
                                                 name=FACTS_TABLE)
            metatable_facts.save()
            metatable_edges = self.YatelTableDBO(type=EDGES_TABLE,
                                                 name=EDGES_TABLE)
            metatable_edges.save()

            haps_columns = {"hap_id": []}
            for hap in haps:
                haps_columns["hap_id"].append(hap.hap_id)
                for an, av in hap.items_attrs():
                    if an not in haps_columns:
                        haps_columns[an] = []
                    haps_columns[an].append(av)
            hapdbo_dict = {"Meta": self.model_meta}
            for cn, values in haps_columns.items():
                hapdbo_dict[cn] = field(values, pk=(cn == "hap_id"), null=True)
                self._add_field_metadata(cn, metatable_haps, hapdbo_dict[cn])
            self.HaplotypeDBO = type(HAPLOTYPES_TABLE,
                                     (peewee.Model,),
                                     hapdbo_dict)

            facts_columns = {}
            for fact in facts:
                for an, av in fact.items_attrs():
                    if an not in facts_columns:
                        facts_columns[an] = []
                    facts_columns[an].append(av)
            factsdbo_dict = {"Meta": self.model_meta,
                             "haplotype": peewee.ForeignKeyField(self.HaplotypeDBO)}
            self._add_field_metadata("haplotype", metatable_facts,
                                     factsdbo_dict["haplotype"])
            for cn, values in facts_columns.items():
                factsdbo_dict[cn] = field(values, null=True)
                self._add_field_metadata(cn, metatable_facts, factsdbo_dict[cn])
            self.FactDBO = type(FACTS_TABLE, (peewee.Model,), factsdbo_dict)

            weight_column = []
            max_number_of_haps = 0
            for edge in edges:
                weight_column.append(edge.weight)
                if len(edge.haps_id) > max_number_of_haps:
                    max_number_of_haps = len(edge.haps_id)
            edgesdbo_dict = {
                "Meta": self.model_meta,
                "weight": field(weight_column)
            }
            self._add_field_metadata("weight", metatable_edges,
                                     edgesdbo_dict["weight"])
            for idx in range(max_number_of_haps):
                key = "haplotype_{}".format(idx)
                edgesdbo_dict[key] = peewee.ForeignKeyField(self.HaplotypeDBO,
                                                            null=True)
                self._add_field_metadata(key, metatable_edges,
                                         edgesdbo_dict[key])
            self.EdgeDBO = type(EDGES_TABLE, (peewee.Model,), edgesdbo_dict)

            self.HaplotypeDBO.create_table(fail_silently=True)
            self.FactDBO.create_table(fail_silently=True)
            self.EdgeDBO.create_table(fail_silently=True)

            hap_instances = {}
            for hap in haps:
                hdbo = self.HaplotypeDBO()
                hdbo.hap_id = hap.hap_id
                for an, av in hap.items_attrs():
                    setattr(hdbo, an, av)
                hdbo.save(True)
                hap_instances[hdbo.hap_id] = hdbo

            for fact in facts:
                fdbo = self.FactDBO()
                fdbo.haplotype = hap_instances[fact.hap_id]
                for an, av in fact.items_attrs():
                    setattr(fdbo, an, av)
                fdbo.save(True)

            for edge in edges:
                edbo = self.EdgeDBO()
                edbo.weight = edge.weight
                for idx, hap_id in enumerate(edge.haps_id):
                    key = "haplotype_{}".format(idx)
                    setattr(edbo, key, hap_instances[hap_id])
                edbo.save(True)

            self.save_version(tag="init", comment="first save")
            self._inited = True

    def init_yatel_database(self):
        """Init the connection asumming all the intenal tables of *Yatel*
        exists.

        """
        if self._inited:
            msg = "Connection already inited"
            raise YatelConnectionError(msg)
        with self.database.transaction():
            self._generate_meta_tables_dbo()
            for table_type in TABLES:
                tabledbo = self.YatelTableDBO.get(type=table_type)
                table_dict = {"Meta": self.model_meta}
                for fdbo in self.YatelFieldDBO.filter(table=tabledbo):
                    field_cls = NAME2FIELD[fdbo.type]
                    field = None
                    if field_cls == peewee.ForeignKeyField:
                        ref = getattr(self, fdbo.reference_to.cls_name)
                        field = field_cls(ref)
                    elif fdbo.is_pk:
                        field = field_cls(primary_key=True)
                    else:
                        null = (table_type != EDGES_TABLE
                                or fdbo.name != "weight")
                        field = field_cls(null=null)
                    table_dict[fdbo.name] = field
                peewee_table_cls = type(str(tabledbo.name),
                                        (peewee.Model,), table_dict)
                setattr(self, tabledbo.cls_name, peewee_table_cls)
            self._inited = True

    #===========================================================================
    # QUERIES
    def iter_haplotypes(self):
        """Iterates over all ``dom.Haplotype`` instances store in the database.

        """
        for hdbo in self.HaplotypeDBO.select():
            data = dict((k, v) for k, v in hdbo._data.items()
                         if v is not None)
            yield dom.Haplotype(**data)

    def iter_edges(self):
        """Iterates over all ``dom.Edge`` instances store in the database."""
        for edbo in self.EdgeDBO.select():
            weight = edbo.weight
            haps_id = [v for k, v in edbo._data.items()
                       if k.startswith("haplotype_") and v is not None]
            yield dom.Edge(weight, *haps_id)

    def iter_facts(self):
        """Iterates over all ``dom.Fact`` instances store in the database."""
        for fdbo in self.FactDBO.select():
            data = {}
            for k, v in fdbo._data.items():
                if k == "haplotype":
                    data["hap_id"] = v
                elif k != "id" and v is not None:
                    data[k] = v
            yield dom.Fact(**data)

    def haplotype_by_id(self, hap_id):
        """Return a ``dom.Haplotype`` instace store in the dabase with the
        giver ``hap_id``.

        **Params**
            :hap_id: An existing id of the ``haplotypes`` type table.

        **Return**
            ``dom.Haplotype`` instance.

        """
        hdbo = self.HaplotypeDBO.get(self.HaplotypeDBO.hap_id == hap_id)
        data = dict((k, v) for k, v in hdbo._data.items() if v is not None)
        return dom.Haplotype(**data)

    def enviroment(self, **kwargs):
        """Return a list of ``dom.Haplotype`` related to a ``dom.Fact`` with
        attribute and value specified in ``kwargs``

        **Params**
            :kwargs: Keys are ``dom.Fact`` attribute name and value a posible
                     value of the given attribte.

        **Return**
            ``tuple`` of ``dom.Haplotype``.

        **Example**

            ::

                >>> from yatel import db, dom
                >>> haps = (dom.Haplotype("hap1"), dom.Haplotype("hap2"))
                >>> facts = (dom.Fact("hap1", a=1, c="foo"), dom.Fact("hap2", a=1, b=2))
                >>> edges = (dom.Edge(1, "hap1", "hap2"),)
                >>> conn = db.YatelConnection("sqlite", "yateldatabase.db")
                >>> conn.init_with_values(haps, facts, edges)
                >>> conn.enviroment(a=1)
                (<Haplotype 'hap1' at 0x2463250>, <Haplotype 'hap2' at 0x2463390>)
                >>> conn.enviroment(c="foo")
                (<Haplotype 'hap1' at 0x2463250>, )
                >>> conn.enviroment(b=2)
                (<Haplotype 'hap2' at 0x2463390>, )

        """
        haps = {}
        queries = []
        for k, v in kwargs.items():
            field = getattr(self.FactDBO, k)
            query = None
            if v is None:
                query = (field >> None)
            else:
                query = (field == v)
            queries.append(query)
        for fdbo in self.FactDBO.filter(*queries):
            hap_id = fdbo._data["haplotype"]
            if  hap_id not in haps:
                haps[hap_id] = self.haplotype_by_id(hap_id)
        return tuple(haps.values())

    def facts_attributes_names(self):
        """Return a ``tuple`` of all existing ``dom.Fact`` atributes."""
        yt_dbo = self.YatelTableDBO.get(self.YatelTableDBO.type == FACTS_TABLE)
        query = self.YatelFieldDBO.filter(self.YatelFieldDBO.table == yt_dbo)
        query = query.filter(self.YatelFieldDBO.reference_to >> None)
        return tuple(tfdbo.name for tfdbo in query)

    def fact_attribute_values(self, att_name):
        """Return a ``frozenset`` of all posible values of given ``dom.Fact``
           atribute.

        """
        values = set()
        for fdbo in self.FactDBO.select():
            v = getattr(fdbo, att_name)
            if v is not None:
                values.add(v)
        return tuple(values)


    def minmax_edges(self):
        """Return a ``tuple`` with ``len == 2`` containing the  edgest with
        minimum ane maximun *weight*

        """

        minedge = None
        maxedge = None
        query = self.EdgeDBO.select()
        query = query.order_by(self.EdgeDBO.weight.asc()).limit(1)
        for edbo in query:
            weight = edbo.weight
            haps_id = [v for k, v in edbo._data.items()
                       if k.startswith("haplotype_") and v is not None]
            minedge = dom.Edge(weight, *haps_id)
        query = self.EdgeDBO.select()
        query = query.order_by(self.EdgeDBO.weight.desc()).limit(1)
        for edbo in query:
            weight = edbo.weight
            haps_id = [v for k, v in edbo._data.items()
                       if k.startswith("haplotype_") and v is not None]
            maxedge = dom.Edge(weight, *haps_id)
        return minedge, maxedge

    def filter_edges(self, minweight, maxweight):
        """Iterates of a the ``dom.Edge`` instance with *weight* value between
        ``minweight`` and ``maxwright``

        """
        for edbo in self.EdgeDBO.filter(self.EdgeDBO.weight >= minweight,
                                        self.EdgeDBO.weight <= maxweight):
            weight = edbo.weight
            haps_id = [v for k, v in edbo._data.items()
                       if k.startswith("haplotype_") and v is not None]
            yield dom.Edge(weight, *haps_id)

    def hap_sql(self, query, *args):
        """Trye to execute an arbitrary *sql* and return the
        ``dom.Haplotype`` instances selected by the query.

        NOTE: Init all queries with ``select * from <HAPLOTYPE_TABLE>``

        **Params**
            :query: The *sql* query.
            :args: Argument to replace the ``?`` in the query.

        **Returns**
            A ``tuple`` of ``dom.Haplotype`` instance.

        """
        haps = []
        for hdbo in self.HaplotypeDBO.raw(query, *args):
            hap = dom.Haplotype(**hdbo._data)
            haps.append(hap)
        return tuple(haps)

    def save_version(self, tag, comment="", hap_sql="",
                     topology={}, weight_range=(None, None), enviroments=()):
        """Store a new exploration status version in the database.

        **Params**
            :tag: The tag of the new version (unique).
            :comment: A comment about the new version.
            :hap_sql: For execute in ``YatelConnection.hap_sql``.
            :topology: A dictionary with ``dom.Haplotype`` instances as keys
                       and a *iterable* with (x, y) position as value.
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
        for hap, xy in topology.items():

            # validate if this hap is in this nejbc.develop@gmail.comtwork
            self.HaplotypeDBO.get(hap_id=hap.hap_id)
            td[hap.hap_id] = list(xy)

        minw, maxw = weight_range
        if minw > maxw:
            raise ValueError("Invalid range: ({}, {})".format(minw, maxw))
        wrl = [minw, maxw]

        envl = []
        for active, enviroment in enviroments:
            active = bool(active)
            for varname, varvalue in enviroment.items():
                if varname not in self.facts_attributes_names():
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

        vdbo = self.YatelVersionDBO()
        vdbo.tag = tag
        vdbo.datetime = datetime.datetime.now()
        vdbo.comment = comment
        vdbo.data = cPickle.dumps(data).encode("base64")

        query = self.YatelVersionDBO.select()
        if query.count():
            query = query.order_by(self.YatelVersionDBO.datetime.desc())
            vdbo_old = tuple(query.limit(1))[0]
            if vdbo.data == vdbo_old.data:
                msg = "Nothing changed from the last version '{}'"
                msg = msg.format(vdbo.tag)
                raise ValueError(msg)
        vdbo.save()
        return vdbo.id, vdbo.datetime, vdbo.tag

    def versions(self):
        """A ``tuple`` with all existing versions.

        Each element contains 3 elements: the  version ``id``, the  version
        ``datetime`` of creation, and the  version ``tag``

        """
        versions = []
        query = self.YatelVersionDBO.select()
        query = query.order_by(self.YatelVersionDBO.id.desc())
        for vdbo in query:
            versions.append((vdbo.id, vdbo.datetime, vdbo.tag))
        return tuple(versions)

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
        vdbo = None
        if match is None:
            query = self.YatelVersionDBO.select()
            query = query.order_by(self.YatelVersionDBO.datetime.desc())
            vdbo = tuple(query.limit(1))[0]
        elif isinstance(match, int):
            vdbo = self.YatelVersionDBO.get(self.YatelVersionDBO.id == match)
        elif isinstance(match, datetime.datetime):
            vdbo = self.YatelVersionDBO.get(self.YatelVersionDBO.datetime == match)
        elif isinstance(match, basestring):
            vdbo = self.YatelVersionDBO.get(self.YatelVersionDBO.tag == match)
        else:
            msg = "Match must be None, int, str, unicode or datetime instance"
            raise TypeError(msg)

        version = cPickle.loads(vdbo.data.decode("base64"))

        topology = {}
        for hap_id, xy in version["topology"].items():
            topology[self.haplotype_by_id(hap_id)] = tuple(xy)

        version["topology"] = topology
        version["tag"] = vdbo.tag
        version["id"] = vdbo.id
        version["datetime"] = vdbo.datetime
        version["comment"] = vdbo.comment
        return version

    @property
    def name(self):
        """The name of the connection."""
        return self._name

    @property
    def inited(self):
        """If the connection is innited."""
        return self._inited


#===============================================================================
# FUNCTIONS
#===============================================================================

def field(objs, pk=False, **kwargs):
    """Create a peewee field type for a given iterable of objects

        CharField <- str or unicode with len < 255 or pk == True
        TextField <- str or unicode with len > 255
        DateTimeField <- datetime.datetime object
        BooleanField <- bool
        IntegerField <- int between (-32000, 32000)
        BigIntegerField <- int outside (-32000, 32000)
        FloatField <- float between (-32000, 32000)
        DoubleField <- float > outside (-32000, 32000)
        DecimalField <- decimal.Decimal
        DateField <- datetime.Date
        TimeField <- datetime.time
        PrimaryKeyField <- with class based on previous items and pk == True

    """
    peek = objs[0]
    peewee_field = None
    if isinstance(peek, basestring):
        if pk or max(map(len, objs)) < 255:
            peewee_field = peewee.CharField
        else:
            peewee_field = peewee.TextField
    elif isinstance(peek, datetime.datetime):
        peewee_field = peewee.DateTimeField
    elif isinstance(peek, bool):
        peewee_field = peewee.BooleanField
    elif isinstance(peek, int):
        if min(objs) < 32000 or max(objs) > 32000:
            peewee_field = peewee.BigIntegerField
        else:
            peewee_field = peewee.IntegerField
    elif isinstance(peek, float):
        if min(objs) < 32000 or max(objs) > 32000:
            peewee_field = peewee.DoubleField
        else:
            peewee_field = peewee.FloatField
    elif isinstance(peek, decimal.Decimal):
        peewee_field = peewee.DecimalField
    elif isinstance(peek, datetime.date):
        peewee_field = peewee.DateField
    elif isinstance(peek, datetime.time):
        peewee_field = peewee.DateTimeField
    if pk:
        kwargs.pop("null", None)
        kwargs["primary_key"] = True
    return peewee_field(**kwargs)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

