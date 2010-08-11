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

from Bio import Seq
from Bio import Alphabet

import Distance

################################################################################
# NODE CLASS
################################################################################

class NetworkHash(object):

    def __init__(self, descriptor, seq):
        assert isinstance(descriptor, basestring), \
               "descriptor must be str or unicode"
        assert isinstance(seq, Seq.Seq), "seq must be Seq instance"
        super(self.__class__, self).__init__()
        self._desc = descriptor
        self._seq = seq

    def __repr__(self):
        return "<%s instance (%s, %s) at %s>" % (self.__class__.__name__,
                                                 self._desc,
                                                 repr(self._seq),
                                                 hex(id(self)))

    def __hash__(self):
        return hash(self._desc)

    def __eq__(self, obj):
        return isinstance(obj, (self.__class__, basestring)) \
               and hash(self) == hash(obj)
               
    def __neq__(self, obj):
        return not self == obj

    def _get_seq(self):
        return self._seq

    seq = property(_get_seq)

    def _get_desc(self):
        return self._desc

    descriptor = property(_get_desc)


################################################################################
# NETWORK CLASS
################################################################################

class Network(object):

    def __init__(self, alphabet, distance=None):
        assert isinstance(alphabet, Alphabet.Alphabet), \
               "alphabet must be Alphabet Instance"
        assert isinstance(distance, Distance.Distance) or distance == None, \
               "distance must be Distance instance or None"
        self._mtx = {}
        self._distance = distance \
                         if distance != None \
                         else Distance.DefaultDistance()
        self._alphabet = alphabet

    def __repr__(self):
        return  "<%s instance (%s records, %s) at %s>" % (self.__class__.__name__,
                                                          len(self._mtx),
                                                          repr(self._alphabet),
                                                          hex(id(self)))
    
    def __getitem__(self, descriptor):
        return self._mtx[descriptor]
        
    def __len__(self):
        return len(self._mtx)

    def __str__(self):
        return repr(self)
        
    def __iter__(self):
        for  sh, distances in self._mtx.items():
            ds = [(nh.descriptor, nh.seq, d) for nh, d in distances.items()]
            yield (sh.descriptor, sh.seq, ds)

    def transform(self, new_distance):
        new_network = Network(self._alphabet, new_distance)
        for descriptor, seq, _ in self:
            new_network.add_sequence(descriptor, str(seq))
        return new_network

    def add_sequence(self, descriptor, seq):
        assert isinstance(seq, basestring), "seq0 must be str or unicode"
        if descriptor not in self._mtx:
            sh0 = NetworkHash(descriptor, Seq.Seq(seq, self._alphabet))
            self._mtx[sh0] = {}
            for sh1, distances in self._mtx.items():
                if sh0 != sh1:
                    distances[sh0] = self._distance.distance_of(sh1.seq, sh0.seq)
                self._mtx[sh0][sh1] = self._distance.distance_of(sh0.seq, sh1.seq)

    def _get_distance(self):
        return self._distance

    distance = property(_get_distance)

    def _get_alphabet(self):
        return self._alphabet

    alphabet = property(_get_alphabet)


################################################################################
# MAIN
################################################################################

if __name__ == "__main__":
    print __doc__

