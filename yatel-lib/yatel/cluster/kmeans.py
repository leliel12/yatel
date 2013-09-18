#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <jbc.develop@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a WISKEY in return Juan BC


#===============================================================================
# DOCS
#===============================================================================

""""""

#===============================================================================
# IMPORTS
#===============================================================================

import numpy as np
from scipy.spatial import distance
from scipy.cluster import vq

from yatel import db


#===============================================================================
# KMEANS
#===============================================================================

def kmeans(nw, fact_attrs, k_or_guess, repeated=True, *args, **kwargs):
    envs, obs, ref = nw2obs(nw, fact_attrs, repeated=repeated)
    codebook, distortion = vq.kmeans(obs=obs, k_or_guess=k_or_guess,
                                     *args, **kwargs)
    clustenv = cluster_enviroments(envs, obs, ref, codebook)
    return codebook, distortion, clustenv


#===============================================================================
# SUPPORT
#===============================================================================

def nw2obs(nw, fact_attrs, repeated=True):
    if not isinstance(nw, db.YatelNetwork):
        msg = "nw must be 'yatel.db.YatelNetwork' instance"
        raise TypeError(ms)
    haps_id = tuple(nw.haplotypes_ids())
    envs = tuple(nw.enviroments_iterator(fact_attrs))
    mtx = []
    ref = []
    for idx, env in enumerate(envs):
        ehid = tuple(nw.haplotypes_ids_enviroment(env=env))
        row = [int(hid in ehid) for hid in haps_id]

        if repeated:
            mtx.append(row)
            ref.append(idx)
        else:
            if row not in mtx:
                mtx.append(row)
            ref.append(mtx.index(row))

    return envs, np.array(mtx), ref


def cluster_enviroments(envs, obs, ref, codebook):
    clustenv = [[] for _ in codebook]
    for idx, env in enumerate(envs):
        ridx = ref[idx]
        env_coords = obs[ridx]
        min_cluster = None
        for cluster, centroid in enumerate(codebook):
            dist = distance.euclidean(env_coords, centroid)
            if min_cluster is None or min_cluster[1] > dist:
                min_cluster = (cluster, dist)
        clustenv[min_cluster[0]].append(env)
    return tuple(map(tuple, clustenv))


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
