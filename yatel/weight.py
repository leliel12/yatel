#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dom.py
     
# Copyright 2011 Juan BC <jbc dot develop at gmail dot com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.


#===============================================================================
# DOCS
#===============================================================================

"""This module is used for calculate weights of edges in yatel.

Esentially contains some of knowed algorithms for calculate distances betwwen 
elements that can be used as edge weights.

"""

#===============================================================================
# IMPORTS
#===============================================================================

import itertools 

import numpy


#===============================================================================
# ERROR
#===============================================================================

class AbstractWeight(object):
    """
    """
    
    def __call__(self, haps=[], repeated=False):
        return self.weights(haps=haps, repeated=repeated)
        
    def weights(self, haps=[], repeated=False):
        ws = {}
        comb = itertools.combinations_with_replacement \
               if repeated else itertools.combinations
        for hap0, hap1 in comb(haps, 2):
            ws[(hap0, hap1)] = self.weight(hap0, hap1)
        return ws
    
    def weight(self, hap0, hap1):
        """"""
        raise NotImplementedError()
        

#===============================================================================
# HAMMING
#===============================================================================

class Hamming(AbstractWeight):
    """Calculate the hamming distances between two haplotypes, by counting
    the number of diferences in attributes.
    
    The distances is incremented by "1" by two reasons:
        #. haplotype0.attr_a != haplotype1.attr_a
        #. attr_a exist in haplotype0 but not exist in haplotype1.
        
    example::
        >>> from yatel import dom, weigth
        >>> haplotype0 = dom.Haplotype("0", attr_a="a", attr_b="b", attr_c=0)
        >>> haplotype1 = dom.Haplotype("1", attr_a="a", attr_c="0")
        >>> hamming = weight.Hamming()
        >>> print  hamming(haplotype0, haplotype1)
        {(<haplotype0>, <haplotype1>): 2.0}
        
    
    """
    
    def weight(self, hap0, hap1):
        w = 0
        for name in set(hap0.names_attrs() + hap1.names_attrs()):
            if name not in h0.names_attrs() \
               or name not in h1.names_attrs() \
               or h0.get_attr(name) != h1.get_attr(name):
                w += 1
        return w
  
        
#===============================================================================
# EXPERT
#===============================================================================

def Expert(AbstractWeight):
    
    def __init__(self, *weights):
        self._ws = {}
        for h0, h1, w in weights:
            self._ws[(h0, h1)] = w


    def weight(self, hap0, hap1):
        return self._ws.get((hap0, hap1))


#===============================================================================
# EUCLIDEAN
#===============================================================================

class Euclidean(AbstractWeight):
    
    def weight(self, hap0, hap1):
        
        def to_num(attr):
            value = 0
            for c in str(attr).encode("base64"):
                value += ord(c)
            return value
        
        s = 0.0
        for name in set(hap0.names_attrs() + hap1.names_attrs()):
            v0 = to_num(hap0.get_attr(name, ""))
            v1 = to_num(hap1.get_attr(name, ""))
            s += (v1 - v0) ** 2
        return numpy.sqrt(s)
        

#===============================================================================
# LEVENSHTEIN
#===============================================================================

class Levenshtein(AbstractWeight):
    
    def weight(self, hap0, hap1):
    
        def levenshtein(a, b):
            """Calculates the Levenshtein distance between a and b.
            
            Found at: http://hetland.org/coding/
            """
            n, m = len(a), len(b)
            if n > m:
                # Make sure n <= m, to use O(min(n,m)) space
                a, b = b, a
                n, m = m, n
            current = range(n + 1)
            for i in range(1, m + 1):
                previous, current = current, [i] + [0] * n
                for j in range(1, n + 1):
                    add, delete = previous[j] + 1, current[j - 1] + 1
                    change = previous[j - 1]
                    if a[j - 1] != b[i - 1]:
                        change = change + 1
                    current[j] = min(add, delete, change)
            return current[n]

        values = []
        for name in sorted(set(hap0.names_attrs() + hap1.names_attrs())):
            as0 = str(hap0.get_attr(name, "")).encode("base64")
            as1 = str(hap1.get_attr(name, "")).encode("base64")
            values.append(levenshtein(as0, as1))
        return sum(values)


#===============================================================================
# DAMERAU-LEVENSHTEIN
#===============================================================================

