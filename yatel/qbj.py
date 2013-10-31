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
    "amax": {'lambda': True, 'nwparam': 'nw', 'func': stats.amax},
    "amin": {'lambda': True, 'nwparam': 'nw', 'func': stats.amin },
    "average": {'lambda': True, 'nwparam': 'nw', 'func': stats.average},
    "env2weightarray": {'lambda': True, 'nwparam': 'nw', 'func': stats.env2weightarray},
    "kurtosis": {'lambda': True, 'nwparam': 'nw', 'func': stats.kurtosis},
    "max": {'lambda': True, 'nwparam': 'nw', 'func': stats.max},
    "median": {'lambda': True, 'nwparam': 'nw', 'func': stats.median},
    "min": {'lambda': True, 'nwparam': 'nw', 'func': stats.min},
    "mode": {'lambda': True, 'nwparam': 'nw', 'func': stats.mode},
    "percentile": {'lambda': True, 'nwparam': 'nw', 'func': stats.percentile},
    "range": {'lambda': True, 'nwparam': 'nw', 'func': stats.range},
    "std": {'lambda': True, 'nwparam': 'nw', 'func': stats.std},
    "sum": {'lambda': True, 'nwparam': 'nw', 'func': stats.sum},
    "var": {'lambda': True, 'nwparam': 'nw', 'func': stats.var},
    "varQ": {'lambda': True, 'nwparam': 'nw', 'func': stats.varQ},
    "variation": {'lambda': True, 'nwparam': 'nw', 'func': stats.variation},
    "weights2array": {'lambda': True, 'nwparam': 'nw', 'func': stats.weights2array},
    "Q": {'lambda': True, 'nwparam': 'nw', 'func': stats.Q},
    "TRI": {'lambda': True, 'nwparam': 'nw', 'func': stats.TRI},
    "MID": {'lambda': True, 'nwparam': 'nw', 'func': stats.MID},
    "MD": {'lambda': True, 'nwparam': 'nw', 'func': stats.MD},
    "MeD": {'lambda': True, 'nwparam': 'nw', 'func': stats.MeD},
    "MAD": {'lambda': True, 'nwparam': 'nw', 'func': stats.MAD},
    "H3_kelly": {'lambda': True, 'nwparam': 'nw', 'func': stats.H3_kelly},
    "H1_yule": {'lambda': True, 'nwparam': 'nw', 'func': stats.H1_yule},
    "Sp_pearson": {'lambda': True, 'nwparam': 'nw', 'func': stats.Sp_pearson},
    "K1_kurtosis": {'lambda': True, 'nwparam': 'nw', 'func': stats.K1_kurtosis},
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
            raise TypeError(msg.format(self._fname, ",".join(banned)))
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
            parser = fdata.get("parser") or default_parser

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

            argspec["defaults"] = [(repr(type(d)), str(d))
                                    for d in argspec["defaults"]]

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
