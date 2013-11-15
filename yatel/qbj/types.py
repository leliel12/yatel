#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# DOCS
#===============================================================================

"""

"""

#===============================================================================
# IMPORTS
#===============================================================================

import datetime, json

from yatel import dom, typeconv


#===============================================================================
# MAP
#===============================================================================

TYPES = {
    "bool": lambda x: x if isinstance(x, bool) else bool(x),
    "str": lambda x: x if isinstance(x, unicode) else unicode(x),
    "unicode": lambda x: x if isinstance(x, unicode) else unicode(x),
    "int": lambda x: x if isinstance(x, int) else int(x),
    "float": lambda x: x if isinstance(x, float) else float(x),
    "NoneType": lambda x: None,
    "complex": lambda x: x if isinstance(x, complex) else complex(x),
    "long": lambda x: x if isinstance(x, long) else long(x),
    "ignore": lambda x: x
}

#===============================================================================
# REGISTER TYPES
#===============================================================================

def register_type(**kwargs):

    def _wraps(func):
        name = kwargs.get("name") or func.__name__
        TYPES[name] = func
        return func

    return _wraps

#===============================================================================
# ERROR
#===============================================================================

class CastError(Exception):
    pass


#===============================================================================
# COMPLEX TYPE
#===============================================================================

@register_type(name="type")
def type_type(x):
    if type(x) == type:
        return x


@register_type(name="list")
def list_type(x):
    if isinstance(x, basestring):
        x = json.loads(x)
    if isinstance(x, list):
        return x
    return list(x)


@register_type(name="tuple")
def tuple_type(x):
    if isinstance(x, basestring):
        x = json.loads(x)
    if isinstance(x, tuple):
        return x
    return tuple(x)


@register_type(name="dict")
def object_name(x):
    if isinstance(x, basestring):
        x = json.loads(x)
    if isinstance(x, dict):
        return x
    return dict(x)


@register_type(name="datetime")
def datetime_type(x):
    if isinstance(x, datetime.datetime):
        return x
    return datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f")


@register_type(name="date")
def date_type(x):
    if isinstance(x, datetime.date):
        return x
    return datetime.datetime.strptime(x, "%Y-%m-%d").date()


@register_type(name="time")
def time_type(x):
    if isinstance(x, datetime.time):
        return x
    return datetime.datetime.strptime(x, "%H:%M:%S.%f").time()


@register_type(name="Haplotype")
def haplotype_type(x):
    if isinstance(x, dom.Haplotype):
        return x
    elif isinstance(x, dict):
        return dom.Haplotype(**x)
    return dom.Haplotype(x)


@register_type(name="Fact")
def fact_type(x):
    if isinstance(x, dom.Fact):
        return x
    elif isinstance(x, dict):
        return dom.Fact(**x)
    return dom.Fact(x)


@register_type(name="Edge")
def edge_type(x):
    if isinstance(x, dom.Edge):
        return x
    elif isinstance(x, dict):
        return dom.Edge(**x)
    elif isinstance(x, (list, tuple)):
        return dom.Edge(*x)
    return dom.Edge(x)


#===============================================================================
# FUNCTIONS
#===============================================================================

def cast(value, to_type):
    parsed = None
    if isinstance(to_type, list):
        value = TYPES["array"](value)
        if len(value) != len(to_type):
            msg = "Diferent lengths 'value' and 'type': {}, {}"
            raise CastError(msg.format(repr(value), repr(to_type)))
        parsed = []
        for v, t in zip(value, to_type):
            parsed.append(cast(v, t))
    elif isinstance(to_type, dict):
        value = TYPES["object"](value)
        if sorted(value.keys()) != sorted(to_type.keys()):
            msg = "Some key not match in 'type' or 'value'. {}, {}"
        parsed = {}
        for k, v in value.items():
            t = to_type[k]
            parsed[k] = cast(v, t)
    else:
        parsed = TYPES[to_type](value)
    return parsed


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

