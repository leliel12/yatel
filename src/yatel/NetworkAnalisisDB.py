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

from elixir import *

import Network


################################################################################
# ANALISIS DB
################################################################################

class Haplotype(Entity):
    id = Field(Unicode(1024), primary_key=True)
    attributes = OneToMany("HaplotypeAtt")
    facts = OneToMany("Fact")


class HaplotypeAtt(Entity):
    value = Field(UnicodeText())
    haplotype = ManyToOne("Haplotype")


class Fact(Entity):
    haplotype = ManyToOne("Haplotype")
    attributes = OneToMany("FactAtt")


class FactAtt(Entity):
    name = Field(UnicodeText())
    value = Field(UnicodeText())
    fact = ManyToOne("Fact")


class Distance(Entity):
    hfrom = ManyToOne("Haplotype")
    hto = ManyToOne("Haplotype")
    value = Field(Float)
    
#===============================================================================
# FUNCTIONS
#===============================================================================

def connect(connection, create=False):
    pass

################################################################################
# MAIN
################################################################################

if __name__ == "__main__":
    print __doc__

