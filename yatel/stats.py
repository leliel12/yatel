#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Statistic functions for calculate weight statustics over yatel enviroments

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

def average(conn, **env):
    arr = env2weightarray(conn, **env)
    return np.average(arr)


def median(conn, **env):
    arr = env2weightarray(conn, **env)
    return np.median(arr)


def percentile(conn, q, **env):
    arr = env2weightarray(conn, **env)
    return np.percentile(arr, q)


def min(conn, **env):
    arr = env2weightarray(conn, **env)
    return np.min(arr)


def max(conn, **env):
    arr = env2weightarray(conn, **env)
    return np.max(arr)


def amin(conn, **env):
    arr = env2weightarray(conn, **env)
    return np.amin(arr)


def amax(conn, **env):
    arr = env2weightarray(conn, **env)
    return np.amax(arr)


def sum(conn, **env):
    arr = env2weightarray(conn, **env)
    return np.sum(arr)


def mode(conn, **env):
    arr = env2weightarray(conn, **env)
    return cead.mode(arr)


def Q(conn, **env):
    """Quartile average"""
    arr = env2weightarray(conn, **env)
    return cead.Q(arr)


def TRI(conn, **env):
    """Trimedian"""
    arr = env2weightarray(conn, **env)
    return cead.TRI(arr)


def MID(conn, **env):
    """Inter quartile average"""
    arr = env2weightarray(conn, **env)
    return cead.MID(arr)


#===============================================================================
# DISPERTION STATS
#===============================================================================

def var(conn, **env):
    arr = env2weightarray(conn, **env)
    return np.var(arr)


def std(conn, **env):
    arr = env2weightarray(conn, **env)
    return np.std(arr)


def variation(conn, **env):
    arr = env2weightarray(conn, **env)
    return stats.variation(arr)


def MD(conn, **env):
    """Average deviation"""
    arr = env2weightarray(conn, **env)
    return cead.MD(arr)


def MeD(conn, **env):
    """Median deviation"""
    arr = env2weightarray(conn, **env)
    return cead.MeD(arr)


def range(conn, **env):
    """Range"""
    arr = env2weightarray(conn, **env)
    return cead.range(arr)


def varQ(conn, **env):
    """Quartile variation

    """
    arr = env2weightarray(conn, **env)
    return cead.varQ(arr)


def MAD(conn, **env):
    """Mediana of absolute observations"""
    arr = env2weightarray(conn, **env)
    return cead.MAD(arr)


#===============================================================================
# SYMETRY
#===============================================================================

def Sp_pearson(conn, **env):
    """Pearson symetry indicator"""
    arr = env2weightarray(conn, **env)
    return cead.Sp_pearson(arr)


def H1_yule(conn, **env):
    """Yule symetry indicator"""
    arr = env2weightarray(conn, **env)
    return cead.H1_yule(arr)


def H3_kelly(conn, **env):
    """Kelly symetry indicator"""
    arr = env2weightarray(conn, **env)
    return cead.H3_kelly(arr)


#===============================================================================
# KURTOSIS
#===============================================================================

def kurtosis(conn, **env):
    arr = env2weightarray(conn, **env)
    return stats.kurtosis(arr)


def K1_kurtosis(conn, **env):
    """Robust kurtosis coeficient"""
    arr = env2weightarray(conn, **env)
    return cead.K1_kurtosis(arr)


#===============================================================================
# SUPPORT
#===============================================================================

def weights2array(edges):
    """Create a *numpy.ndarray* with all the weights of ``dom.Edges``"""
    return np.array([e.weight for e in edges])


def env2weightarray(conn, **kwargs):
    """This function always return a *numpy.ndarray* with this conditions:

    - If ``conn`` is instance of ``numpy.ndarray`` the same array is returned.
    - If ``conn`` is instance of ``db.YatelConnection`` and come enviroment is
      given return all the edges in this enviroment.
    - If ``conn`` is instance of ``db.YatelConnection`` and no enviroment is
      given  then return all edges.
    - In the last case the function try to convert conn to ``numpy.ndarray``
      instance.

    """
    if isinstance(conn, np.ndarray):
        return conn
    elif isinstance(conn, db.YatelConnection):
        if not kwargs:
            return weights2array(conn.iter_edges())
        return weights2array(conn.edges_enviroment(**kwargs))
    else:
        return np.array(conn)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




