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

def average(dsrc, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return np.average(arr)


def median(dsrc, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return np.median(arr)


def percentile(dsrc, q, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return np.percentile(arr, q)


def min(dsrc, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return np.min(arr)


def max(dsrc, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return np.max(arr)


def amin(dsrc, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return np.amin(arr)


def amax(dsrc, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return np.amax(arr)


def sum(dsrc, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return np.sum(arr)


def mode(dsrc, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.mode(arr)


def Q(dsrc, env=None, **kwargs):
    """Quartile average"""
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.Q(arr)


def TRI(dsrc, env=None, **kwargs):
    """Trimedian"""
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.TRI(arr)


def MID(dsrc, env=None, **kwargs):
    """Inter quartile average"""
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.MID(arr)


#===============================================================================
# DISPERTION STATS
#===============================================================================

def var(dsrc, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return np.var(arr)


def std(dsrc, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return np.std(arr)


def variation(dsrc, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return stats.variation(arr)


def MD(dsrc, env=None, **kwargs):
    """Average deviation"""
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.MD(arr)


def MeD(dsrc, env=None, **kwargs):
    """Median deviation"""
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.MeD(arr)


def range(dsrc, env=None, **kwargs):
    """Range"""
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.range(arr)


def varQ(dsrc, env=None, **kwargs):
    """Quartile variation

    """
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.varQ(arr)


def MAD(dsrc, env=None, **kwargs):
    """Mediana of absolute observations"""
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.MAD(arr)


#===============================================================================
# SYMETRY
#===============================================================================

def Sp_pearson(dsrc, env=None, **kwargs):
    """Pearson symetry indicator"""
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.Sp_pearson(arr)


def H1_yule(dsrc, env=None, **kwargs):
    """Yule symetry indicator"""
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.H1_yule(arr)


def H3_kelly(dsrc, env=None, **kwargs):
    """Kelly symetry indicator"""
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.H3_kelly(arr)


#===============================================================================
# KURTOSIS
#===============================================================================

def kurtosis(dsrc, env=None, **kwargs):
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return stats.kurtosis(arr)


def K1_kurtosis(dsrc, env=None, **kwargs):
    """Robust kurtosis coeficient"""
    arr = env2weightarray(dsrc, env=env, **kwargs)
    return cead.K1_kurtosis(arr)


#===============================================================================
# SUPPORT
#===============================================================================

def weights2array(edges):
    """Create a *numpy.ndarray* with all the weights of ``dom.Edges``"""
    return np.array([e.weight for e in edges])


def env2weightarray(dsrc, env=None, **kwargs):
    """This function always return a *numpy.ndarray* with this conditions:

    - If ``dsrc`` is instance of ``numpy.ndarray`` the same array is returned.
    - If ``dsrc`` is instance of ``db.YatelNetwork`` and no enviroment is
      given return all the edges in this enviroment.
    - If ``dsrc`` is instance of ``db.YatelNetwork`` and no enviroment is
      given  then return all edges.
    - In the last case the function try to convert dsrc to ``numpy.ndarray``
      instance.

    """
    env = dict(env) if env else {}
    env.update(kwargs)
    if isinstance(dsrc, np.ndarray):
        return dsrc
    elif isinstance(dsrc, db.YatelNetwork):
        if not env:
            return weights2array(dsrc.edges_iterator())
        return weights2array(dsrc.edges_enviroment(env=env))
    else:
        return np.array(dsrc)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




