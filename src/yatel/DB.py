#!/usr/bin/env python
#-*-coding:utf-8-*-

# Copyright (C) 2010 Juan BC <jbc dot develop at gmail dot com>

# Biopython License Agreement

# Permission to use, copy, modify, and distribute this software and its
# documentation with or without modifications and for any purpose and
# without fee is hereby granted, provided that any copyright notices
# appear in all copies and that both those copyright notices and this
# permission notice appear in supporting documentation, and that the
# names of the contributors or copyright holders not be used in
# advertising or publicity pertaining to distribution of the software
# without specific prior permission.

# THE CONTRIBUTORS AND COPYRIGHT HOLDERS OF THIS SOFTWARE DISCLAIM ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL THE
# CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY SPECIAL, INDIRECT
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
# OR PERFORMANCE OF THIS SOFTWARE.

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

__version__ = "Biopython License"
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

from Bio import Seq
from Bio import Alphabet
from Bio import SeqRecord

from yatel import Network
from yatel import Distance
from yatel import util


#===============================================================================
# CONSTANTS
#===============================================================================

FORMATTER = util.TypeFormatter(
    int=int,
    float=float,
    bool=bool, 
    str=str, 
    unicode=unicode,
    datetime=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
)

DBS = {
    "memory": string.Template("sqlite:///:memory:"),
    "sqlite": string.Template("sqlite:///$name"),
    "mysql": string.Template("mysql://$user:$password@$host:$port/$name")
}


#===============================================================================
# NETWORK
#===============================================================================

class Network(elixir.Entity):
    
    name = elixir.Field(elixir.UnicodeText)
    description = elixir.Field(elixir.UnicodeText)
    
    details = elixir.OneToMany("NetworkDetail")
    

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


#===============================================================================
# FUNCTIONS
#===============================================================================

def connect(db, name="", user="", password="",
             host="", port="", create=False, echo=False):
    elixir.metadata.bind = DBS[db].substitute(name=name,
                                              user=user, password=password,
                                              host=host, port=port)
    elixir.setup_all(create)
    elixir.metadata.bind.echo = echo

connect("memory", create=True, echo=True)
#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

