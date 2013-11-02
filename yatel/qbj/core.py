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

import inspect

from yatel.qbj import functions


#===============================================================================
# CLASS CORE
#===============================================================================

class QBJson(object):

    def __init__(self, nw):
            """
            """
            self.functions = {}
            default_parser = lambda x: x
            for fname, fdata in functions.FUNCTIONS.items():

                func = None
                doc = None
                argspec = None
                parser = fdata.get("parser") or default_parser

                if fdata.get("wrap"):
                    nwparam = fdata.get("nwparam") or "nw"
                    internalfunc = fdata.get("func")
                    params = {nwparam: nw}
                    func = functions.WrappedCallable(fname, internalfunc, params)
                    doc = fdata["func"].__doc__ or ""
                    argspec = dict(inspect.getargspec(internalfunc)._asdict())
                    if nwparam in argspec["args"]:
                        argspec["args"].remove(nwparam)
                else:
                    func = getattr(nw, fname)
                    doc = func.__doc__ or ""
                    argspec = dict(inspect.getargspec(func)._asdict())
                    argspec["args"].pop(0)

                argspec["defaults"] = [(repr(type(d)), str(d))
                                        for d in argspec["defaults"] or ()]
                self.functions[fname] = functions.Function(fname, func, parser,
                                                           doc, argspec)

    def execute_str(self, string):
        sin = StringIO.StringIO(string)
        sout = StringIO.StringIO()
        self.execute_stream(sin, sout)
        return sout.getvalue()

    def execute_stream(self, sin, sout):
        pass

    def execute_dict(self, querydict):
        pass