class DamerauLevenshtein(AbstractWeight):
    """Calculate the Damerau-Levenshtein distance between haplotypes.
    
    This distance is the number of additions, deletions, substitutions,
    and transpositions needed to transform the first haplotypes as sequences
    sequence into the  second. .

    Transpositions are exchanges of *consecutive* characters; all other
    operations are self-explanatory.

    This implementation is O(N*M) time and O(M) space, for N and M the
    lengths of the two sequences.

    """
    
    def weight(self, hap0, hap1):
        
        def dameraulevenshtein(seq1, seq2):
            """This is the original code found in: 
            
            http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance/
            
            The code is available under the MIT licence, in the hope that it
            will be useful, but without warranty of any kind. I have also 
            included a codesnippet  GUID in line with the linked post, as a sort 
            of experiment. Please leave that comment intact if you’re 
            posting a derivative somewhere, and add your own.
            
            """
            # codesnippet:D0DE4716-B6E6-4161-9219-2903BF8F547F
            # Conceptually, this is based on a len(seq1) + 1 * len(seq2) + 1 matrix.
            # However, only the current and two previous rows are needed at once,
            # so we only store those.
            oneago = None
            thisrow = range(1, len(seq2) + 1) + [0]
            for x in xrange(len(seq1)):
                # Python lists wrap around for negative indices, so put the
                # leftmost column at the *end* of the list. This matches with
                # the zero-indexed strings and saves extra calculation.
                twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
                for y in xrange(len(seq2)):
                    delcost = oneago[y] + 1
                    addcost = thisrow[y - 1] + 1
                    subcost = oneago[y - 1] + (seq1[x] != seq2[y])
                    thisrow[y] = min(delcost, addcost, subcost)
                    # This block deals with transpositions
                    if (x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                        and seq1[x - 1] == seq2[y] and seq1[x] != seq2[y]):
                        thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)
            return thisrow[len(seq2) - 1]
        
        values = []
        for name in sorted(set(hap0.names_attrs() + hap1.names_attrs())):
            as0 = str(hap0.get_attr(name, "")).encode("base64")
            as1 = str(hap1.get_attr(name, "")).encode("base64")
            values.append(dameraulevenshtein(as0, as1))
        return sum(values)



#===============================================================================
# SOMME
#===============================================================================

class McCarthy(AbstractWeight):
    
    def __init__(self, hamming_attrs, migrated_attrs,
                 broken2_attrs, broken1_attrs, to_bool=bool):
        assert hasattr(hamming_attrs, "__iter__")
        assert hasattr(migrated_attrs, "__iter__")
        assert hasattr(broken2_attrs, "__iter__")
        assert hasattr(broken1_attrs, "__iter__")
        assert callable(to_bool)
        self._hams = tuple(hamming_attrs)
        self._mig = tuple(migrated_attrs)
        self._br2 = tuple(broken2_attrs)
        self._br1 = tuple(broken1_attrs)
        self._to_bool = to_bool
    
    def booleanify(self, hap):
        """Convert all attributes of a given haplotype to a
        dict with all values converted in bool by to_bool
        function
        
            >>> from yatel import dom, weight
            >>> hap = dom.Haplotype("hap", a=1, b=2, c=10)
            >>> to_bool = lambda att: att > 5
            >>> mc = wight.McArty([], [], [], [], to_bool)
            >> mc.booleanify(hap)
            {'a': False, 'b': False, 'c': True}
            
        """
        assert isinstance(hap, dom.Haplotype)
        hab = {}
        for k, v in hap.items_attrs():
            hab[k] = bool(self._to_bool(v))
        return hab
            
    def _weight(self, hap0, hap1):
        h0attrs = self.booleanify(hap0)
        h1attrs = self.booleanify(hap1)
        
    @property
    def hamming_attrs(self):
        return self._hams
        
    @property
    def migrated_attrs(self):
        return self._mig
    
    @property
    def broken2_attrs(self):
        return self._br2
        
    @property
    def broken1_attrs(self):
        return self._br1
    
    @property
    def to_bool(self):
        return self._to_bool


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    import dom

    h0 = dom.Haplotype(
        "9",
        B3a=1, B3b=0, B9a=0, B9b=0, B9c=1, B10a=1,
        B10b=0, BE10=0, B5=1, BE5=0, B8=1
    )
    h1 = dom.Haplotype(
        "13",
        B3a=0, B3b=1, B9a=0, B9b=0, B9c=1, B10a=1,
        B10b=0, BE10=1, B5=1, BE5=1, B8=1
    )
    print Levenshtein()([h0, h1])
    """
    d0 = lambda h0, h1: abs(h0.B5 - h1.B5)
   
    d1 = lambda h0, h1: abs(h0.B8 - h1.B8)
   
    d2 = lambda h0, h1: (
        abs(h0.B3a - h1.B3a) + abs(h0.B3b - h1.B3b) +
        abs(h0.B3a - h1.B3a + h0.B3b - h1.B3b)
    ) / 2
                          
    d3 = lambda h0, h1: (
        abs(h0.B9a - h1.B9a) + abs(h0.B9b - h1.B9b) + abs(h0.B9c - h1.B9c) +
        abs( h0.B9a - h1.B9a + h0.B9b - h1.B9b + h0.B9c - h1.B9c)
    ) / 2
    
    d4 = lambda h0, h1: (
        abs(h0.B10a - h1.B10a) + abs(h0.B10b - h1.B10b) +
        abs(h0.B10a - h1.B10a + h0.B10b - h1.B10b)
    ) / 2
    
    d5 = lambda h0, h1: (
        abs(h0.BE10 - h1.BE10) * (
            1 - (1 if abs(h0.B3a - h1.B3a) or abs(h0.B3a - h1.B3a) else 0)
        )
    )
    
    d6 = lambda h0, h1: (
        abs(h0.BE5 - h1.BE5) * (1 - abs(h0.B5 - h1.B5))
    )"""
                           
    




