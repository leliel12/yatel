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

import numpy

import Network


################################################################################
# NODE CLASS
################################################################################

class NetworkInfo(object):

    def __init__(self, network):
        assert isinstance(network, Network.Network), \
               "network must be Network instance find: " % str(type(network))
        self._nw = network

    def __repr__(self):
        return "%s instance of %s at %s" % (self.__class__.__name__,
                                           repr(self._nw),
                                           hex(id(self)))
    @property
    def network(self):
        return self._nw                                       
    
    @property
    def distances(self):
        all_d = []
        for srd_dict in self._nw.values():
            distances = [d for d in srd_dict.values() if isinstance(d, (float, int))]
            all_d.extend(distances)
        return all_d
                    
    @property
    def distance_avg(self):
        return numpy.average(self.distances)
    
    @property
    def distance_std(self):
        return numpy.std(self.distances)
        
    @property
    def distance_max(self):
        return max(self.distances)
    
    @property
    def distance_min(self):
        return min(self.distances)
    
    @property
    def distance_frequency(self):
        """Return a list of tuples where all elements have"""
        freq = {}
        for d in self.distances:
            if d not in freq:
                freq[d] = 0
            freq[d] += 1
        return freq
    
    @property
    def distance_mode(self):
        freq = self.distance_frequency
        mode = max(freq.values())
        return tuple([d for d, count in freq.items() if count >= mode])
        
    @property
    def distance_anti_mode(self):
        freq = self.distance_frequency
        mode = min(freq.values())
        return tuple([d for d, count in freq.items() if count <= mode])
        

################################################################################
# MAIN
################################################################################

if __name__ == "__main__":
    print __doc__

