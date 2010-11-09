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

import elixir
import string

from yatel import Network

#===============================================================================
# CONSTANTS
#===============================================================================

_DBS = {
    "memory": string.Template("sqlite:///:memory:"),
    "sqlite": string.Template("sqlite:///$db_name"),
    "mysql": string.Template("mysql://$user:$password@$host/$db_name")
}


#===============================================================================
# 
#===============================================================================

class Haplotype(elixir.Entity):
    
    id = elixir.Field(elixir.Unicode(1024), primary_key=True)
    attributes = elixir.OneToMany("HaplotypeAtt")
    facts = elixir.OneToMany("Fact")
    
    elixir.using_options(tablename="haplotypes") 


#===============================================================================
# 
#===============================================================================

class HaplotypeAtt(elixir.Entity):
    
    value = elixir.Field(elixir.UnicodeText())
    haplotype = elixir.ManyToOne("Haplotype")
    
    elixir.using_options(tablename="haplotypes_attributes")
    
    
#===============================================================================
# 
#===============================================================================

class Fact(elixir.Entity):
    
    haplotype = elixir.ManyToOne("Haplotype")
    attributes = elixir.OneToMany("FactAtt")
    
    elixir.using_options(tablename="facts")


#===============================================================================
# 
#===============================================================================

class FactAtt(elixir.Entity):
    
    name = elixir.Field(elixir.UnicodeText())
    value = elixir.Field(elixir.UnicodeText())
    fact = elixir.ManyToOne("Fact")
    
    elixir.using_options(tablename="fact_attributes")


#===============================================================================
# 
#===============================================================================

class Distance(elixir.Entity):
    
    hfrom = elixir.ManyToOne("Haplotype")
    hto = elixir.ManyToOne("Haplotype")
    value = elixir.Field(elixir.Float)
    
    elixir.using_options(tablename="distances")
    
    
#===============================================================================
# FUNCTIONS
#=============================================================================== 
 
def valid_connections():
    return _DBS.keys()
 
    
def connect(db, db_name="", 
            user="", password="", host=None, port="", 
            create=False, echo=False):
    elixir.metadata.bind = _DBS[db].substitute(db_name=db_name, 
                                               user=user, password=password, 
                                               host=host, port=port)
    elixir.setup_all(create)
    elixir.metadata.bind.echo = echo
    

def commit():
    elixir.session.commit()


def rollback():
    elixir.session.rollback()
    
    
def execute(query, *args, **kwargs):
    return elixir.session.execute(query, *args, **kwargs)


def close():
    elixir.session.close()


def write(networks):
     for nw in networks:
         print nw
    
    
    

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

