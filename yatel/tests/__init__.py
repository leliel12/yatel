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

import unittest

from yatel.tests import core,  test_db, test_dom, test_typeconv, test_qbj


#===============================================================================
# FUNCTIONS
#===============================================================================

def run_tests(verbosity=1):
    loader = unittest.TestLoader()
    runner = unittest.runner.TextTestRunner(verbosity=verbosity)
    for testcase in core.YatelTestCase.subclasses():
        for test_suite in loader.loadTestsFromTestCase(testcase):
            if test_suite.countTestCases():
                runner.run(test_suite)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
