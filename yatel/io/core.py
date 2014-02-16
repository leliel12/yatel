#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# DOC
#===============================================================================

"""Base structure for yatel parsers"""


#===============================================================================
# IMPORTS
#===============================================================================

import abc


#===============================================================================
# CONSTANTS
#===============================================================================

YF_VERSION = ("0", "5")
YF_STR_VERSION = ".".join(YF_VERSION)


#===============================================================================
# CLASS
#===============================================================================

class BaseParser(object):

    __metaclass__ = abc.ABCMeta

    @classmethod
    def version(cls):
        return YF_STR_VERSION

    @classmethod
    def file_exts(cls):
        raise NotImplementedError()

    def dumps(self, nw, *args, **kwargs):
        fp = StringIO.StringIO()
        self.dump(nw, fp, *args, **kwargs)
        return fp.getvalue()

    def loads(self, nw, string, *args, **kwargs):
        fp = StringIO.StringIO(string)
        self.loads(nw, fp, *args, **kwargs)

    @abc.abstractmethod
    def dump(self, nw, fp, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def load(self, nw, fp, *args, **kwargs):
        raise NotImplementedError()

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
