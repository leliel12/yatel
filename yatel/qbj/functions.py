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
#:      "sendnw": ``bool`` No se ejecuta en el contexto de la intancia de
#:                ``yatel.db.YatelNetwork``, por lo cual no se envia el *nwparam*.
#:                 por defecto en True
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
    "variation": {'wrap': True,  'func': stats.variation},
}


#===============================================================================
# REGISTER FUNCTION
#===============================================================================

def register_func(**kwargs):

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
        self._fname = fname

    def __call__(self, *args, **kwargs):
        for k, v in self._params.items():
            if k not in kwargs:
                kwargs[k] = v
        return self._func(*args, **kwargs)


class QBJFunction(object):

    def __init__(self, fname, func, parser, doc, argspec):
        self.fname = fname
        self.func = func
        self.parser = parser
        self.doc = doc
        self.argspec = argspec


class QBJContext(dict):

    def evaluate(self, name, args, kwargs):
        return self[name].func(*args, **kwargs)

#===============================================================================
# NATIVE QBX FUNCTIONS
#===============================================================================

@register_func(wrap=True, sendnw=False)
def slice(iterable, f, t=None):
    """Split the an iterable from Fth element to Tth element"""
    if t is None:
        return iterable[f:]
    return iterable[f:t]

@register_func(wrap=True, sendnw=False)
def ping():
    "Return always True"
    return True


#===============================================================================
# NETWORK WRAPPER
#===============================================================================

def wrap_network(nw):
    wrapped_network = QBJContext()
    default_parser = lambda x: x
    for fname, fdata in FUNCTIONS.items():

        wrapped_network_data = {}

        func = None
        doc = None
        argspec = None
        parser = fdata.get("parser") or default_parser

        if fdata.get("wrap"):
            sendnw = fdata.get("sendnw", True)
            nwparam = fdata.get("nwparam") or "nw"
            internalfunc = fdata.get("func")
            params = {nwparam: nw} if sendnw else {}
            func = WrappedCallable(fname, internalfunc, params)
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
        wrapped_network[fname] = QBJFunction(fname, func, parser, doc, argspec)
    return wrapped_network


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

