#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# DOCS
#===============================================================================

"""The Yatel kmeans algorithm clusters a network's environments generated by
a set of filters (attributes of facts), using as dimensions the haplotypes
which exists in each environment or arbitrary values computed over them.

For more information about kmeans:

    - `Scipy Doc <http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans.html>`_
    - `KMeans in wikipedia <http://en.wikipedia.org/wiki/K-means_clustering>`_

"""

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

def kmeans(nw, fact_attrs, k_or_guess,
           whiten=False, coordc=None, *args, **kwargs):
    """Performs k-means on a set of all enviroments defined by ``fact_attrs``
    of a network.

    :param nw: Network source of enviroments to classify.
    :type nw: yatel.db.YatelNetwork
    :param fact_attrs: A collection of fact attributes names existing in ``nw``.
                       which generates all posible combinations of values of
                       the given attributes.
    :type fact_attrs: iterable os strings
    :param k_or_guess: The number of centroids to generate. A code is assigned
                       to each centroid, which is also the row index of the
                       centroid in the code_book matrix generated.

                       The initial k centroids are chosen by randomly
                       selecting observations from the observation matrix.
                       Alternatively, passing a k by N array specifies the
                       initial k centroids.
    :type k_or_guess: int or ndarray
    :param whiten: execute ``scipy.cluster.vq.whiten`` function over the
                   observation array before executing subjacent *scipy kmeans*.
    :type whiten: bool
    :param coordc: If coordc is None generates the coordinates for the algorithm
                   with the haplotypes which exists in each environment.
                   Otherwise ``coordc`` must be a callable with 2 arguments:

                        - ``nw`` network source of enviroments to classify.
                        - ``env`` the enviroment to calculate the coordinates

                   and must must return an array of coordinates for the given
                   network enviroment.
    :type coordc: None or callable
    :param args: arguments for scipy kmeans
    :param kwargs: keywords arguments for scipy kmeans

    :returns: Three objects are returned:

                - ``coodebook``: A k by N array of k centroids. The i’th
                                 centroid codebook[i] is represented with the
                                 code i.
                                 The centroids and codes generated represent
                                 the lowest distortion seen, not necessarily
                                 the globally minimal distortion.
                - ``distortion``: The distortion between the observations
                                  passed and the centroids generated.
                - ``clustenv``: An array with the same length as ``coodebook``.
                                The i'th element of ``clustenv`` contains all
                                the enviroments of the i'th centroid of
                                coodebook

    **Example**

    >>> from yatel import nw
    >>> from yatel.cluster import kmeans
    >>> nw = db.YatelNetwork('memory', mode=db.MODE_WRITE)
    >>> nw.add_elements([dom.Haplotype(1), dom.Haplotype(2), dom.Haplotype(3)])
    >>> nw.add_elements([dom.Fact(1, att0=True, att1=4),
    ...                  dom.Fact(2, att0=False),
    ...                  dom.Fact(2, att0=True, att2="foo")])
    >>> nw.add_elements([dom.Edge(12, 1, 2),
    ...                  dom.Edge(34, 2, 3),
    ...                  dom.Edge(1.25, 3, 1)])
    >>> nw.confirm_changes()
    >>> kmeans.kmeans(nw, ["att0", "att2"], 2)
    (array([[1, 0, 0],
           [0, 1, 0]]),
     0.0,
     (({u'att0': True, u'att2': None},),
      ({u'att0': False, u'att2': None}, {u'att0': True, u'att2': u'foo'})))

    >>> calc = lambda nw, env: [stats.average(nw, env), stats.std(nw, env)]
    >>> kmeans.kmeans(nw, ["att0", "att2"], 2, coordc=calc)
    (array([[ 23.   ,  11.   ],
           [  6.625,   5.375]]),
     0.0,
     (({u'att0': False, u'att2': None}, {u'att0': True, u'att2': u'foo'}),
      ({u'att0': True, u'att2': None},)))

    """
    obs, envs = nw2obs(nw, fact_attrs, coordc=coordc)
    codebook, distortion = vq.kmeans(obs=obs, k_or_guess=k_or_guess,
                                     *args, **kwargs)
    clustenv = cluster_enviroments(envs, obs, codebook)
    return codebook, distortion, clustenv


