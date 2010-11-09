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
__date__ = "2010-08-04"


#===============================================================================
# IMPORTS
#===============================================================================

from Bio import SeqRecord
from Bio import Seq
from Bio import Alphabet

from yatel import Distance


#===============================================================================
# BASE CLASS
#===============================================================================

class Network(object):

    def __init__(self, id, alphabet, distance,
                 name="", description="", annotations={}, sequences=[]):
        assert isinstance(id, basestring), \
               "id must be a str or unicode instance"        
        assert isinstance(alphabet, Alphabet.Alphabet), \
               "alphabet must be Alphabet Instance"
        assert isinstance(distance, Distance.Distance), \
               "distance must be Distance instance"
        assert isinstance(name, basestring), \
               "name must be a str or unicode instance"
        assert isinstance(description, basestring), \
               "description must be a str or unicode instance"
        self._mtx = {}
        self._id = id
        self._alphabet = alphabet
        self._distance = distance        
        self._name = name
        self._description = description
        self._annotations = {}
        for k, v in annotations.items():
            self.add_annotation(k, v)
        for s in sequences:
            self.add(s)

    def __repr__(self):
        return  "%s instance (%s records, %s) at %s" % (self.__class__.__name__,
                                                        len(self._mtx),
                                                        repr(self._alphabet),
                                                        hex(id(self)))

    def __getitem__(self, seq_record):
        return dict(self._mtx[seq_record])

    def __len__(self):
        return len(self._mtx)

    def __str__(self):
        return repr(self)

    def __iter__(self):
        return iter(self._mtx)

    def distance_of(self, seq_record0, seq_record1):
        assert seq_record0 in self._mtx, "seq_record0 not in this %s" % \
               self.__class__.__name__
        assert seq_record1 in self._mtx, "seq_record1 not in this %s" % \
               self.__class__.__name__
        return self._mtx[seq_record0].get(seq_record1, None)

    def keys(self):
        return self._mtx.iterkeys()

    def items(self):
        for k, v in self._mtx.iteritems():
            yield k, dict(v)

    def values(self):
        for d in self._mtx.itervalues():
            yield dict(d)

    def get(self, seq_record, default=None):
        v = self._mtx.get(seq_record, default)
        if isinstance(v, dict):
            v = dict(v)
        return v

    def add(self, r0):
        assert isinstance(r0, SeqRecord.SeqRecord), "r0 must be a SeqRecordInstance"
        self._mtx[r0] = {}
        for r1, distances in self._mtx.items():
            if r0 != r1:
                d = self._distance.distance_of(r1, r0)
                distances[r0] = abs(d) if d != None else d
            d = self._distance.distance_of(r0, r1)
            self._mtx[r0][r1] = abs(d) if d != None else d

    def pop(self, seq_record):
        pop = self._mtx.pop(seq_record)
        for v in self._mtx.values:
            v.pop(seq_record)
        return pop
    
    def add_annotaion(self, name, value):
        assert isinstance(name, basestring), \
               "name must be a unicode or str instance"
        assert isinstance(value, basestring), \
               "value must be a unicode or str instance"
        self._annotations[name] = value
        
    def del_annotation(self, name):
        return self._annotations.pop(name)

    @property
    def id(self):
        return self._id

    @property
    def distance(self):
        return self._distance

    @property
    def alphabet(self):
        return self._alphabet
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, n):
        assert isinstance(n, basestring), \
               "name must be a str or unicode instance"
        self._name = n
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, d):
        assert isinstance(d, basestring), \
               "description must be a unicode or str instance"
        self._description = d

    @property
    def annotations(self):
        return dict(self._annotations) 


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

