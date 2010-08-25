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
__date__ = "2010-08-04"


################################################################################
# IMPORTS
################################################################################

from Bio import SeqRecord
from Bio import Seq
from Bio import Alphabet

import Distance

################################################################################
# NETWORK CLASS
################################################################################

class Network(object):

    def __init__(self, alphabet, distance):
        assert isinstance(alphabet, Alphabet.Alphabet), \
               "alphabet must be Alphabet Instance"
        assert isinstance(distance, Distance.Distance) or distance == None, \
               "distance must be Distance instance or None"
        self._mtx = {}
        self._descs = {}
        self._distance = distance
        self._alphabet = alphabet
        
    def __repr__(self):
        return  "%s instance (%s records, %s) at %s" % (self.__class__.__name__,
                                                        len(self._mtx),
                                                        repr(self._alphabet),
                                                        hex(id(self)))
    
    def __getitem__(self, descriptor):
        r = self._descs[descriptor]
        return self._mtx[r]
        
    def __len__(self):
        return len(self._mtx)

    def __str__(self):
        return repr(self)
        
    def __iter__(self):
        for  r, distances in self._mtx.items():
            yield (r, distances.items())

    def new_network(self, new_distance,):
        new_network = Network(self._alphabet, new_distance)
        for r in self._mtx.keys():
                new_network.add_sequence(r.id, str(r.seq))
        return new_network

    def remove_sequence(self, descriptor):
        assert isinstance(descriptor, basestring), "descriptor must be str or unicode"
        r = self._descs[descriptor]
        self._mtx.pop(r)
        for v in self._mtx.values():
            v.pop(r)
        return self._descs.pop(r)
                

    def add_sequence(self, descriptor, str_seq):
        assert isinstance(str_seq, basestring), "str_seq must be str or unicode"
        assert isinstance(descriptor, basestring), "descriptor must be str or unicode"
        
        if descriptor not in self._descs:
            r0 = SeqRecord.SeqRecord(Seq.Seq(str_seq, self._alphabet),
                                    id=descriptor, description=descriptor)

            self._descs[descriptor] = r0
            
            self._mtx[r0] = {}
            
            for r1, distances in self._mtx.items():
                if r0 != r1:
                    d = self._distance.distance_of(r1, r0)
                    distances[r0] = abs(d) if d != None else d
                d = self._distance.distance_of(r0, r1)
                self._mtx[r0][r1] = abs(d) if d != None else d
    
    @property
    def distance(self):
        return self._distance

    @property
    def alphabet(self):
        return self._alphabet


################################################################################
# MAIN
################################################################################

if __name__ == "__main__":
    print __doc__

