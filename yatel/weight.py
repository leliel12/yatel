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

"""This module is used for calculate weights of edgest in yatel

"""

#===============================================================================
# IMPORTS
#===============================================================================

import numpy


#===============================================================================
# ERROR
#===============================================================================

class AbstractWeight(object):
    """"""
    
    def __call__(self, hap0, hap1):
        return self.weight(hap0, hap1)
    
    def weight(self, hap0, hap1):
        """"""
        raise NotImplementedError()
        

#===============================================================================
# HAMMING
#===============================================================================


class Hamming(AbstractWeight):
    
    def weight(self, hap0, hap1):
        w = 0
        for name in set(hap0.names_attrs() + hap1.names_attrs()):
            if name not in h0.names_attrs() \
               or name not in h1.names_attrs() \
               or h0.get_attr(name) != h1.get_attr(name):
                w += 1
        return w
        
            

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
        for name in set(hap0.names_attrs() +  hap1.names_attrs()):
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
                a,b = b,a
                n,m = m,n
            current = range(n+1)
            for i in range(1,m+1):
                previous, current = current, [i]+[0]*n
                for j in range(1,n+1):
                    add, delete = previous[j]+1, current[j-1]+1
                    change = previous[j-1]
                    if a[j-1] != b[i-1]:
                        change = change + 1
                    current[j] = min(add, delete, change)
            return float(current[n])
        
        # aas = attributes as string
        aas0 = []
        aas1= []
        for name in sorted(set(hap0.names_attrs() +  hap1.names_attrs())):
            as0 = str(hap0.get_attr(name, "")).encode("base64")
            as1 = str(hap1.get_attr(name, "")).encode("base64")
            aas0.append(as0)
            aas1.append(as1)
        return levenshtein("".join(aas0), "".join(aas1))

        
#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    import dom

    h0 = dom.Haplotype("h0", a0="0a", a1="156", a2="lalal")
    h1 = dom.Haplotype("h1", a0="15", a1="1h")
    h2 = dom.Haplotype("h1", a0=1, a1="1h")

    hamming = Levenshtein()
    print hamming.weight(h2, h1)

    print __doc__




