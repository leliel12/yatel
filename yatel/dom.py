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
import decimal
import datetime
import inspect


#===============================================================================
# CONSTANTS
#===============================================================================

CONTAINER_TYPES = (tuple, set, list, frozenset)

HASH_TYPES = (dict,)

TO_SIMPLE_TYPES = {
    datetime.datetime: lambda x: x.isoformat(),
    datetime.time: lambda x: x.isoformat(),
    datetime.date: lambda x: x.isoformat(),
    bool: lambda x: x,
    int: lambda x: x,
    long: lambda x: x,
    float: lambda x: x,
    str: lambda x: x,
    unicode: lambda x: x,
    decimal.Decimal: lambda x: str(x),
    type(None): lambda x: None
}

TO_PYTHON_TYPES = {
    datetime.datetime:
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f"),
    datetime.time:
        lambda x: datetime.datetime.strptime(s, "%H:%M:%S.%f").time(),
    datetime.date:
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date(),
    bool:
        lambda x: x.lower() == "true" if isinstance(x, basestring) else bool(x),
    long: long,
    int: int,
    float: float,
    str: str,
    unicode: unicode,
    decimal.Decimal: lambda x: decimal.Decimal(x),
    type(None): lambda x: None
}


TYPES_TO_NAMES = dict((k, k.__name__) for k in TO_SIMPLE_TYPES.keys())

NAMES_TO_TYPES = dict((v, k) for k, v in TYPES_TO_NAMES.items())


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

    @classmethod
    def from_simple_dict(cls, data, types={}):
        prepared_data = {}
        for k, v in data.items():
            if k in types:
                type_parser = types[k]
                if type_parser in NAMES_TO_TYPES:
                    type_parser = NAMES_TO_TYPES[type_parser]
                v = type_parser(v)
            prepared_data[k] = v
        return cls(**prepared_data)



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

    def __init__(self, weight, *haps_id, **kwargs):
        """Creates a new instance.

        **Params**
            :weight: The degree of relationship between haplotypes.
            :haps_id: The list of the related haplotypes.

        """
        if haps_id and "haps_id" in kwargs:
            msg = "__init__() got multiple values for keyword argument 'haps_id'"
            raise TypeError(msg)
        haps_id = haps_id or kwargs["haps_id"]
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
# FUNCTIONS
#===============================================================================

def to_simple_type(e):
    if isinstance(e, YatelDOM):
        return e.as_simple_dict()
    etype = type(e)
    if etype in CONTAINER_TYPES:
        return map(to_simple_type, e)
    elif etype in HASH_TYPES:
        return dict((k, to_simple_type(v)) for k, v in e.items())
    elif etype == type:
        return TYPES_TO_NAMES[e]
    return TO_SIMPLE_TYPES[etype](e)


#~ def to_python_type(e, t, cls=dict):
    #~ if inspect.isclass(t) and issubclass(t, YatelDOM):
        #~ t.from_simple_dict(e


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




