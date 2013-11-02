#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#===============================================================================
# DOC
#===============================================================================

"""All yatel tests"""


#===============================================================================
# IMPORTS
#===============================================================================

from yatel.tests import core


#===============================================================================
# BASE CLASS
#===============================================================================

class FunctionsTestCase(core.YatelTestCase):

    def test_wrap_network(self):
        print self.nw



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
