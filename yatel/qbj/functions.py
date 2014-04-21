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

FUNCTIONS = collections.OrderedDict()

PRIVATE_FUNC_DATA = ["func"]


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


def pformat_data(fname):
    fdata = FUNCTIONS[fname]
    data = {}
    for k, v in fdata._asdict().items():
        if k not in PRIVATE_FUNC_DATA:
            data[k] = v
    return data


def execute(name, nw, *args, **kwargs):
    return FUNCTIONS[name].func(nw=nw, *args, **kwargs)


#==============================================================================
# HELP FUNCTION
#==============================================================================

@qbjfunction()
def help(nw, fname=None):
    if fname is None:
        return list(FUNCTIONS.keys())
    return pformat_data(fname)


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
# GENERIC ITERATION
#===============================================================================

@qbjfunction()
def slice(nw, iterable, f, t=None):
    """Split the an iterable from Fth element to Tth element"""
    if t is None:
        return iterable[f:]
    return iterable[f:t]


@qbjfunction()
def size(nw, iterable):
    return len(iterable)


@qbjfunction()
def sort(nw, iterable, key=None, dkey=None, reverse=False):

    def keyextractor(elem):
        if isinstance(elem, collections.Mapping):
            return elem.get(key, dkey)
        return getattr(elem, key, dkey)

    if key is None:
        return sorted(iterable, reverse=reverse)
    return sorted(iterable, key=keyextractor, reverse=reverse)


@qbjfunction()
def index(nw, iterable, value, start=None, end=None):
    try:
        if start is None and end is None:
            return iterable.index(value)
        if end is None:
            return iterable.index(value, start)
        return iterable.index(value, start, end)
    except:
        return -1


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


#==============================================================================
# ARITMETICS
#==============================================================================

@qbjfunction()
def minus(nw, minuend, sust):
    return minuend - sust


@qbjfunction()
def times(nw, t0, t1):
    return t0 * t1


@qbjfunction()
def div(nw, dividend, divider):
    return dividend / float(divider)


@qbjfunction()
def floor(nw, dividend, divider):
    return dividend % float(divider)


@qbjfunction()
def pow(nw, radix, exp):
    return radix ** exp


@qbjfunction()
def xroot(nw, radix, root):
    return radix ** (1/float(root))


@qbjfunction()
def count(nw, iterable, to_count):
    return collections.Counter(iterable)[to_count]


#==============================================================================
# STRING
#==============================================================================

@qbjfunction()
def split(nw, string, s=None, maxsplit=None):
    if s is None and maxsplit is None:
        return string.split()
    elif maxsplit is None:
        return string.split(s)
    return string.split(s, maxsplit)


@qbjfunction()
def rsplit(nw, string, s=None, maxsplit=None):
    if s is None and maxsplit is None:
        return string.rsplit()
    elif maxsplit is None:
        return string.rsplit(s)
    return string.rsplit(s, maxsplit)


@qbjfunction()
def strip(nw, string, chars=None):
    if chars is None:
        return string.strip()
    return string.strip(chars)


@qbjfunction()
def lstrip(nw, string, chars=None):
    if chars is None:
        return string.lstrip()
    return string.lstrip(chars)


@qbjfunction()
def rstrip(nw, string, chars=None):
    if chars is None:
        return string.rstrip()
    return string.rstrip(chars)


@qbjfunction()
def join(nw, joiner, to_join):
    return joiner.join(to_join)


@qbjfunction()
def upper(nw, string):
    return string.upper()


@qbjfunction()
def lower(nw, string):
    return string.lower()


@qbjfunction()
def title(nw, string):
    return string.title()


@qbjfunction()
def capitalize(nw, string):
    return string.capitalize()


@qbjfunction()
def isalnum(nw, string):
    return string.isalnum()


@qbjfunction()
def isalpha(nw, string):
    return string.isalpha()


@qbjfunction()
def isdigit(nw, string):
    return string.isdigit()


@qbjfunction()
def startswith(nw, string, suffix, start=None, end=None):
    if start is None and end is None:
        return string.startswith(suffix)
    if end is None:
        return string.startswith(suffix, start)
    return string.startswith(suffix, start, end)


@qbjfunction()
def endswith(nw, string, suffix, start=None, end=None):
    if start is None and end is None:
        return string.endswith(suffix)
    if end is None:
        return string.endswith(suffix, start)
    return string.endswith(suffix, start, end)


@qbjfunction()
def istitle(nw, string):
    return string.istitle()


@qbjfunction()
def isupper(nw, string):
    return string.isupper()


@qbjfunction()
def isspace(nw, string):
    return string.isspace()


@qbjfunction()
def islower(nw, string):
    return string.islower()


@qbjfunction()
def swapcase(nw, string):
    return string.swapcase()


@qbjfunction()
def replace(nw, string, old, new, count=None):
    if count is None:
        return string.replace(old, new)
    return string.replace(old, new, count)


@qbjfunction()
def find(nw, string, subs, start=None, end=None):
    try:
        if start is None and end is None:
            return string.find(subs)
        if end is None:
            return string.find(subs, start)
        return string.find(subs, start, end)
    except:
        return -1


@qbjfunction()
def rfind(nw, string, subs, start=None, end=None):
    try:
        if start is None and end is None:
            return string.rfind(subs)
        if end is None:
            return string.rfind(subs, start)
        return string.rfind(subs, start, end)
    except:
        return -1


# TODO: Regex, trigonometric, and math contants SUPPORT

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

