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

from yatel.qbx import function_maps


#===============================================================================
# CLASS
#===============================================================================

class YQBX(object):

    def __init__(self, nw):
            """
            """
            default_parser = lambda x: x
            mfunc = {}
            for fname, fdata in function_maps.FUNCTION_MAP.items():

                func = None
                doc = None
                argspec = None
                parser = fdata.get("parser") or default_parser

                if fdata.get("wrap"):
                    nwparam = fdata.get("nwparam") or "nw"
                    internalfunc = fdata.get("func")
                    func = function_maps.WrappedCallable(fname, internalfunc,
                                                         {nwparam: nw})
                    doc = fdata["func"].__doc__ or ""
                    argspec = dict(inspect.getargspec(internalfunc)._asdict())
                    if nwparam in argspec["args"]:
                        argspec["args"].remove(fdata["nwparam"])
                else:
                    func = getattr(nw, fname)
                    doc = func.__doc__ or ""
                    argspec = dict(inspect.getargspec(func)._asdict())
                    argspec["args"].pop(0)

                argspec["defaults"] = [(repr(type(d)), str(d))
                                        for d in argspec["defaults"]]
                mfunc[fname] = function_maps.YQBXFunction(fname, func, parser,
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
