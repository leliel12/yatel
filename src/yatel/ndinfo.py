#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

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

__version__ = "0.1"
__license__ = "GPL3"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2010-08-04"


#===============================================================================
# IMPORTS
#===============================================================================

import numpy

from yatel import nd


#===============================================================================
# NODE CLASS
#===============================================================================


                          
def weights(nwd):
    """Return a list of all weights of the network
    
    @param ignore_none: if is True do not return the "None" values
     
    """
    assert isinstance(nwd, nd.NetworkDescriptor)
    return  [w for h0, h1, w in nwd.edges]

                    
def weights_avg(nwd, *args, **kwargs):
    """Calculate the weights average of all network
    
    @param *args: the numpy average extra arguments.
    @param **kwargs: the numpy average extra arguments.
    
    """
    ws = [w for w in weights(nwd) if w != None]
    return numpy.average(ws, *args, **kwargs)


def weights_std(nwd, *args, **kwargs):
    """Compute the standard deviation of network weights
    along the specified axis.
    
    @param *args: the numpy std extra arguments.
    @param **kwargs: the numpy std extra arguments.
     
     """
    ws = [w for w in weights(nwd) if w != None]
    return numpy.std(ws, *args, **kwargs)
        
        
def weights_max(nwd, *args, **kwargs):
    """Return the maximum weights of the network along an axis.
    
    @param *args: the numpy max extra arguments.
    @param **kwargs: the numpy max extra arguments.
     
     """
    ws = [w for w in weights(nwd) if w != None]
    return numpy.max(ws, *args, **kwargs)


def weights_min(nwd, *args, **kwargs):
    """Return the minimum weights of the network along an axis.
    
    @param *args: the numpy min extra arguments.
    @param **kwargs: the numpy min extra arguments.
     
     """
    ws = [w for w in weights(nwd) if w != None]
    return numpy.min(ws, *args, **kwargs)


def weights_frequency(nwd):
    """Return a dictionary where the keys are the weightss, and a value
    are the frequency of the weights"""
    freq = {}
    for w in weights(nwd):
        if w not in freq:
            freq[w] = 0
        freq[w] += 1
    return freq
   

def weights_mode(nwd, *args, **kwargs):
    """Return a tuple of the weightss with max frequencies
    
    @param *args: the numpy max extra arguments.
    @param **kwargs: the numpy max extra arguments.
    
    """
    freq = weights_frequency(nwd)
    mode = numpy.max(freq.values(), *args, **kwargs)
    return tuple(d for d, count in freq.items() if count == mode)
        
        
def weights_anti_mode(nwd, *args, **kwargs):
    """Return a tuple of the weightss with min frequencies
    
    @param *args: the numpy min extra arguments.
    @param **kwargs: the numpy min extra arguments.
    
    """
    freq = weights_frequency(nwd)
    mode = numpy.min(freq.values(), *args, **kwargs)
    return tuple([d for d, count in freq.items() if count == mode])


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

