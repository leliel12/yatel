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

from yatel import dom


#===============================================================================
# MAP
#===============================================================================

TYPES = {
    "boolean": lambda x: x if isinstance(x, bool) else bool(x),
    "string": lambda x: x if isinstance(x, unicode) else unicode(x),
    "integer": lambda x: x if isinstance(x, int) else int(x),
    "float": lambda x: x if isinstance(x, float) else float(x),
    "null": lambda x: None,
    "complex": lambda x: x if isinstance(x, complex) else complex(x),
    "array": lambda x: x if isinstance(x, list) else list(x),
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
# COMPLEX TYPE
#===============================================================================

@register_type(name="array")
def array_type(x):
    if isinstance(x, basestring):
        x = json.loads(x)
    if isinstance(x, list):
        return x
    return list(x)


@register_type(name="object")
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


@register_type()
def time(x):
    if isinstance(x, datetime.time):
        return x
    return datetime.datetime.strptime(x, "%H:%M:%S.%f").time()


@register_type(name="haplotype")
def haplotype_type(x):
    if isinstance(x, dom.Haplotype):
        return x
    elif isinstance(x, dict):
        return dom.Haplotype(**x)
    return dom.Haplotype(x)


@register_type(name="fact")
def fact_type(x):
    if isinstance(x, dom.Fact):
        return x
    elif isinstance(x, dict):
        return dom.Fact(**x)
    return dom.Fact(x)


@register_type(name="edge")
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
    return TYPES[to_type](value)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

