#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# DOCS
#===============================================================================

"""Domain Object Model for Yatel.

"""

#===============================================================================
# IMPORTS
#===============================================================================

import collections


#===============================================================================
# BASE CLASS
#===============================================================================

class YatelDOM(collections.Mapping):

    def __init__(self, **attrs):
        if "id" in attrs:
            raise ValueError("'id' is not valid attribute name")
        self._data = attrs
        super(YatelDOM, self).__init__()

    def __getitem__(self, k):
        return self._data[k]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __eq__(self, obj):
        """x.__eq__(y) <==> x==y"""
        return isinstance(obj, type(self)) and super(YatelDOM, self).__eq__(obj)

    def __ne__(self, obj):
        """x.__ne__(y) <==> x!=y"""
        return not (self == obj)

    def __getattr__(self, n):
        """x.__getattr__('name') <==> x.name <==> x['name']"""
        try:
            return self._data[n]
        except KeyError:
            t = type(self).__name__
            msg = "'{t}' object has no attribute '{n}'".format(t=t, n=n)
            raise AttributeError(msg)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return repr(self._data)

    def as_simple_dict(self):
        return to_simple_type(self._data)


#===============================================================================
# HAPLOTYPES
#===============================================================================

class Haplotype(YatelDOM):
    """Represent a individual class or group with similar characteristics
    to be analized."""

    def __init__(self, hap_id, **attrs):
        """Creates a new instance

        **Params**
            :hap_id: Unique id of this haplotype.
            :attrs: Diferents attributes of this haplotype.

        """
        attrs["hap_id"] = hap_id
        super(Haplotype, self).__init__(**attrs)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        cls = type(self).__name__
        desc = self.hap_id
        at = hex(id(self))
        return "<{cls} ({desc}) at {at}>".format(cls=cls, desc=desc, at=at)


#===============================================================================
# FACT
#===============================================================================

class Fact(YatelDOM):
    """The Fact represent a *metadata* of the *haplotype*.

    For example if you relieve in two places the same *haplotype*,
    the characteristics of these places correspond to different *facts* of the
    same *haplotype*.

    """

    def __init__(self, hap_id, **attrs):
        """Creates a new instance

        **Params**
            :hap_id: The ``dom.Haplotype`` id of this fact.
            :attrs: Diferents attributes of this fact.

        """
        attrs["hap_id"] = hap_id
        super(Fact, self).__init__(**attrs)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        cls = type(self).__name__
        desc = "of Haplotype '{hap_id}'".format(hap_id=self.hap_id)
        at = hex(id(self))
        return "<{cls} ({desc}) at {at}>".format(cls=cls, desc=desc, at=at)


#===============================================================================
# Edge
#===============================================================================

class Edge(YatelDOM):
    """Represent a relation between 2 or more *haplotypes*

    """

    def __init__(self, weight, haps_id):
        """Creates a new instance.

        **Params**
            :weight: The degree of relationship between haplotypes.
            :haps_id: The list of the related haplotypes.

        """
        super(Edge, self).__init__(weight=float(weight), haps_id=haps_id)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        cls = type(self).__name__
        desc = "[{weight} {haps_id}]  ".format(weight=self.weight,
                                               haps_id=str(self.haps_id))
        at = hex(id(self))
        return "<{cls} ({desc}) at {at}>".format(cls=cls, desc=desc, at=at)


#===============================================================================
# ENVIROMENT
#===============================================================================

class Enviroment(YatelDOM):

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        cls = type(self).__name__
        desc = super(Enviroment, self).__repr__()
        at = hex(id(self))
        return "<{cls} {desc} at {at}>".format(cls=cls, desc=desc, at=at)


#===============================================================================
# DESCRIPTOR
#===============================================================================

class Descriptor(YatelDOM):

    def __init__(self, uri, mode, fact_attributes,
                 haplotype_attributes, edge_attributes, size):
        super(Descriptor, self).__init__(
            uri=uri, mode=mode, fact_attributes=fact_attributes,
            haplotype_attributes=haplotype_attributes,
            edge_attributes=edge_attributes, size=size
        )

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        cls = type(self).__name__
        desc = self.uri
        at = hex(id(self))
        return "<{cls} '{desc}' at {at}>".format(cls=cls, desc=desc, at=at)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




