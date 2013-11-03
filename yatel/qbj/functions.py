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

from yatel import stats


#===============================================================================
# MAP
#===============================================================================

#: Este ``dict`` contiene las funciones principales que se mapearan desde
#: yatel a posibles sentencias json. Cada llave representa el nombre de la
#: función dentro de YQBJ, por su parte los valores son siempre ``dicts`` que
#: tienen llaves siempre opcionales.
#:
#: Valores:
#:      "func": ``callable`` que indica que sera llamado a bajo nivel por esta
#:                función. De no estar presente se asume que la función que se
#:                llamará es un método interno (con el mismo nombre que la llave)
#:                a la instancia de ``yatel.db.YatelNetwork`` que este siendo
#:                mapeada. Solo se toma en cuenta si wrap es true.
#:      "wrap": ``bool`` si es ``True`` la función se enmascarara adentro de otro
#:              ``callable`` al cual se le enviara la instancia de
#:              ``yatel.db.YatelNetwork`` con el nombre definido en *nwparam*
#:      "nwparam": String que indica con que nombre se enviará la instancia de
#:                 ``yatel.db.YatelNetwork`` a la función si *wrap* es True.
#:                 Por defecto el valor es ``nw``
FUNCTIONS = {
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
    "amax": {'wrap': True,  'func': stats.amax},
    "amin": {'wrap': True,  'func': stats.amin },
    "average": {'wrap': True,  'func': stats.average},
    "env2weightarray": {'wrap': True,  'func': stats.env2weightarray},
    "kurtosis": {'wrap': True,  'func': stats.kurtosis},
    "max": {'wrap': True,  'func': stats.max},
    "median": {'wrap': True,  'func': stats.median},
    "min": {'wrap': True,  'func': stats.min},
    "mode": {'wrap': True,  'func': stats.mode},
    "percentile": {'wrap': True,  'func': stats.percentile},
    "range": {'wrap': True,  'func': stats.range},
    "std": {'wrap': True,  'func': stats.std},
    "sum": {'wrap': True,  'func': stats.sum},
    "var": {'wrap': True,  'func': stats.var},
    "varQ": {'wrap': True,  'func': stats.varQ},
    "variation": {'wrap': True,  'func': stats.variation},
    "weights2array": {'wrap': True,  'func': stats.weights2array},
    "Q": {'wrap': True,  'func': stats.Q},
    "TRI": {'wrap': True,  'func': stats.TRI},
    "MID": {'wrap': True,  'func': stats.MID},
    "MD": {'wrap': True,  'func': stats.MD},
    "MeD": {'wrap': True,  'func': stats.MeD},
    "MAD": {'wrap': True,  'func': stats.MAD},
    "H3_kelly": {'wrap': True,  'func': stats.H3_kelly},
    "H1_yule": {'wrap': True,  'func': stats.H1_yule},
    "Sp_pearson": {'wrap': True,  'func': stats.Sp_pearson},
    "K1_kurtosis": {'wrap': True,  'func': stats.K1_kurtosis},
}


#===============================================================================
# REGISTER FUNCTION
#===============================================================================

def register(**kwargs):

    def _wraps(func):
        name = kwargs.pop("name", None) or func.__name__
        kwargs["func"] = func
        FUNCTIONS[name] = kwargs
        return func

    return _wraps


#===============================================================================
# CLASSES
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
        kwargs.update(self._params)
        return self._func(*args, **kwargs)


class Function(object):

    def __init__(self, fname, func, parser, doc, argspec):
        self.fname = fname
        self.func = func
        self.parser = parser
        self.doc = doc
        self.argspec = argspec


#===============================================================================
# NATIVE QBX FUNCTIONS
#===============================================================================

@register(wrap=True)
def slice(iterable, f, t=None, **kwargs):
    """Split the an iterable from Fth element to Tth element"""
    if t is None:
        return iterable[f]
    return iterable[f:t]


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

