#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Core structures for yatel ETL's

"""


#===============================================================================
# INSPECT
#===============================================================================

import inspect
import abc


#===============================================================================
# META CLASSES
#===============================================================================

class _ETLMeta(abc.ABCMeta):

    def __init__(self, *args, **kwargs):
        super(_ETLMeta, self).__init__(*args, **kwargs)
        spec = inspect.getargspec(self.setup)
        if spec.varargs or spec.keywords or spec.defaults:
            msg = "Only positional arguments without defauls is alowed on setup"
            raise TypeError(msg)
        self.setup_args = tuple(arg for arg in spec.args if arg != "self")


#===============================================================================
# CLASSES
#===============================================================================

class ETL(object):

    __metaclass__ = _ETLMeta

    def setup(self):
        pass

    def pre_haplotype_gen(self):
        pass

    @abc.abstractmethod
    def haplotype_gen(self):
        return []

    def post_haplotype_gen(self):
        pass

    def pre_fact_gen(self):
        pass

    @abc.abstractmethod
    def fact_gen(self):
        return []

    def post_fact_gen(self):
        pass

    def pre_edge_gen(self):
        pass

    @abc.abstractmethod
    def edge_gen(self):
        return []

    def post_edge_gen(self):
        pass

    def teardown(self):
        pass


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

