#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This package contains several modules and functions for calculatte
distances between haplotypes.

Esentially contains some of knowed algorithms for calculate distances betwwen
elements that can be used as edge weights.

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
    """Register a new weight calculator for yatel.

    :param cls: Tha calculator class
    :type nw: yatel.weight.Weight subclass
    :param names: list of string for identify the calcularor

    **Example**

    >>> from yatel import weight
    >>>
    >>> Class MyHyperSuperCalculator(weight.Weight):
    ...     def weight(self, hap0, hap1):
    ...         return some_operation(hap0, hap1)
    >>>
    >>> weight.register(MyHyperSuperCalculator,
    ...                 "my_hyper_super_calculator", "mhsc")
    >>>
    >>> weight.calculator("my_hyper_super_calculator")
    __main__.MyHyperSuperCalculator
    >>> weight.calculator("mhsc")
    __main__.MyHyperSuperCalculator

    """
    if not inspect.isclass(cls) or not issubclass(cls, Weight):
        raise TypeError("'cls' must be subclass of 'yatel.weight.Weight'")
    for name in names:
        if not isinstance(name, basestring):
            msg = "'name' must be a string instance"
            raise TypeError(msg)
        _weights[name] = cls


def calculators():
    """Returns a list with all registered calculators

    :returns: list of strings of registered calculator names

    """
    return _weights.keys()


def calculator(name):
    """Return a calculator class for a given calculator name

    :return: ``yatel.weight.Weight`` subclass

    """
    return _weights[name]


def weight(calcname, hap0, hap1):
    """Calculate the a weight between ``yatel.dom.Haplotype`` instance by the
    given calculator

    :param calcname: Registered calculator name (see:
                     ``yatel.weight.calculators``)
    :type calcname: string
    :param hap0: an Haplotype
    :type hap0: yatel.dom.Haplotype
    :param hap1: an Haplotype
    :type hap1: yatel.dom.Haplotype

    **Example**

    >>> from yatel import dom, weight
    >>> hap0 = dom.Haplotype(1, att0="foo", att1=34)
    >>> hap1 = dom.Haplotype(2, att1=65)
    >>> weight.weight("hamming", hap0, hap1)
    2

    """

    cls = _weights[calcname]
    calculator = cls()
    return calculator.weight(hap0, hap1)


def weights(calcname, nw, to_same=False, env=None, **kwargs):
    """Calculate distance between all combinations of a existing haplotypes
    of network enviroment or a collection by the given calculator algorithm.

    :param calcname: Registered calculator name (see:
                     ``yatel.weight.calculators``)
    :type calcname: string
    :param nw: ``yatel.db.YatelNetwork`` instance or iterable of
               ``yatel.dom.Haplotype`` instances
    :param to_same: If ``True` `calculate the distance between the same
                    haplotype.
    :type to_dame: bool
    :param env: enviroment dictionary only if nw is
                ``yatel.db.YatelNetwork`` instance.
    :type env: None or dict
    :param kwargs: Variable parameters for use as enviroment filter only
                   if nw is ``yatel.db.YatelNetwork`` instance.

    :returns: A iterator like like ``(hap_x, hap_y), float`` where hap_x is
                  the origin node, hap_y is the end node and float is the weight
                  of between them.

    **Example**

    >>> from yatel import db, dom, weight
    >>> nw = db.YatelNetwork('memory', mode=db.MODE_WRITE)
    >>> nw.add_elements([dom.Haplotype(1, att0="foo", att1=34),
    ...                  dom.Haplotype(2, att1=65),
    ...                  dom.Haplotype(3)])
    >>> nw.add_elements([dom.Fact(1, att0=True, att1=4),
    ...                  dom.Fact(2, att0=False),
    ...                  dom.Fact(2, att0=True, att2="foo")])
    >>> nw.add_elements([dom.Edge(12, 1, 2),
    ...                  dom.Edge(34, 2, 3)])
    >>> nw.confirm_changes()

    >>> dict(weight.weights("lev", nw))
    {(<Haplotype '1' at 0x2823c10>, <Haplotype '2' at 0x2823c50>): 5,
     (<Haplotype '1' at 0x2823c10>, <Haplotype '3' at 0x2823d50>): 7,
     (<Haplotype '2' at 0x2823c50>, <Haplotype '3' at 0x2823d50>): 4}

    >>> dict(weight.weights("ham", nw, to_same=True, att0=False))
    {(<Haplotype '2' at 0x1486c90>, <Haplotype '2' at 0x1486c90>): 0}

    """
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