#===============================================================================
# SUPPORT
#===============================================================================

def nw2obs(nw, fact_attrs, whiten=False, coordc=None):
    """Convert a given enviroments defined by ``fact_attrs``
    of a network to observation matrix to cluster with subjacent *scipy kmeans*

    :param nw: Network source of enviroments to classify.
    :type nw: yatel.db.YatelNetwork
    :param fact_attrs: A collection of fact attributes names existing in ``nw``.
                       which generates all posible combinations of values of
                       the given attributes.
    :type fact_attrs: iterable os strings
    :param whiten: execute ``scipy.cluster.vq.whiten`` function over the
                   observation array before executing subjacent *scipy kmeans*.
    :type whiten: bool
    :param coordc: If coordc is None generates the coordinates for the algorithm
                   with the haplotypes which exists in each environment.
                   Otherwise ``coordc`` must be a callable with 2 arguments:

                        - ``nw`` network source of enviroments to classify.
                        - ``env`` the enviroment to calculate the coordinates

                   and must must return an array of coordinates for the given
                   network enviroment.
    :type coordc: None or callable

    :returns: Two objects are returned:

                - ``obs``: Each I'th row of the M by N array is an observation
                           vector of the I'th enviroment of ``envs``.
                - ``envs``: M array of all posible enviroments of the ``nw``
                            by the given ``facts_attrs``

    **Example**

    >>> from yatel import nw
    >>> from yatel.cluster import kmeans
    >>> nw = db.YatelNetwork('memory', mode=db.MODE_WRITE)
    >>> nw.add_elements([dom.Haplotype(1), dom.Haplotype(2), dom.Haplotype(3)])
    >>> nw.add_elements([dom.Fact(1, att0=True, att1=4),
    ...                  dom.Fact(2, att0=False),
    ...                  dom.Fact(2, att0=True, att2="foo")])
    >>> nw.add_elements([dom.Edge(12, 1, 2),
    ...                  dom.Edge(34, 2, 3),
    ...                  dom.Edge(1.25, 3, 1)])
    >>> nw.confirm_changes()
    >>> kmeans.nw2obs(nw, ["att0", "att2"])
    (array([[1, 0, 0],
        [0, 1, 0],
        [0, 1, 0]]),
     ({u'att0': True, u'att2': None},
      {u'att0': False, u'att2': None},
      {u'att0': True, u'att2': u'foo'}))

    """
    if not isinstance(nw, db.YatelNetwork):
        msg = "nw must be 'yatel.db.YatelNetwork' instance"
        raise TypeError(ms)
    haps_id = None
    if coordc is None:
        haps_id = tuple(nw.haplotypes_ids())
    envs = tuple(nw.enviroments_iterator(fact_attrs))
    mtx = []
    for idx, env in enumerate(envs):
        row = None
        if coordc is None:
            ehid = tuple(nw.haplotypes_ids_enviroment(env=env))
            row = [int(hid in ehid) for hid in haps_id]
        else:
            row = coordc(nw, env)
        mtx.append(row)
    obs = np.array(mtx)
    if whiten:
        obs = vq.whiten(obs)
    return obs, envs


def cluster_enviroments(envs, obs, codebook):
    """Sort a collection of enviroment by the minimun distance of their
    observation coordinates to the codebook centroids.

    :params envs: M array of all posible enviroments of the ``nw``
                  by the given ``facts_attrs``.
    :type envs: collection of dict
    :param obs: Each I'th row of the M by N array is an observation
                vector of the I'th enviroment of ``envs``
    :param coodebook: K by N Array of centroids of clusters.

    :returns: An array with the same length as ``coodebook``.
              The i'th element of ``clustenv`` contains all
              the enviroments of the i'th centroid of coodebook

    """
    clustenv = [[] for _ in codebook]
    for idx, env in enumerate(envs):
        env_coords = obs[idx]
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
