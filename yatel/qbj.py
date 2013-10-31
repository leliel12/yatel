#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# FUNCTION
#===============================================================================

import json

from yatel import dom
from yatel import db
from yatel import stats

from yatel.io import json_parser

#===============================================================================
# CONSTANTS
#===============================================================================

MAPINGS = {
    "haplotypes": {},
    "haplotype_by_id": {},
    "haplotypes_by_enviroment": {},
    "edges": {},
    "edges_by_haplotype": {},
    "edges_by_enviroment": {},
    "facts": {},
    "facts_by_haplotype": {},
    "facts_by_enviroment": {},
    "describe": {},
    "enviroments": {},

    # stats
    "amax": {'lambda': True, 'nwparam': 'nw'},
    "amin": {'lambda': True, 'nwparam': 'nw'},
    "average": {'lambda': True, 'nwparam': 'nw'},
    "cead": {'lambda': True, 'nwparam': 'nw'},
    "db": {'lambda': True, 'nwparam': 'nw'},
    "env2weightarray": {'lambda': True, 'nwparam': 'nw'},
    "kurtosis": {'lambda': True, 'nwparam': 'nw'},
    "max": {'lambda': True, 'nwparam': 'nw'},
    "median": {'lambda': True, 'nwparam': 'nw'},
    "min": {'lambda': True, 'nwparam': 'nw'},
    "mode": {'lambda': True, 'nwparam': 'nw'},
    "np": {'lambda': True, 'nwparam': 'nw'},
    "percentile": {'lambda': True, 'nwparam': 'nw'},
    "range": {'lambda': True, 'nwparam': 'nw'},
    "stats": {'lambda': True, 'nwparam': 'nw'},
    "std": {'lambda': True, 'nwparam': 'nw'},
    "sum": {'lambda': True, 'nwparam': 'nw'},
    "var": {'lambda': True, 'nwparam': 'nw'},
    "varQ": {'lambda': True, 'nwparam': 'nw'},
    "variation": {'lambda': True, 'nwparam': 'nw'},
    "weights2array": {'lambda': True, 'nwparam': 'nw'}

}





#===============================================================================
# MAPPED FUNCTION
#===============================================================================

class WrappedCallable(object):
    """Lambda with steroids"""

    def __init__(self, fname, func, params):
        if not hasattr(func, "__call__"):
            raise TypeError("'func' must be callable")
        self._func = func
        self._params = params
        self._banned_params = set(params)
        self._fname = fname

    def __call__(self, *args, **kwargs):
        banned = self._banned_params.intersection(kwargs)
        if banned:
            msg = "{}() got multiple values for keyword argument '{}'"
            raise TypeError(msg.format(self._fname, ",".join(banned))
        kwargs.update(params)
        return self._func(*args, **kwargs)


#===============================================================================
# QUERY
#===============================================================================

class QueryByJSON(object):
    """ Class doc """

    def __init__ (self, nw):
        """ Class initialiser """
        self._nw = nw
        self._func_map = function_map(nw)




#===============================================================================
# FUNCTION
#===============================================================================

def function_dict(nw):
        """
        """
        default_parser = lambda x: x
        mfunc = {}
        for fname, fdata in MAPINGS.items():
            func = None
            doc = None
            argspec = None
            if fdata.get("lambda"):
                func = WrappedCallable(fname, fdata["func"],
                                       {fdata["nwparam"]: nw})
                doc = fdata["func"].__doc__ or ""
                argspec = dict(inspect.getargspec(fdata["func"])._asdict())
                if fdata["nwparam"] in argspec["args"]:
                    argspec["args"].remove(fdata["nwparam"])
            else:
                func = getattr(nw, fname)
                doc = func.__doc__ or ""
                argspec = dict(inspect.getargspec(func)._asdict())
            parser = fdata.get("parser") or default_parser

            # parsing all default values

            mfunc[fname] = Function(fname, func, parser, doc, argspec)
        return mfuncs



haplotype_by_id_query = {
    "function": "haplotype_by_id",
    "id": None,
    "kwargs": {
        "hap_id": {
            "type": None,
            "value": 1
        }
    }
}

edges_by_haplotype = {
    "function": "edges_by_haplotype",
    "id": None,
    "args": [
        {
            "query": {
                "function": "haplotype_by_id",
                "kwargs": {
                    "hap_id": {
                        "type": None,
                        "value": 1
                    }
                }
            }
        }
    ]
}
