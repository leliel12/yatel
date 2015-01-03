#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#==============================================================================
# DOCS
#==============================================================================

"""Statistic functions to calculate network statistics over YatelNetwork
environments.


"""

#==============================================================================
# IMPORT
#==============================================================================

import numpy as np


# =============================================================================
# NETWORK STATISTICS
# =============================================================================

def haplotypesfreq(nw, env=None, **kwargs):
    """Calculates a frequency of an haplotype of a given enviroment.

    Every *enviroment* is defined for a set of *facts*, every *fact* has only
    one *haplotype*. This method count how many facts has the same hap_id.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    Returns
    -------
    haps_ids : An array of k haps_ids present on this enviroment
        A list of haps ids inside the given enviroment.
    cnt : An array of k counte
         The cnt[i] has the frequency of haps_ids[i]

    """
    facts = (
        nw.facts_by_environment(env=env, **kwargs)
        if (env or kwargs) else nw.facts()
    )
    haps_ids, cnt = np.unique(facts.attrs(["hap_id"]), return_counts=True)
    return haps_ids, cnt


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(__doc__)
