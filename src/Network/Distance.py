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

__version__ = "0.1"
__license__ = "Biopython License"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2010-08-04"


################################################################################
# IMPORTS
################################################################################

import abc

from Bio import Seq


################################################################################
# BASE CLASS
################################################################################

class Distance(object):
    """Base class for all Distances classes
    
    You need to impelment distance_of(seq0, seq1) method.
    
    """
    
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod    
    def distance_of(self, seq_record0, seq_record1):
        """Returns the distances between seq_record0 and seq_record1"""
        raise NotImplementedError()


################################################################################
# DEFAULT DISTANCE CLASS
################################################################################

class DefaultDistance(Distance):
    
    def distance_of(self, seq_record0, seq_record1):
        d = abs(len(seq_record0) - len(seq_record1))
        for e0, e1 in zip(seq_record0, seq_record1):
            if e0 != e1:
                d += 1
        return d


################################################################################
# EXPERT DISTANCE CLASS
################################################################################

class ExpertDistance(Distance):
    
    def __init__(self):
        self._distances = {}
    
    def set_distance(self, str_seq0, str_seq1, distance):
        assert isinstance(str_seq0, basestring), "str_seq0 must be str or unicode"
        assert isinstance(str_seq1, basestring), "str_seq1 must be str or unicode"
        assert isinstance(distance, (int, float)) or distance == None, \
              "distance must be int or float or None"
        key = (str_seq0, str_seq1)
        self._distances[key] = distance
    
    def distance_of(self, seq_record0, seq_record1):
        key = (str(seq_record0.seq), str(seq_record1.seq))
        return self._distances.get(key)
        

################################################################################
# MAIN
################################################################################

if __name__ == "__main__":
    print __doc__

