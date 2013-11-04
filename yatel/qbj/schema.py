#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# DOCS
#===============================================================================

"""Defines the schema for validate all incomming QBJ

"""

#===============================================================================
# IMPORTS
#===============================================================================

import jsonschema

from yatel.qbj import functions

#===============================================================================
# SCHEMA
#===============================================================================

QBJ_SCHEMA = {
    # metadata
    "title": "Yatel QBJ Schema",
    "description": __doc__,

    # validation itself
    "type":  "object",
    "properties" : {
        "id": {
            "description": "unique id for a query. this will be returned in response"
        },
        "function": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "enum": functions.FUNCTIONS.keys()},
                "kwargs": {"type": "object"},
                "args": {"type": "array"}
            },
            "additionalProperties": False
        },
    },
    "required": ["id", "function"],
    "additionalProperties": False,
}


#===============================================================================
# FUNCTION
#===============================================================================

def validate(to_validate, *args, **kwargs):
    return jsonschema.validate(to_validate, QBJ_SCHEMA, *args, **kwargs)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
