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
        for env in self.nw.environments():
            haps, cnt = nwstats.haplotypesfreq(self.nw, env)


# ===============================================================================
# MAIN
# ===============================================================================

if __name__ == "__main__":
    print(__doc__)
