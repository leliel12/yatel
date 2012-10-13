#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Domain Object Model for Yatel.

"""


#===============================================================================
# ERROR
#===============================================================================

class ValidationError(BaseException):
    """Used in function ``dom.validate`` function.

    """
    pass


#===============================================================================
# FACT
#===============================================================================

class Fact(object):

    def __init__(self, hap_id, **attrs):
        self._hap_id = hap_id
        self._attrs = attrs

    def __eq__(self, obj):
        return obj is not None \
            and isinstance(obj, Fact) \
            and hash(self) == hash(obj)

    def __ne__(self, obj):
        return not (self == obj)

    def __hash__(self):
        return hash(str(hash(self._hap_id)) + str(hash(self.items_attrs())))

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
# HAPLOTYPES
#===============================================================================

class Haplotype(object):

    def __init__(self, hap_id, **attrs):
        self._hap_id = hap_id
        self._attrs = attrs

    def __eq__(self, obj):
        return obj is not None \
            and isinstance(obj, Haplotype) \
            and hash(self) == hash(obj)

    def __ne__(self, obj):
        return not (self == obj)

    def __hash__(self):
        return hash(self._hap_id)

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
# Edge
#===============================================================================

class Edge(object):

    def __init__(self, weight, *haps_id):
        self._weight = float(weight)
        self._haps_id = haps_id

    def __eq__(self, obj):
        return obj is not None \
            and isinstance(obj, Edge) \
            and hash(self) == hash(obj)

    def __ne__(self, obj):
        return not (self == obj)

    def __hash__(self):
        return hash(str(hash(self._weight)) + str(hash(tuple(self._haps_id))))

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




