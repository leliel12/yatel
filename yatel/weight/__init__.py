#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This package contains several modules for calculatte distances between
haplotypes in yatel

"""

#===============================================================================
# IMPORTS
#===============================================================================

import inspect

from yatel.weight.core import Weight

#===============================================================================
# FUNCTIONS
#===============================================================================

_weights = {}
def register(cls, *names):
    if not inspect.isclass(cls) or not issubclass(cls, Weight):
        raise TypeError("'cls' must be subclass of 'yatel.weight.Weight'")
    for name in names:
        _weights[name] = cls


def calculators():
    return _weights.keys()


def weight_calculator(name):
    return _weights[name]


def weight(calcname, hap0, hap1):
    cls = _weights[calcname]
    calculator = cls()
    return calculator.weight(hap0, hap1)


def weights(calcname, nw, to_same=False, env=None, **kwargs):
    cls = _weights[calcname]
    calculator = cls()
    return calculator.weights(nw=nw, to_same=to_same, env=env, **kwargs)


#===============================================================================
# REGISTERS!
#===============================================================================

from yatel.weight import hamming
register(hamming.Hamming, "hamming", "ham")


from yatel.weight import euclidean
register(euclidean.Euclidean, "euclidean", "euc", "ordinary")


from yatel.weight import levenshtein
register(levenshtein.Levenshtein, "levenshtein", "lev")
register(levenshtein.DamerauLevenshtein, "dameraulevenshtein", "damlev",
         "damerau-levenshtein")


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
