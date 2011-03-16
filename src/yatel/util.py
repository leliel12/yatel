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
# DOCS
#===============================================================================

"""Various utilities for yatel."""


#===============================================================================
# META
#===============================================================================

__version__ = "Biopython License"
__license__ = "GPL3"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2011-02-17"


#===============================================================================
# CLASSES
#===============================================================================

class Cloneable(object):
    
    def clone(self):
        pass


class TypeFormatter(object):
    
    def __init__(self, **kwargs):
        self._types = dict((unicode(k), v) for k, v in kwargs.items())
        
    def parse(self, value_type, value):
        return self._types[value_type](value)
    
    def format(self, value):
        tn = unicode(type(value).__name__)
        if tn not in self._types:
            msg = u"'value' must be instance of %s. Found %s" % ( ", ".join(self._types), tn)
            raise TypeError(msg)
        return tn, unicode(value)
        
    @property
    def valid_types(self):
        return self._types.keys()
        
        
#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__
