#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.

import sys


NOT_CLASS = ("EDir", )

class Mock(object):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super(Mock, self).__new__(cls)

    def __init__(self, *args, **kwargs):
            pass

    def __call__(self, *args, **kwargs):
        return Mock()

    def __getattribute__(cls, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        elif name[0] == name[0].upper() and name not in NOT_CLASS:
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        else:
            return Mock()

MOCK_MODULES = ("graph_tool", "PyQt4", "numpy",  "QtCore2", "QtGui", "sip", "pycante")
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()
