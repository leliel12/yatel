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

import numpy as np

from scipy import stats

from yatel import db
from yatel.libs import cead


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
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.mode(arr)


def Q(nw, env=None, **kwargs):
    """Quartile average"""
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.Q(arr)


def TRI(nw, env=None, **kwargs):
    """Trimedian"""
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.TRI(arr)


def MID(nw, env=None, **kwargs):
    """Inter quartile average"""
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.MID(arr)


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


def MD(nw, env=None, **kwargs):
    """Average deviation"""
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.MD(arr)


def MeD(nw, env=None, **kwargs):
    """Median deviation"""
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.MeD(arr)


def range(nw, env=None, **kwargs):
    """Range"""
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.range(arr)


def varQ(nw, env=None, **kwargs):
    """Quartile variation

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.varQ(arr)


def MAD(nw, env=None, **kwargs):
    """Mediana of absolute observations"""
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.MAD(arr)


#===============================================================================
# SYMETRY
#===============================================================================

def Sp_pearson(nw, env=None, **kwargs):
    """Pearson symetry indicator"""
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.Sp_pearson(arr)


def H1_yule(nw, env=None, **kwargs):
    """Yule symetry indicator"""
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.H1_yule(arr)


def H3_kelly(nw, env=None, **kwargs):
    """Kelly symetry indicator"""
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.H3_kelly(arr)


#===============================================================================
# KURTOSIS
#===============================================================================

def kurtosis(nw, env=None, **kwargs):
    arr = env2weightarray(nw, env=env, **kwargs)
    return stats.kurtosis(arr)


def K1_kurtosis(nw, env=None, **kwargs):
    """Robust kurtosis coeficient"""
    arr = env2weightarray(nw, env=env, **kwargs)
    return cead.K1_kurtosis(arr)


#===============================================================================
# SUPPORT
#===============================================================================

def weights2array(edges):
    """Create a *numpy.ndarray* with all the weights of ``dom.Edges``"""
    return np.array([e.weight for e in edges])


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
            return weights2array(nw.edges_iterator())
        return weights2array(nw.edges_enviroment(env=env))
    else:
        return np.array(nw)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




