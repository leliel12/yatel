#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.


#===============================================================================
# FUTURE
#===============================================================================

from __future__ import absolute_import


#===============================================================================
# DOCS
#===============================================================================

"""
"""
#===============================================================================
# META
#===============================================================================

__version__ = "0.1"
__license__ = "GPL3"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2011-06-11"


#===============================================================================
# IMPORTS
#===============================================================================

import inspect, datetime

import elixir

from yatel import util

TYPE_PARSER = util.StringParser(
    int=(unicode, int),
    float=(unicode, float),
    bool=(unicode, lambda v: v == "True"),
    str=(unicode, str),
    unicode=(unicode, unicode),
    datetime=(unicode,
              lambda s: datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f"))
)

#===============================================================================
# FUNCTIONS
#===============================================================================

def create(session, metadata):

    class NetworkDescriptorEntity(elixir.Entity):
        
        nwid = elixir.Field(elixir.UnicodeText(), unique=True)
        annotations = elixir.OneToMany("AnnotationEntity")
        edges = elixir.OneToMany("EdgeEntity")
        haplotypes = elixir.ManyToMany("HaplotypeEntity",
                                       tablename="networks_descriptors_X_haplotypes")
        
        elixir.using_options(metadata=metadata,
                             session=session,
                             tablename="network_descriptors")


    class AnnotationEntity(elixir.Entity):
        
        name = elixir.Field(elixir.UnicodeText())
        _type = elixir.Field(elixir.UnicodeText(), colname="type")
        _value = elixir.Field(elixir.UnicodeText(), colname="value")
        network_descriptor = elixir.ManyToOne("NetworkDescriptorEntity")
        
        @property
        def value(self):
            return TYPE_PARSER.loads(self.type, self._value) if self._value else None
        
        @value.setter
        def value(self, v):
            self._value, self.type = TYPE_PARSER.dumps(v)
            
        @property
        def type(self):
            return self._type
        
        elixir.using_options(metadata=metadata,
                             session=session,
                             tablename="annotations")


    class HaplotypeEntity(elixir.Entity):
        
        name = elixir.Field(elixir.UnicodeText(), unique=True)
        attributes = elixir.OneToMany("HaplotypeAttributeEntity")
        networks_descriptors = elixir.ManyToMany("NetworkDescriptorEntity",
                                                 tablename="networks_descriptors_X_haplotypes")
        edges = elixir.ManyToMany("EdgeEntity",
                                  tablename="edges_X_haplotypes")
        facts = elixir.ManyToMany("FactEntity",
                                  tablename="facts_X_haplotypes")
        
        elixir.using_options(metadata=metadata,
                             session=session,
                             tablename="haplotypes")


    class HaplotypeAttributeEntity(elixir.Entity):
        
        name = elixir.Field(elixir.UnicodeText())
        _type = elixir.Field(elixir.UnicodeText(), colname="type")
        _value = elixir.Field(elixir.UnicodeText(), colname="value")
        
        haplotype = elixir.ManyToOne("HaplotypeEntity")
        
        @property
        def value(self):
            return TYPE_PARSER.loads(self.type, self._value) if self._value else None
        
        @value.setter
        def value(self, v):
            self._value, self.type = TYPE_PARSER.dumps(v)
            
        @property
        def type(self):
            return self._type
        
        elixir.using_options(metadata=metadata,
                             session=session,
                             tablename="haplotypes_attributes")
    
    
    class EdgeEntity(elixir.Entity):
        
        weigth = elixir.Field(elixir.Float())
        network_descriptor = elixir.ManyToOne("NetworkDescriptorEntity")
        haplotypes = elixir.ManyToMany("HaplotypeEntity",
                                       tablename="edges_X_haplotypes")
        
        elixir.using_options(metadata=metadata,
                             session=session,
                             tablename="edges")


    class FactEntity(elixir.Entity):
            
        name = elixir.Field(elixir.UnicodeText(), unique=True)
        attributes = elixir.OneToMany("FactAttributeEntity")
        haplotypes = elixir.ManyToMany("HaplotypeEntity",
                                       tablename="facts_X_haplotypes")
            
        elixir.using_options(metadata=metadata,
                             session=session,
                             tablename="facts")
    
    
    class FactAttributeEntity(elixir.Entity):
        
        name = elixir.Field(elixir.UnicodeText())
        _type = elixir.Field(elixir.UnicodeText(), colname="type")
        _value = elixir.Field(elixir.UnicodeText(), colname="value")
        
        fact = elixir.ManyToOne("FactEntity")
        
        @property
        def value(self):
            return TYPE_PARSER.loads(self.type, self._value) if self._value else None
        
        @value.setter
        def value(self, v):
            self._value, self.type = TYPE_PARSER.dumps(v)
        
        @property
        def type(self):
            return self._type
        
        elixir.using_options(metadata=metadata,
                             session=session,
                             tablename="facts_attributes")

    #===========================================================================
    # END ENTITIES
    #===========================================================================
    
    entities = {}
    for k, v in locals().items():
            if inspect.isclass(v) and issubclass(v, elixir.Entity):
                entities[k] = v
    return entities


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
