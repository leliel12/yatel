#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#==============================================================================
# DOCS
#==============================================================================

"""Base classes for weight calculation in yatel

"""

#==============================================================================
# IMPORTS
#==============================================================================

import abc
import itertools

from yatel import db


#==============================================================================
# BASE CLASS
#==============================================================================

class BaseWeight(object):
    """Base class of all weight calculators"""

    __metaclass__ = abc.ABCMeta

    @classmethod
    def names(cls):
        raise NotImplementedError()

    def weights(self, nw, to_same=False, env=None, **kwargs):
        """Calculate distance between all combinations of a existing haplotypes
        of network enviroment or a collection

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
                  the origin node, hap_y is the end node and float is the
                  weight of between them.

        """
        env = dict(env) if env else {}
        env.update(kwargs)

        haps = None
        if isinstance(nw, db.YatelNetwork):
            haps = (
                nw.haplotypes_by_environment(env) if env else nw.haplotypes()
            )
        elif env:
            msg = (
                "If nw is not instance of yatel.db.YatelNetwork, "
                "env and kwargs must be empty"
            )
            raise ValueError(msg)
        else:
            haps = nw

        comb = (
            itertools.combinations_with_replacement
            if to_same else
            itertools.combinations
        )
        for hap0, hap1 in comb(haps, 2):
            yield (hap0, hap1), self.weight(hap0, hap1)

    @abc.abstractmethod
    def weight(self, hap0, hap1):
        """**Not implemented:** A ``float`` distance
           between 2 ``dom.Haplotype`` instances

        """
        raise NotImplementedError()


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
