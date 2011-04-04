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

import numpy

from yatel import network


#===============================================================================
# NODE CLASS
#===============================================================================

class NetworkInfo(object):
    """This class is used for extract information about networks
    
    """

    def __init__(self, nw):
        """Create a new instance
        
        @param nw: a ntwork toextract information
        
        """
        assert isinstance(nw, network.Network), \
               "'nw' must be Network instance found: %s" % str(type(nw))
        self._nw = nw

    def __repr__(self):
        return "%s instance of %s at %s" % (self.__class__.__name__,
                                             repr(self._nw),
                                             hex(id(self)))                                 
    
    def distances(self, ignore_none=True):
        """Return a list of all distances of the network
        
        @param ignore_none: if is True do not return the "None" values
         
        """
        all_d = []
        for h0 in self._nw:
            for h1 in self._nw:
                d = self._nw.distance(h0, h1)
                if not ignore_none or d != None :
                    all_d.append(d)
        return all_d
                    
    def distance_avg(self, *args, **kwargs):
        """Calculate the distance average of all network
        
        @param *args: the numpy average extra arguments.
        @param **kwargs: the numpy average extra arguments.
        
        """
        return numpy.average(self.distances(), *args, **kwargs)
    
    def distance_std(self, *args, **kwargs):
        """Compute the standard deviation of network distances 
        along the specified axis.
        
        @param *args: the numpy std extra arguments.
        @param **kwargs: the numpy std extra arguments.
         
         """
        return numpy.std(self.distances(), *args, **kwargs)
        
    def distance_max(self, *args, **kwargs):
        """Return the maximum distance of the network along an axis.
        
        @param *args: the numpy max extra arguments.
        @param **kwargs: the numpy max extra arguments.
         
         """
        return numpy.max(self.distances(), *args, **kwargs)

    def distance_min(self, *args, **kwargs):
        """Return the minimum distance of the network along an axis.
        
        @param *args: the numpy min extra arguments.
        @param **kwargs: the numpy min extra arguments.
         
         """
        return min(self.distances(), *args, **kwargs)

    def distance_frequency(self):
        """Return a dictionary where the keys are the distances, and a value
        are the frequency of the distance"""
        freq = {}
        for d in self.distances():
            if d not in freq:
                freq[d] = 0
            freq[d] += 1
        return freq
    
    def distance_mode(self, *args, **kwargs):
        """Return a tuple of the distances with max frequencies
        
        @param *args: the numpy max extra arguments.
        @param **kwargs: the numpy max extra arguments.
        
        """
        freq = self.distance_frequency()
        mode = numpy.max(freq.values(), *args, **kwargs)
        return tuple(d for d, count in freq.items() if count >= mode)
        
        
    def distance_anti_mode(self, *args, **kwargs):
        """Return a tuple of the distances with min frequencies
        
        @param *args: the numpy min extra arguments.
        @param **kwargs: the numpy min extra arguments.
        
        """
        freq = self.distance_frequency()
        mode = numpy.min(freq.values(), *args, **kwargs)
        return tuple([d for d, count in freq.items() if count <= mode])
        
    @property
    def network(self):
        return self._nw      

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

