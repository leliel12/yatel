#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


# =============================================================================
# DOC
# =============================================================================

"""yatel.nwstats module tests"""


# =============================================================================
# IMPORTS
# =============================================================================

import collections
import warnings

import numpy as np

from yatel import nwstats
from yatel.tests.core import YatelTestCase


# =============================================================================
# VALIDATE TESTS
# =============================================================================

class TestNWStats(YatelTestCase):

    def test_haplotypesfreq(self):
        enviroments = list(self.nw.environments()) + [None]
        for env in enviroments:
            haps_ids = collections.defaultdict(int)
            for fact in self.nw.facts_by_environment(env):
                haps_ids[fact.hap_id] += 1
            haps, cnts = nwstats.haplotypesfreq(self.nw, env)
            self.assertTrue(len(haps) == len(cnts) == len(haps_ids))
            for idx, hap_id in enumerate(haps):
                cnt = cnts[idx]
                self.assertEqual(haps_ids[hap_id], cnt)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(__doc__)
