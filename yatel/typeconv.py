#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# DOCS
#===============================================================================

"""Contains functions for convert various support types of yatel to more easily
serializable types.

"""

#===============================================================================
# IMPORTS
#===============================================================================

import decimal
import datetime
import inspect

from yatel import dom


#===============================================================================
# CONSTANTS
#===============================================================================

LITERAL_TYPE = "literal"

CONTAINER_TYPES = (tuple, set, list, frozenset)

HASHED_TYPES = tuple([dict] + dom.YatelDOM.__subclasses__())

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
    type(None): lambda x: None,
    complex: lambda x: unicode(x)
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
    type(None): lambda x: None,
    complex: lambda x: complex(x)
}

TYPES_TO_NAMES = dict(
    (k, k.__name__)
    for k in TO_SIMPLE_TYPES.keys() +
             list(CONTAINER_TYPES) +
             list(HASHED_TYPES) + [type]
)

NAMES_TO_TYPES = dict((v, k) for k, v in TYPES_TO_NAMES.items())


#===============================================================================
# FUNCTIONS
#===============================================================================

def simplifier(obj):
    typename = TYPES_TO_NAMES[type(obj)]
    value = ""
    if isinstance(obj, CONTAINER_TYPES):
        value = map(simplifier, obj)
    elif isinstance(obj, HASHED_TYPES):
        value = dict((k, simplifier(v)) for k, v in obj.items())
    elif type(obj) == type:
        value = TYPES_TO_NAMES[obj]
    else:
        value = TO_SIMPLE_TYPES[type(obj)](obj)
    return {"type": typename, "value": value}


def parse(obj):
    typename = obj["type"]
    value = obj["value"]
    if typename == LITERAL_TYPE:
        return value
    otype = NAMES_TO_TYPES[typename]
    if otype in CONTAINER_TYPES:
        value = map(parse, value)
    elif otype in HASHED_TYPES:
        data = dict((k, parse(v)) for k, v in value.items())
        value = otype(**data)
    elif otype == type:
        value = NAMES_TO_TYPES[value]
    else:
        value = TO_PYTHON_TYPES[otype](value)
    return value

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




