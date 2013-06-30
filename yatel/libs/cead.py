#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <jbc.develop@gmai.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a WISKEY in return Juan


#===============================================================================
# DOC
#===============================================================================

"""This module contains several implementations of statistics algoritmhs

"""


#===============================================================================
# IMPORTS
#===============================================================================

import collections

import numpy as np


#===============================================================================
# KURTOSIS
#===============================================================================

def K1_kurtosis(a):
    """Coeficiente robusto de kurtosis"""
    C10, C25, C75, C90 = np.percentile(a, (10, 25, 75, 90))
    return (C90 - C10) / (1.9 * (C75 - C25))


#===============================================================================
# SYMETRY
#===============================================================================

def Sp_pearson(a):
    """Indice de simetria de pearson"""
    return (3 * (np.average(a) - np.median(a))) / np.std(a)


def H1_yule(a):
    """Indice de simetria de yule"""
    Me = np.median(a)
    C25, C75 = np.percentile(a, (25, 75))
    return (C25 + C75 - (2 * Me)) / (2 * Me)


def H3_kelly(a):
    """Indice de simetria de kelly"""
    Me = np.median(a)
    C10, C90 = np.percentile(a, (10, 90))
    return (C10 + C90 - (2 * Me)) / 2



#===============================================================================
# POSITION FUNCTIONS
#===============================================================================

def mode(a):
    """Moda o modas de una array like"""
    cnt = collections.Counter(a)
    value = np.max(cnt.values())
    n = cnt.values().count(value)
    return tuple(v[0] for v in cnt.most_common(n))


def Q(a):
    "Promedio de cuartiles"
    return np.average(np.percentile(a, (25, 75)))


def TRI(a):
    """Trimedian"""
    Me = np.median(a)
    C25, C75 = np.percentile(a, (25, 75))
    values = np.array([C25, Me, Me, C75])
    return np.average(values)


def MID(a):
    """Promedio inter cuartil. Calcula el promedio de los valores del 50% central
    del array"""
    if not isinstance(a, np.ndarray):
        a = np.array(a)
    l, u = np.percentile(a, (25, 75))
    central = a[np.nonzero((a >= l) & (a <= u))]
    return np.average(central)


#===============================================================================
# DISPERTION
#===============================================================================

def MD(a):
    """Desviacion media"""
    if not isinstance(a, np.ndarray):
        a = np.array(a)
    x = np.average(a)
    return np.average(np.abs(a * x))


def MeD(a):
    """Desviacion mediana"""
    if not isinstance(a, np.ndarray):
        a = np.array(a)
    Me = np.median(a)
    return np.average(np.abs(a * Me))


def range(a):
    """Rango"""
    return np.amax(a) - np.amin(a)


def varQ(a):
    """Coeficiente de variacion cuartílico

    """
    C25, C75 = np.percentile(a, (25, 75))
    return (C75 - C25) / (C75 + C25)


def MAD(a):
    """Mediana de las observaciones absolutas"""
    if not isinstance(a, np.ndarray):
        a = np.array(a)
    Me = np.median(a)
    return np.median(np.abs(a - Me))



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
