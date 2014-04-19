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

import inspect, collections
import datetime as dt

from yatel import stats, db


#===============================================================================
# MAP
#===============================================================================

FUNCTIONS = {}


#==============================================================================
# CLASS
#==============================================================================

QBJFunction = collections.namedtuple(
    "QBJFunction", ["name", "doc", "func"]
)


#===============================================================================
# REGISTER FUNCTION
#===============================================================================

def qbjfunction(name=None, doc=None):

    def _dec(func):
        qbjfunc = QBJFunction(
            name=name or func.__name__,
            doc=doc or func.__doc__,
            func=func
        )
        FUNCTIONS[qbjfunc.name] = qbjfunc
        return func

    return _dec


def execute(name, nw, *args, **kwargs):
    return FUNCTIONS[name].func(nw, *args, **kwargs)


#==============================================================================
# YATEL NETWORK
#==============================================================================

@qbjfunction(doc=db.YatelNetwork.haplotypes.__doc__)
def haplotypes(nw):
    return nw.haplotypes()


@qbjfunction(doc=db.YatelNetwork.haplotype_by_id.__doc__)
def haplotype_by_id(nw, hap_id):
    return nw.haplotype_by_id(hap_id)


@qbjfunction(doc=db.YatelNetwork.haplotypes_by_enviroment.__doc__)
def haplotypes_by_enviroment(nw, env=None, **kwargs):
    return nw.haplotypes_by_enviroment(env=env, **kwargs)


@qbjfunction(doc=db.YatelNetwork.edges.__doc__)
def edges(nw):
    return nw.edges()


@qbjfunction(doc=db.YatelNetwork.edges_by_haplotype.__doc__)
def edges_by_haplotype(nw, hap):
    return nw.edges_by_haplotype(hap)


@qbjfunction(doc=db.YatelNetwork.edges_by_enviroment.__doc__)
def edges_by_enviroment(nw, env=None, **kwargs):
    return nw.edges_by_enviroment(env=env, **kwargs)


@qbjfunction(doc=db.YatelNetwork.facts.__doc__)
def facts(nw):
    return nw.facts()


@qbjfunction(doc=db.YatelNetwork.facts_by_haplotype.__doc__)
def facts_by_haplotype(nw, hap):
    return nw.facts_by_haplotype(hap)


@qbjfunction(doc=db.YatelNetwork.facts_by_enviroment.__doc__)
def facts_by_enviroment(nw, env=None, **kwargs):
    return nw.facts_by_enviroment(env=env, **kwargs)


@qbjfunction(doc=db.YatelNetwork.describe.__doc__)
def describe(nw):
    return nw.describe()


@qbjfunction(doc=db.YatelNetwork.enviroments.__doc__)
def enviroments(nw, facts_attrs=None):
    return nw.enviroments(facts_attrs=facts_attrs)


#==============================================================================
# STATS
#==============================================================================

@qbjfunction(doc=stats.amax.__doc__)
def amax(nw, env=None, **kwargs):
    return stats.amax(nw, env=env, **kwargs)


@qbjfunction(doc=stats.amin.__doc__)
def amin(nw, env=None, **kwargs):
    return stats.amin (nw, env=env, **kwargs)


@qbjfunction(doc=stats.average.__doc__)
def average(nw, env=None, **kwargs):
    return stats.average(nw, env=env, **kwargs)


@qbjfunction(doc=stats.env2weightarray.__doc__)
def env2weightarray(nw, env=None, **kwargs):
    return stats.env2weightarray(nw, env=env, **kwargs)


@qbjfunction(doc=stats.kurtosis.__doc__)
def kurtosis(nw, env=None, **kwargs):
    return stats.kurtosis(nw, env=env, **kwargs)


@qbjfunction(doc=stats.max.__doc__)
def max(nw, env=None, **kwargs):
    return stats.max(nw, env=env, **kwargs)


@qbjfunction(doc=stats.median.__doc__)
def median(nw, env=None, **kwargs):
    return stats.median(nw, env=env, **kwargs)


@qbjfunction(doc=stats.min.__doc__)
def min(nw, env=None, **kwargs):
    return stats.min(nw, env=env, **kwargs)


@qbjfunction(doc=stats.mode.__doc__)
def mode(nw, env=None, **kwargs):
    return stats.mode(nw, env=env, **kwargs)


@qbjfunction(doc=stats.percentile.__doc__)
def percentile(nw, q, env=None, **kwargs):
    return stats.percentile(nw, q, env=env, **kwargs)


@qbjfunction(doc=stats.range.__doc__)
def range(nw, env=None, **kwargs):
    return stats.range(nw, env=env, **kwargs)


@qbjfunction(doc=stats.env2weightarray.__doc__)
def std(nw, env=None, **kwargs):
    return stats.std(nw, env=env, **kwargs)


@qbjfunction(doc=stats.sum.__doc__)
def sum(nw, env=None, **kwargs):
    return stats.sum(nw, env=env, **kwargs)


@qbjfunction(doc=stats.var.__doc__)
def var(nw, env=None, **kwargs):
    return stats.var(nw, env=env, **kwargs)


@qbjfunction(doc=stats.variation.__doc__)
def variation(nw, env=None, **kwargs):
    return stats.variation(nw, env=env, **kwargs)


#===============================================================================
# NATIVE QBJ FUNCTIONS
#===============================================================================

@qbjfunction()
def slice(nw, iterable, f, t=None):
    """Split the an iterable from Fth element to Tth element"""
    if t is None:
        return iterable[f:]
    return iterable[f:t]


#==============================================================================
# DATE AND TIME
#==============================================================================

@qbjfunction()
def now(nw, *args, **kwargs):
    return dt.datetime.now()


@qbjfunction()
def utcnow(nw, *args, **kwargs):
    return dt.datetime.utcnow()


@qbjfunction()
def today(nw, *args, **kwargs):
    return dt.date.today()


@qbjfunction()
def utctoday(nw, *args, **kwargs):
    return dt.datetime.utcnow().date()


@qbjfunction()
def time(nw, *args, **kwargs):
    return dt.datetime.now().time()


@qbjfunction()
def utctime(nw, *args, **kwargs):
    return dt.datetime.utcnow().time()


@qbjfunction
def get_from_time(nw, datetime_instance, dtformat, *args, **kwargs):
    return datetime_instance.strftime(dtformat)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

