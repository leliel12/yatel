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

from yatel.qbj import functions, types

#===============================================================================
# SCHEMA
#===============================================================================

# http://www.tutorialspoint.com/json/json_schema.htm


DEFINITIONS = {

    "ARGUMENT_STATIC_DEF": {
        "type": "object",
        "properties": {
            "type": {"type": "string", "enum": types.TYPES.keys()},
            "value": {"type": ["string", "number", "boolean", "null"] }
        },
        "additionalProperties": False
    },

    "ARGUMENT_FUNCTION_DEF": {
        "type": "object",
        "properties": {
            "type": {"type": "string", "enum": types.TYPES.keys()},
            "function": {"$ref": "#/definitions/FUNCTION_DEF"}
        },
        "additionalProperties": False
    },

    "ARGUMENT_DEF": {
        "type": "object",
        "oneOF": [
            {"$ref": "#/definitions/ARGUMENT_STATIC_DEF"},
            {"$ref": "#/definitions/ARGUMENT_FUNCTION_DEF"}
        ],
        "additionalProperties": False
    },

    "FUNCTION_DEF": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "enum": functions.FUNCTIONS.keys()},
            "kwargs": {
                "type": "object",
                "patternProperties": {
                    r".*": {"$ref": "#/definitions/ARGUMENT_DEF"}
                },
            },
            "args": {
                "type": "array",
                "items": {"$ref": "#/definitions/ARGUMENT_DEF"}
            }
        },
        "required": ["name"],
        "additionalProperties": False
    }
}


QBJ_SCHEMA = {
    # metadata
    "title": "Yatel QBJ Schema",
    "description": __doc__,

    # validation itself
    "type":  "object",
    "definitions" : DEFINITIONS,
    "properties" : {
        "id": {"type": ["string", "number", "boolean", "null"]},
        "function": { "$ref": "#/definitions/FUNCTION_DEF" }
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
