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
__date__ = "2010-09-14"


#===============================================================================
# IMPORTS
#===============================================================================

import string
import datetime

import elixir

from yatel import util

#===============================================================================
# CONSTANTS
#===============================================================================

TYPE_PARSER = util.StringParser(
    int=(unicode, int),
    float=(unicode, float),
    bool=(unicode, lambda v: v == "True"),
    str=(unicode, str),
    unicode=(unicode, unicode),
    datetime=(unicode, 
              lambda s: datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f"))
)

DB_SCHEMAS = {
    "memory": string.Template("sqlite:///:memory:"),
    "sqlite": string.Template("sqlite:///$path"),
    "mysql": string.Template("mysql://$user:$password@$host:$port/$name")
}

SCHEMA_DOC = "34344343"
#===============================================================================
# NETWORK
#===============================================================================

class Network(elixir.Entity):
    
    name = elixir.Field(elixir.UnicodeText)
    
"""
#===============================================================================
# NETWORK DETAILS
#===============================================================================

class NetworkDetail(elixir.Entity):
    
    distance_value = elixir.Field(elixir.Float)
    
    network = elixir.ManyToOne("Network")
    seq_0 = elixir.ManyToOne("Sequence")
    seq_1 = elixir.ManyToOne("Sequence")


#===============================================================================
# DISTANCE
#===============================================================================

class Distance(elixir.Entity):
    
    name = elixir.Field(elixir.UnicodeText)
    description = elixir.Field(elixir.UnicodeText)
    
    details = elixir.OneToMany("DistanceDetail")

    
#===============================================================================
# DISTANCE DETAIL
#===============================================================================

class DistanceDetail(elixir.Entity):
    
    distance_value = elixir.Field(elixir.Float)
    
    seq_0 = elixir.ManyToOne("Sequence")
    seq_1 = elixir.ManyToOne("Sequence")
    metric = elixir.ManyToOne("Metric")
    distance = elixir.ManyToOne("Distance", inverse="details")


#===============================================================================
# METRIC
#===============================================================================

class Metric(elixir.Entity):
    
    name = elixir.Field(elixir.UnicodeText)
    description = elixir.Field(elixir.UnicodeText)
    
    distance_details = elixir.OneToMany("DistanceDetail")


#===============================================================================
# SEQUENCES
#===============================================================================

class Sequence(elixir.Entity):
    
    name = elixir.Field(elixir.UnicodeText)
    description = elixir.Field(elixir.UnicodeText)
    
    attributes = elixir.OneToMany("SequenceAttribute")
    distance_details = elixir.OneToMany("DistanceDetail")
    network_details = elixir.OneToMany("NetworkDetail")
    

#===============================================================================
# SEQUENCE ATTRIBUTES
#===============================================================================

class SequenceAttribute(elixir.Entity):                                            
                                            
    _value = elixir.Field(elixir.UnicodeText, colname="value")
    att_type = elixir.Field(elixir.Enum(FORMATTER.valid_types))
    
    seq = elixir.ManyToOne("Sequence")
    
    @property
    def value(self):
        return FORMATTER.parse(self.att_type, self._value)
    
    @property    
    def value(self, v):
        self.att_type, self._value = FORMATTER.format(v)
    

#===============================================================================
# FACT
#===============================================================================
    
class Fact(elixir.Entity):
    
    name = elixir.Field(elixir.UnicodeText)
    description = elixir.Field(elixir.UnicodeText)
    
    seq = elixir.ManyToOne("Sequence")
    attributes = elixir.OneToMany("FactAttribute")


#===============================================================================
# FACT ATTS
#===============================================================================

class FactAttribute(elixir.Entity):                                            
                                            
    _value = elixir.Field(elixir.UnicodeText, colname="value")
    att_type = elixir.Field(elixir.Enum(FORMATTER.valid_types))
    
    seq = elixir.ManyToOne("Sequence")
    
    @property
    def value(self):
        return FORMATTER.parse(self.att_type, self._value)
    
    @property    
    def value(self, v):
        self.att_type, self._value = FORMATTER.format(v)

"""

#===============================================================================
# CONNECTION
#===============================================================================

class Connection(object):
    
    def __init__(schema, reate=False, echo=False, **kwargs):
        __doc__ = SCHEMA_DOC
        self._conn_str = DBS[schema].substitute(name=name,
                                                user=user, password=password,
                                                host=host, port=port)




#===============================================================================
# FUNCTIONS
#===============================================================================
"""
def connect:
    elixir.metadata.bind = 
    elixir.setup_all(create)
    elixir.metadata.bind.echo = echo

connect("memory", create=True, echo=True)
"""
#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

