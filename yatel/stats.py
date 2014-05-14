#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Statistic functions for calculate weight statistics over yatel enviroments

"""

#===============================================================================
# IMPORT
#===============================================================================

import collections

import numpy as np

from scipy import stats

from yatel import db


#===============================================================================
# BASIC POSITION STATS
#===============================================================================

def average(nw, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.average(arr)


def median(nw, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.median(arr)


def percentile(nw, q, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.percentile(arr, q)


def min(nw, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.min(arr)


def max(nw, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.max(arr)


def amin(nw, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.amin(arr)


def amax(nw, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.amax(arr)


def sum(nw, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.sum(arr)


def mode(nw, env=None, **kwargs):
    """Calcula la moda sobre una red

    Parameters
    ----------
    nw : yatel.db.YatelNetwork
        La red sobre la que se desea calcular la estadistica
    env: yatel.dom.Enviroment or dict like
        Enviroment de filtrado para calcular este coso

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    cnt = collections.Counter(arr)
    value = np.max(cnt.values())
    n = cnt.values().count(value)
    return np.array(tuple(v[0] for v in cnt.most_common(n)))


#===============================================================================
# DISPERTION STATS
#===============================================================================

def var(nw, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.var(arr)


def std(nw, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.std(arr)


def variation(nw, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return stats.variation(arr)

def range(nw, env=None, **kwargs):
    """Range"""
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.amax(arr) - np.amin(arr)


#===============================================================================
# KURTOSIS
#===============================================================================

def kurtosis(nw, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return stats.kurtosis(arr)


#===============================================================================
# SUPPORT
#===============================================================================

def weights2array(edges):
    """Create a *numpy.ndarray* with all the weights of ``dom.Edges``"""
    generator = (e.weight for e in edges)
    return np.fromiter(generator, np.float128)


def env2weightarray(nw, env=None, **kwargs):
    """This function always return a *numpy.ndarray* with this conditions:

    - If ``nw`` is instance of ``numpy.ndarray`` the same array is returned.
    - If ``nw`` is instance of ``db.YatelNetwork`` and no enviroment is
      given return all the edges in this enviroment.
    - If ``nw`` is instance of ``db.YatelNetwork`` and no enviroment is
      given  then return all edges.
    - In the last case the function try to convert nw to ``numpy.ndarray``
      instance.

    """
    env = dict(env) if env else {}
    env.update(kwargs)
    if isinstance(nw, np.ndarray):
        if env:
            msg = "if nw is numpy.ndarray you you can't use enviroments"
            raise ValueError(msg)
        return nw
    elif isinstance(nw, db.YatelNetwork):
        if not env:
            return weights2array(nw.edges())
        return weights2array(nw.edges_by_enviroment(env=env))
    else:
        return np.array(nw)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




