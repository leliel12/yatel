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

from yatel.qbj import functions, types, schema

#===============================================================================
# CLASS QBJ RESOLVER
#===============================================================================

class QBJResolver(object):
    """ Class doc """

    def __init__ (self, function, context):
        """ Class initialiser """
        self.function = function
        self.context = context

    def resolve(self):
        name = self.function["name"]
        args = []
        value = None
        for arg in self.function.get("args"):
            atype = arg["type"]
            if "function" in arg:
                function = arg["function"]
                resolver = QBJResolver(function, self.context)
                value = resolver.resolve()
            else:
                value = args["value"]
            result = types.cast(value, atype)
            args.append(result)
        kwargs = {}
        for kw, arg in self.function.get("kwargs"):
            atype = args["type"]
            if "function" in arg:
                function = arg["function"]
                resolver = QBJResolver(function, self.context)
                value = resolver.resolve()
            else:
                value = args["value"]
            result = types.cast(value, atype)
            kwargs[kw] = result
        return context.evaluate(name, arg, kwargs)


#===============================================================================
# CLASS CORE
#===============================================================================

class QBJson(object):

    def __init__(self, nw):
        self.context = functions.wrap_network(nw)

    def execute_str(self, string, stack_trace_on_error=False):
        sin = StringIO.StringIO(string)
        sout = StringIO.StringIO()
        self.execute_stream(
            sin, sout, stack_trace_on_error=stack_trace_on_error
        )
        return sout.getvalue()

    def execute_stream(self, sin, sout, stack_trace_on_error=False):
        indict = json.load(sin)
        outdict = self.execute_dict(
            indict, stack_trace_on_error=stack_trace_on_error
        )
        return json.dump(outdict, sout)

    def execute_dict(self, querydict, stack_trace_on_error=False):
        query_id = None
        function = None
        maintype = None
        error = False
        stack_trace = None
        error_msg = ""
        result = None
        try:
            #schema.validate(querydict)
            query_id = querydict["id"]
            function = querydict["function"]
            maintype = querydict["type"]
            main_resolver = QBJResolver(function, self.context)
            result = types.cast(main_resolver.resolve(), maintype)
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
            "id": query_id, "error": False, "stack_trace": None,
            "error_msg": "",  "result": result
        }


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
