#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.


#===============================================================================
# DOCS
#===============================================================================

"""Database interface for yatel

"""

#===============================================================================
# IMPORTS
#===============================================================================

import sys
import datetime
import os
import json
import decimal

import peewee

import dom


#===============================================================================
# CONSTANTS
#===============================================================================

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

ENGINES = ENGINES_CONF.keys()

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

FIELD2NAME = dict((v, k) for k, v in NAME2FIELD.items())

NAME2COLUMNCLASS = dict(
    (v.column_class.__name__, v.column_class) for v in NAME2FIELD.values()
)

COLUMNCLASS2NAME = dict((v, k) for k, v in NAME2COLUMNCLASS.items())

HAPLOTYPES_TABLE = "haplotypes"

FACTS_TABLE = "facts"

EDGES_TABLE = "edges"

TABLES = (HAPLOTYPES_TABLE, FACTS_TABLE, EDGES_TABLE)


#===============================================================================
# ERROR
#===============================================================================

class YatelConnectionError(BaseException):
    pass


#===============================================================================
# CONNECTION
#===============================================================================

class YatelConnection(object):

    def __init__(self, engine, name, **kwargs):
        """
            engine: sqlite, mysql or postgres

        """
        try:
            self.database = ENGINES_CONF[engine]["class"](name, **kwargs)
            self.database.connect()
            self._name = "{}://{}/{}".format(engine, kwargs.get("host", "localhost"), name)
            self._minmaxedge = None
            self._versions = None
            self._inited = False

            class Meta:
                database = self.database
            self.model_meta = Meta

        except KeyError:
            msg = "'engine' must be any of {}, found '{}'"
            raise ValueError(msg.format(ENGINES.keys(), engine))

    def __getattr__(self, k):
        if not self._inited:
            msg = "Connection not inited"
            raise YatelConnectionError(msg)
        return getattr(self.database, k)

    def _generate_meta_tables_dbo(self):
        self.YatelTableDBO = type(
            "_yatel_tables", (peewee.Model,), {
                "type": peewee.CharField(unique=True,
                                         choices=[(t, t) for t in TABLES]),
                "name": peewee.CharField(unique=True),
                "cls_name": property(lambda self: str(self.type[:-1].title()
                                                       + "DBO")),
                "Meta": self.model_meta,
            }
        )
        self.YatelFieldDBO = type(
            "_yatel_fields", (peewee.Model,), {
                "name": peewee.CharField(),
                "table": peewee.ForeignKeyField(self.YatelTableDBO),
                "type": peewee.CharField(),
                "reference_to": peewee.ForeignKeyField(self.YatelTableDBO, null=True),
                "pk_column_class": peewee.CharField(null=True),
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
        nf = self.YatelFieldDBO()
        nf.name = name
        nf.table = table
        nf.type = FIELD2NAME[type(field)]
        if isinstance(field, peewee.ForeignKeyField):
            reference_name = field.to.__name__
            table_reference = self.YatelTableDBO.get(name=reference_name)
            nf.reference_to = self.YatelTableDBO.get(name=reference_name)
        elif isinstance(field, peewee.PrimaryKeyField):
            nf.pk_column_class = COLUMNCLASS2NAME[field.column_class]
        nf.save()

    def init_with_values(self, haps, facts, edges):

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
            factsdbo_dict = {
                "Meta": self.model_meta,
                "haplotype": peewee.ForeignKeyField(self.HaplotypeDBO)
            }
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
                    elif field_cls == peewee.PrimaryKeyField:
                        column_class = NAME2COLUMNCLASS[fdbo.pk_column_class]
                        field = field_cls(column_class)
                    else:
                        null = (table_type != EDGES_TABLE
                                or fdbo.name != "weight")
                        field = field_cls(null=null)
                    table_dict[fdbo.name] = field
                peewee_table_cls = type(str(tabledbo.name),
                                        (peewee.Model,), table_dict)
                setattr(self, tabledbo.cls_name, peewee_table_cls)
            self._inited = True

    def haplotype_by_id(self, hap_id):
        hdbo = self.HaplotypeDBO.get(hap_id=hap_id)
        data = dict(
            (k, v)
            for k, v in hdbo.get_field_dict().items()
            if v is not None
        )
        return dom.Haplotype(**data)

    def iter_haplotypes(self):
        for hdbo in self.HaplotypeDBO.select():
            data = dict(
                (k, v)
                for k, v in hdbo.get_field_dict().items()
                if v is not None
            )
            yield dom.Haplotype(**data)

    def iter_edges(self):
        for edbo in self.EdgeDBO.select():
            weight = edbo.weight
            haps_id = [
                v for k, v in edbo.get_field_dict().items()
                if k.startswith("haplotype_") and v is not None
            ]
            yield dom.Edge(weight, *haps_id)

    def iter_facts(self):
        for fdbo in self.FactDBO.select():
            data = {}
            for k, v in fdbo.get_field_dict().items():
                if k == "haplotype":
                    data["hap_id"] = v
                elif k != "id" and v is not None:
                    data[k] = v
            yield dom.Fact(**data)

    def ambient(self, **kwargs):
        haps = {}
        query = {}
        for k, v in kwargs.items():
            if v is None:
                k += "__is"
            query[k] = v
        for fdbo in self.FactDBO.filter(**query):
            hap_id = fdbo.get_field_dict()["haplotype"]
            if  hap_id not in haps:
                hdbo = fdbo.haplotype
                haps[hap_id] = dom.Haplotype(**hdbo.get_field_dict())
        return tuple(haps.values())

    def facts_attributes_names(self):
        return tuple([
            k for k, v in vars(self.FactDBO).items()
            if not k.startswith("_")
            and isinstance(v, peewee.FieldDescriptor)
            and k != "id"
        ])

    def get_fact_attribute_values(self, att_name):
        query = {att_name + "__is": None}
        return frozenset(
            getattr(fdbo, att_name)
            for fdbo in self.FactDBO.filter(~peewee.Q(**query))
        )

    def min_max_edge(self):
        if self._minmaxedge is None:
            minedge = None
            maxedge = None
            query = self.EdgeDBO.select().order_by(("weight", "ASC")).limit(1)
            for edbo in query:
                weight = edbo.weight
                haps_id = [
                    v for k, v in edbo.get_field_dict().items()
                    if k.startswith("haplotype_") and v is not None
                ]
                minedge = dom.Edge(weight, *haps_id)
            query = self.EdgeDBO.select().order_by(("weight", "DESC")).limit(1)
            for edbo in query:
                weight = edbo.weight
                haps_id = [
                    v for k, v in edbo.get_field_dict().items()
                    if k.startswith("haplotype_") and v is not None
                ]
                maxedge = dom.Edge(weight, *haps_id)
            self._minmaxedge = minedge, maxedge
        return self._minmaxedge

    def filter_edges(self, minweight, maxweight):
        for edbo in self.EdgeDBO.filter(weight__gte=minweight,
                                         weight__lte=maxweight):
            weight = edbo.weight
            haps_id = [
                v for k, v in edbo.get_field_dict().items()
                if k.startswith("haplotype_") and v is not None
            ]
            yield dom.Edge(weight, *haps_id)

    def hap_sql(self, query, *args):
        haps = []
        for hdbo in self.HaplotypeDBO.raw(query, *args):
            hap = dom.Haplotype(**hdbo.get_field_dict())
            haps.append(hap)
        return tuple(haps)

    def save_version(self, tag, comment="", hap_sql="",
                     topology={}, weight_range=(None, None), ambients=()):
        td = {}
        for hap, xy in topology.items():

            # validate if this hap is in this network
            self.HaplotypeDBO.get(hap_id=hap.hap_id)
            td[hap.hap_id] = list(xy)

        minw, maxw = weight_range
        if minw > maxw:
            raise ValueError("Invalid range: ({}, {})".format(minw, maxw))
        wrl = [minw, maxw]

        al = []
        for active, ambient in ambients:
            active = bool(active)
            for varname, varvalue in ambient.items():
                if varname not in self.facts_attributes_names():
                    msg = "Invalid fact attribute: '{}'".format(varname)
                    raise ValueError(msg)
                if (varvalue is not None
                    and varvalue not in self.get_fact_attribute_values(varname)):
                        msg = "Invalid value '{}' for fact attribute '{}'"
                        msg = msg.format(varvalue, varname)
                        raise ValueError(msg)
            al.append([active, ambient])

        data = {"topology": td, "weight_range": wrl, 
                "ambients": al, "hap_sql": hap_sql}
        
        vdbo = self.YatelVersionDBO()
        vdbo.tag = tag
        vdbo.datetime = datetime.datetime.now()
        vdbo.comment = comment
        vdbo.data = json.dumps(data).encode("base64")

        query = self.YatelVersionDBO.select()
        if query.count():
            vdbo_old = tuple(query.order_by(("datetime", "DESC")).limit(1))[0]
            if vdbo.data == vdbo_old.data:
                msg = "Nothing changed from the last version '{}'"
                msg = msg.format(vdbo.tag)
                raise ValueError(msg)
        vdbo.save()
        if self._versions is None:
            self.versions()
        else:
            self._versions.insert(0, (vdbo.id, vdbo.datetime, vdbo.tag))
        return vdbo.id, vdbo.datetime, vdbo.tag

    def versions(self):
        if self._versions is None:
            self._versions = []
            for vdbo in self.YatelVersionDBO.select().order_by(("id", "DESC")):
                ver = (vdbo.id, vdbo.datetime, vdbo.tag)
                self._versions.append(ver)
        return tuple(self._versions)

    def get_version(self, match=None):
        vdbo = None
        if match is None:
            query = self.YatelVersionDBO.select()
            vdbo = tuple(query.order_by(("datetime", "DESC")).limit(1))[0]
        elif isinstance(match, int):
            vdbo = self.YatelVersionDBO.get(id=match)
            data = vdbo.data
        elif isinstance(match, datetime.datetime):
            vdbo = self.YatelVersionDBO.get(datetime=match)
        elif isinstance(match, basestring):
            vdbo = self.YatelVersionDBO.get(tag=match)
        else:
            msg = "Match must be None, int, str, unicode or datetime instance"
            raise TypeError(msg)

        version = json.loads(vdbo.data.decode("base64"))

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
        return self._name

    @property
    def inited(self):
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
        peewee_field = peewee.DateTime
    if pk:
        kwargs.pop("null", None)
        return peewee.PrimaryKeyField(
            column_class=peewee_field.column_class, **kwargs
        )
    return peewee_field(**kwargs)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

