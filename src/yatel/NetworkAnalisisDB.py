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



################################################################################
# DOCS
################################################################################

"""


"""


################################################################################
# META
################################################################################

__version__ = "Biopython License"
__license__ = "GPL3"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2010-09-14"


################################################################################
# IMPORTS
################################################################################

import elixir
import string

import Network

#===============================================================================
# DB CONNECT CLASS
#===============================================================================

class DBTemplate(object):
    
    def __init__(self, template, default_host, default_port):
        self.template = string.Template(template)
        self.default_host = default_host
        self.default_port = default_port

    def substitute(self, db_name, user=None, password=None, host=None, port=None):
        user = user if user else ""
        password = password if password else ""
        host = host if host else self.default_host
        port = port if port else self.default_port
        return self.template.substitute(db_name=db_name, 
                                        user=user, password=password,
                                        host=host, port=port)


################################################################################
# 
################################################################################

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

 
_DBS = {
    "memory": DBTemplate("sqlite:///:memory:", "", ""),
    "sqlite": DBTemplate("sqlite:///${db_name}", "", "")
}
 
 
def valid_connections():
    return _DBS.keys()
 
    
def connect(db, db_name, 
            user="", password="", host=None, port="", 
            create=False, echo=False):
    elixir.metadata.bind = _DBS[db].substitute(db_name, user, password, host, port)
    elixir.setup_all(create)
    elixir.metadata.bind.echo = echo
    

def commit():
    elixir.session.commit()


def rollback():
    elixir.session.rollback()
    
    
def execute(query):
    return elixir.session.execute(query)


def close():
    elixir.session.close()



    

################################################################################
# MAIN
################################################################################

if __name__ == "__main__":
    print __doc__

