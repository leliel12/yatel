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

from yatel.tests import (
    core,
    test_db,
    test_dom,
    test_db,
    test_dom,
    test_stats,
    test_typeconv,
    test_qbj,
    test_cluster,
    test_yio,
    test_weight,
    test_server,
    test_client,
    test_etl,
    test_extra_dbs
)


#===============================================================================
# FUNCTIONS
#===============================================================================

def collect_modules():
    def collect(basecls):
        collected = set()
        for testcls in basecls.subclasses():
            collected.add(testcls)
            collected.update(collect(testcls))
        return collected

    modules = {}
    for testcls in collect(core.YatelTestCase):
        modname = testcls.__module__.rsplit(".", 1)[-1].replace("test_", "", 1)
        if modname not in modules:
            modules[modname] = set()
        modules[modname].add(testcls)
    return modules


def run_tests(verbosity=1, modules=None, failfast=False, extra_dbs=None):

    if extra_dbs:
        test_extra_dbs.create_test_for(extra_dbs)

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    runner = unittest.runner.TextTestRunner(
        verbosity=verbosity, failfast=failfast
    )
    for modname, testcases in collect_modules().items():
        if not modules or modname in modules:
            for testcase in testcases:
                tests = loader.loadTestsFromTestCase(testcase)
                if tests.countTestCases():
                        suite.addTests(tests)
    return runner.run(suite)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
