#!/usr/bin/env python
# -*- coding: utf-8 -*-

# csv.py
     
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
# IMPORTS
#===============================================================================

import csvcool

import dom


#===============================================================================
# VALIDATORS
#===============================================================================

_validators = {}
_conversors = {}

def register(for_type, func_type, func=None):

    def _wrap(func):
        if func_type == "validator":
            _validators[for_type] = func
        elif func_type == "conversor":
            _conversors[for_type] = func
        else:
            msg = "Invalid func_type '{ft}'".format(ft=func_type)
            raise ValueError(msg)
        return func

    if func == None:
        return _wrap
    _wrap(func)


def types():
    return _validators.keys()
    
    
@register(bool, "validator")
def is_bool(v):
    return v.strip().lower() in ("true", "false", "0", "1", "")


@register(bool, "conversor")
def to_bool(v):
    v = v.strip().lower()
    if v in ("true", "1"):
        return True
    elif v in ("false", "0", ""):
        return False
    msg = "Invalid {type} value: {v}".format(type="bool", v=v)
    raise ValueError(msg)


@register(int, "validator")
def is_int(v):
    return v.strip().isdigit() or not v.strip()


@register(int, "conversor")
def to_int(v):
    if "." not in v:
        return int(v) if v.strip() else 0
    msg = "Invalid {type} value: {v}".format(type="int", v=v)
    raise ValueError(msg)


@register(float, "validator")
def is_float(v):
    return v.strip().replace(".", "0").isdigit() or not v.strip()


@register(float, "conversor")
def to_float(v):
    return float(v) if v.strip() else 0.0


@register(str, "validator")
def is_str(v):
    return isinstance(v, basestring)


@register(str, "conversor")
def to_str(v):
    return v


@register(type(None), "validator")
def is_none(v):
    return not v.strip()


@register(type(None), "conversor")
def to_none(v):
    return None
    

#===============================================================================
# LOGIC
#===============================================================================

def discover_types(cool, order=(bool, int, float, type(None), str)):
    """Try to infer the type of columns of a CSVCool instance """
    types = {}
    for cn in cool.columnnames:
        column = cool.column(cn)
        for t in order:
            if all(map(_validators[t], column)):
                break
        types[cn] = t
    return types


def type_corrector(cool, column_types):
    correct = []
    for row in cool:
        crow = []
        for cname in cool.columnnames:
            ctype = column_types[cname]
            conversor = _conversors[ctype]
            crow.append(conversor(row[cname]))
        correct.append(crow)
    return csvcool.CSVCool(cool.columnnames, correct)


def construct_facts(cool, column_haplotype):
    assert column_haplotype in cool.columnnames
    facts = []
    for row in cool:
        hap_id = None
        atts = {}
        for cname, cvalue in row.items():
            if cname == column_haplotype:
                hap_id = str(cvalue)
            else:
                atts[cname] = cvalue
        facts.append(dom.Fact(hap_id, **atts))
    return tuple(facts)


def construct_haplotypes(cool, column_id):
    assert column_id in cool.columnnames
    haps = []
    for row in cool:
        hap_id = None
        atts = {}
        for cname, cvalue in row.items():
            if cname == column_id:
                hap_id = str(cvalue)
            else:
                atts[cname] = cvalue
        haps.append(dom.Haplotype(hap_id, **atts))
    return tuple(haps)
    
    
def construct_edges(cool, column_weight):
    assert column_weight in cool.columnnames
    edges = []
    for row in cool:
        weight = None
        haps_id = []
        for cname, cvalue in row.items():
            if cname == column_weight:
                weight = cvalue
            else:
                haps_id.append(cvalue)
        edges.append(dom.Edge(weight, *haps_id))
    return tuple(edges)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




