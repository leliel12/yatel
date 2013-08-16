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

def average(dsrc, **env):
    arr = env2weightarray(dsrc, **env)
    return np.average(arr)


def median(dsrc, **env):
    arr = env2weightarray(dsrc, **env)
    return np.median(arr)


def percentile(dsrc, q, **env):
    arr = env2weightarray(dsrc, **env)
    return np.percentile(arr, q)


def min(dsrc, **env):
    arr = env2weightarray(dsrc, **env)
    return np.min(arr)


def max(dsrc, **env):
    arr = env2weightarray(dsrc, **env)
    return np.max(arr)


def amin(dsrc, **env):
    arr = env2weightarray(dsrc, **env)
    return np.amin(arr)


def amax(dsrc, **env):
    arr = env2weightarray(dsrc, **env)
    return np.amax(arr)


def sum(dsrc, **env):
    arr = env2weightarray(dsrc, **env)
    return np.sum(arr)


def mode(dsrc, **env):
    arr = env2weightarray(dsrc, **env)
    return cead.mode(arr)


def Q(dsrc, **env):
    """Quartile average"""
    arr = env2weightarray(dsrc, **env)
    return cead.Q(arr)


def TRI(dsrc, **env):
    """Trimedian"""
    arr = env2weightarray(dsrc, **env)
    return cead.TRI(arr)


def MID(dsrc, **env):
    """Inter quartile average"""
    arr = env2weightarray(dsrc, **env)
    return cead.MID(arr)


#===============================================================================
# DISPERTION STATS
#===============================================================================

def var(dsrc, **env):
    arr = env2weightarray(dsrc, **env)
    return np.var(arr)


def std(dsrc, **env):
    arr = env2weightarray(dsrc, **env)
    return np.std(arr)


def variation(dsrc, **env):
    arr = env2weightarray(dsrc, **env)
    return stats.variation(arr)


def MD(dsrc, **env):
    """Average deviation"""
    arr = env2weightarray(dsrc, **env)
    return cead.MD(arr)


def MeD(dsrc, **env):
    """Median deviation"""
    arr = env2weightarray(dsrc, **env)
    return cead.MeD(arr)


def range(dsrc, **env):
    """Range"""
    arr = env2weightarray(dsrc, **env)
    return cead.range(arr)


def varQ(dsrc, **env):
    """Quartile variation

    """
    arr = env2weightarray(dsrc, **env)
    return cead.varQ(arr)


def MAD(dsrc, **env):
    """Mediana of absolute observations"""
    arr = env2weightarray(dsrc, **env)
    return cead.MAD(arr)


#===============================================================================
# SYMETRY
#===============================================================================

def Sp_pearson(dsrc, **env):
    """Pearson symetry indicator"""
    arr = env2weightarray(dsrc, **env)
    return cead.Sp_pearson(arr)


def H1_yule(dsrc, **env):
    """Yule symetry indicator"""
    arr = env2weightarray(dsrc, **env)
    return cead.H1_yule(arr)


def H3_kelly(dsrc, **env):
    """Kelly symetry indicator"""
    arr = env2weightarray(dsrc, **env)
    return cead.H3_kelly(arr)


#===============================================================================
# KURTOSIS
#===============================================================================

def kurtosis(dsrc, **env):
    arr = env2weightarray(dsrc, **env)
    return stats.kurtosis(arr)


def K1_kurtosis(dsrc, **env):
    """Robust kurtosis coeficient"""
    arr = env2weightarray(dsrc, **env)
    return cead.K1_kurtosis(arr)


#===============================================================================
# SUPPORT
#===============================================================================

def weights2array(edges):
    """Create a *numpy.ndarray* with all the weights of ``dom.Edges``"""
    return np.array([e.weight for e in edges])


def env2weightarray(dsrc, **kwargs):
    """This function always return a *numpy.ndarray* with this conditions:

    - If ``dsrc`` is instance of ``numpy.ndarray`` the same array is returned.
    - If ``dsrc`` is instance of ``db.YatelNetwork`` and come enviroment is
      given return all the edges in this enviroment.
    - If ``dsrc`` is instance of ``db.Yateldsrcection`` and no enviroment is
      given  then return all edges.
    - In the last case the function try to convert dsrc to ``numpy.ndarray``
      instance.

    """
    if isinstance(dsrc, np.ndarray):
        return dsrc
    elif isinstance(dsrc, db.YatelNetwork):
        if not kwargs:
            return weights2array(dsrc.edges_iterator())
        return weights2array(dsrc.edges_enviroment(**kwargs))
    else:
        return np.array(dsrc)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




