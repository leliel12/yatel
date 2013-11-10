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

import datetime

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
    "object": lambda x: x if isinstance(x, dict) else dict(x),
}

#===============================================================================
# REGISTER TYPES
#===============================================================================

def register_type(**kwargs):

    def _wraps(func):
        name = kwargs.get("name") or func.__name__
        TYPES["name"] = func
        return func

    return _wraps


#===============================================================================
# COMPLEX TYPE
#===============================================================================

@register_type()
def datetime(x):
    if isinstance(x, datetime.datetime):
        return x
    return datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f")


@register_type()
def date(x):
    if isinstance(x, datetime.date):
        return x
    return datetime.datetime.strptime(x, "%Y-%m-%d").date()


@register_type()
def time(x):
    if isinstance(x, datetime.time):
        return x
    return datetime.datetime.strptime(x, "%H:%M:%S.%f").time()


@register_type()
def haplotype(x):
    if isinstance(x, dom.Haplotype):
        return x
    elif isinstance(x, dict):
        return dom.Haplotype(**x)
    return dom.Haplotype(*x)


@register_type()
def fact(x):
    if isinstance(x, dom.Fact):
        return x
    elif isinstance(x, dict):
        return dom.Fact(**x)
    return dom.Fact(*x)


@register_type()
def edge(x):
    if isinstance(x, dom.Edge):
        return x
    elif isinstance(x, dict):
        return dom.Edge(**x)
    return dom.Edge(*x)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

