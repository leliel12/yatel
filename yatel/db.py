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
            self._inited = False
            
            class Meta:
                database = self.database
            self.model_meta = Meta    
            
        except KeyError:
            msg = "'engine' must be any of {}, found '{}'"
            raise ValueError(msg.format(ENGINES.keys(), engine))
    
    def __getattr__(self, k):
        return getattr(self.database, k)
    
    def init_with_values(self, haps, facts, edges):
        
        if self._inited:
            msg = "Connection already inited"
            raise YatelConnectionError(msg)
            
        haps_columns = {"hap_id": []}
        for hap in haps:
            haps_columns["hap_id"].append(hap.hap_id)
            for an, av in hap.items_attrs():
                if an not in haps_columns:
                    haps_columns[an] = []
                haps_columns[an].append(av)
        hapdbo_dict = {"Meta": self.model_meta}
        for cn, values in haps_columns.items():
            hapdbo_dict[cn] = field(values, pk=(cn=="hap_id"), null=True)
        self.HaplotypeDBO = type("Haplotypes", (peewee.Model, ), hapdbo_dict)
        
        facts_columns = {}
        for fact in facts:
            for an, av in fact.items_attrs():
                if an not in facts_columns:
                    facts_columns[an] = []
                facts_columns[an].append(av)

        factsdbo_dict = {
            "Meta": self.model_meta, 
            "haplotype": peewee.ForeignKeyField(self.HaplotypeDBO, null=True)
        }
        for cn, values in facts_columns.items():
            factsdbo_dict[cn] = field(values, null=True)
        self.FactDBO = type("Facts", (peewee.Model, ), factsdbo_dict)
        
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
        for idx in range(max_number_of_haps):
            key = "haplotype_{}".format(idx)
            edgesdbo_dict[key] = peewee.ForeignKeyField(
                self.HaplotypeDBO, null=True
            )
        self.EdgeDBO = type("Edges", (peewee.Model,), edgesdbo_dict)
        
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
            
        self._inited = True
        
    def iter_haplotypes(self):
        for hdbo in self.HaplotypeDBO.select():
            yield dom.Haplotype(**hdbo.get_field_dict())
        
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
                elif v is not None:
                    data[k] = v
            return dom.Fact(db)
    
    def ambient(self, **kwargs):
        haps = {}
        for fdbo in self.FactDBO.filter(**kwargs):
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
        return tuple([
            getattr(fdbo, att_name)
            for fdbo in self.FactDBO.select()
            if getattr(fdbo, att_name, None)
        ])
        
    def hap_sql(self, query, *args):
        for hdbo in self.HaplotypeDBO.raw(query, *args):
            dom.Haplotype(**hdbo.get_field_dict())
            
    
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
            peewee_field =  peewee.TextField
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
    haps = [
        dom.Haplotype("hola", a=1, b="h1",z=23),
        dom.Haplotype("hola2", a=4, b="h4"),
        dom.Haplotype("hola3", b="h"),
        dom.Haplotype("hola4", a=4, ),
        dom.Haplotype("hola5", a=5, b="h3")
    ]

    facts = [
        dom.Fact("hola", b=1, c=2),
        dom.Fact("hola", j=1, k=2, c=3)
    ]

    edges = [
        dom.Edge(23, "hola", "hola2"),
        dom.Edge(22, "hola", "hola2", "hola5")

    ]

    conn = YatelConnection("sqlite", name="tito.db")
    conn.init_with_values(haps, facts, edges)
