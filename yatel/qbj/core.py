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

import sys
import json
import traceback

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from yatel import typeconv
from yatel.qbj import functions, schema


#===============================================================================
# CLASS QBJ RESOLVER
#===============================================================================

class QBJResolver(object):
    """ Class doc """

    def __init__ (self, function, context):
        """ Class initialiser """
        self.function = function
        self.context = context

    def argument_resolver(self, arg):
        atype = arg["type"]
        value = None
        if "function" in arg:
            function = arg["function"]
            resolver = QBJResolver(function, self.context)
            value = resolver.resolve()
        else:
            value = arg["value"]
        return typeconv.parse({"type": atype, "value": value})

    def resolve(self):
        name = self.function["name"]
        args = []
        for arg in self.function.get("args", ()):
            result = self.argument_resolver(arg)
            args.append(result)
        kwargs = {}
        for kw, arg in self.function.get("kwargs", {}).items():
            result = self.argument_resolver(arg)
            kwargs[kw] = result
        return self.context.evaluate(name, args, kwargs)


#===============================================================================
# CLASS CORE
#===============================================================================

class QBJEngine(object):

    def __init__(self, nw):
        self.context = functions.wrap_network(nw)

    def execute_dict(self, querydict, stack_trace_on_error=False):
        query_id = None
        function = None
        error = False
        stack_trace = None
        error_msg = ""
        result = None
        try:
            #schema.validate(querydict)
            query_id = querydict["id"]
            function = querydict["function"]
            main_resolver = QBJResolver(function, self.context)
            result = typeconv.simplifier(main_resolver.resolve())
        except Exception as err:
            if not query_id and isinstance(querydict, dict):
                query_id = querydict.get("id")
            error = True
            error_msg = unicode(err)
            if stack_trace_on_error:
                stack_trace = u"".join(
                    traceback.format_exception(*sys.exc_info())
                )
        return {
            "id": query_id, "error": error, "stack_trace": stack_trace,
            "error_msg": error_msg, "result": result
        }


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
