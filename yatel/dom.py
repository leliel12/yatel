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
# ERROR
#===============================================================================

class ValidationError(BaseException):
    pass
    

#===============================================================================
# FACT
#===============================================================================

class Fact(object):
    
    def __init__(self, hap_id, **attrs):
        self._hap_id = hap_id
        self._attrs = attrs
                
    def __getattr__(self, n):
        try:
            return self._attrs[n]
        except KeyError:
            t = type(self).__name__
            msg = "'{t}' object has no attribute '{n}'".format(t=t, n=n)
            raise AttributeError(msg)
    
    def __getitem__(self, k):
        return self._attrs[k]
    
    @property
    def hap_id(self):
        return self._hap_id


#===============================================================================
# HAPLOTYPES
#===============================================================================

class Haplotype(object):
    
    def __init__(self, hap_id, **attrs):
        self._hap_id = hap_id
        self._attrs = attrs
    
    def __repr__(self):
        return "<{0} '{1}' at {2}>".format(
            self.__class__.__name__,
            self._hap_id, hex(id(self))
        )
    
    def __getattr__(self, n):
        try:
            return self._attrs[n]
        except KeyError:
            t = type(self).__name__
            msg = "'{t}' object has no attribute '{n}'".format(t=t, n=n)
            raise AttributeError(msg)
    
    def __getitem__(self, k):
        return self._attrs[k]
    
    def items_attrs(self):
        return self._attrs.items()
        
    def names_attrs(self):
        return self._attrs.keys()
        
    def values_attrs(self):
        return self._attrs.values()
    
    def get_attr(self, n, d=None):
        return self._attrs.get(n, d)
    
    @property
    def hap_id(self):
        return self._hap_id


#===============================================================================
# DISTANCES
#===============================================================================

class Edge(object):
    
    def __init__(self, weight, *haps_id):
        self._weight = float(weight)
        self._haps_id = haps_id
    
    @property    
    def weight(self):
        return self._weight
    
    @property
    def haps_id(self):
        return self._haps_id


#===============================================================================
# FUNCTIONS
#===============================================================================

def validate(haplotypes, facts, edges):
    
    haps_id = set()
    for hap in haplotypes:
        if hap.hap_id in haps_id:
            msg = "Duplicated hap_id '{id}'".format(id=hap.hap_id)
            raise ValidationError(msg)
        haps_id.add(hap.hap_id)
        
    for fact in facts:
        if fact.hap_id not in haps_id:
            msg = "Haplotype id '{id}'  of Fact '{fact}'not found on given haplotypes"
            raise ValidationError(msg.format(id=fact.hap_id, fact=repr(fact)))
            
    for edge in edges:
        for hap_id in edge.haps_id:
            if hap_id not in haps_id:
                msg = "Haplotype id '{id}'  of edge '{edge}'not found on given haplotypes"
                raise ValidationError(msg.format(id=edge.hap_id, edge=repr(edge)))
                
    
#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




