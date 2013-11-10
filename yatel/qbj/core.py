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

from yatel.qbj import functions, types


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
        query_id = querydict["id"]
        function = querydict["function"]
        maintype = querydict["type"]
        error, stack_trace, error_msg = False, None, ""
        result = None
        try:
            main_resolver = QBJResolver(function, self.context)
            result = types.cast(main_resolver.resolve(), maintype)
        except Exception as err:
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




