#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This module is used for calculate weights of edges in yatel.

Esentially contains some of knowed algorithms for calculate distances betwwen
elements that can be used as edge weights.

"""

#===============================================================================
# IMPORTS
#===============================================================================

import itertools

import numpy


#===============================================================================
# ERROR
#===============================================================================

class AbstractWeight(object):
    """Base class of all weight calculators"""

    def __call__(self, haps=[], repeated=False):
        return self.weights(haps=haps, repeated=repeated)

    def weights(self, haps=[], repeated=False):
        """Calculate distance between all combinations of acollection of
        haplotypes.

        **Params**
            :haps: A iterable of ``dom.Haplotype`` instances.
            :repeated: If calculate the distance between the same haplotype.

        **Return**
            A ``dict`` like ``{(hap_x, hap_y) : float}``

        """
        ws = {}
        comb = itertools.combinations_with_replacement \
               if repeated else itertools.combinations
        for hap0, hap1 in comb(haps, 2):
            ws[(hap0, hap1)] = self.weight(hap0, hap1)
        return ws

    def weight(self, hap0, hap1):
        """A ``float`` distance between 2 ``dom.Haplotype`` instances"""
        raise NotImplementedError()


#===============================================================================
# HAMMING
#===============================================================================

class Hamming(AbstractWeight):
    """Calculate the hamming distances between two haplotypes, by counting
    the number of diferences in attributes.

    The distances is incremented by "1" by two reasons:
        #. haplotype0.attr_a != haplotype1.attr_a
        #. attr_a exist in haplotype0 but not exist in haplotype1.

    example

        ::

            >>> from yatel import dom, weigth
            >>> h0 = dom.Haplotype("0", attr_a="a", attr_b="b", attr_c=0)
            >>> h1 = dom.Haplotype("1", attr_a="a", attr_c="0")
            >>> hamming = weight.Hamming()
            >>> print  hamming(h0, h1)
            {(<haplotype0>, <haplotype1>): 2.0}


    """

    def weight(self, hap0, hap1):
        """A ``float`` distance between 2 ``dom.Haplotype`` instances"""
        w = 0
        for name in set(hap0.names_attrs() + hap1.names_attrs()):
            if name not in hap0.names_attrs() \
               or name not in hap1.names_attrs() \
               or hap0.get_attr(name) != hap1.get_attr(name):
                w += 1
        return w


#===============================================================================
# EXPERT
#===============================================================================

def Expert(AbstractWeight):
    """This calculator receives in the constructor a precalculated weights
    and return these values ​​when is requested or None if no weight

    """

    def __init__(self, *weights):
        """Create a new instance

        **Params**
            :weights: A iterable with 2 haplotypes and 1 weight in every item

        """
        self._ws = {}
        for h0, h1, w in weights:
            self._ws[(h0, h1)] = w

    def weight(self, hap0, hap1):
        """A ``float`` distance between 2 ``dom.Haplotype`` instances"""
        return self._ws.get((hap0, hap1))


#===============================================================================
# EUCLIDEAN
#===============================================================================

class Euclidean(AbstractWeight):
    """Calculate "ordinary" distance/weight between two haplotypesm given by the
    Pythagorean formula.

    Every attribute value is converted to a number by a ``to_num`` function.
    The default behavior of ``to_num`` is a sumatory of base64 ord value of
    every attribute value or

    .. code-block:: python

        def to_num(attr):
            value = 0
            for c in str(attr).encode("base64"):
                value += ord(c)
            return value

        to_num("h") # 294

    """
    def __init__(self, to_num=None):
        """Creates a new instance

        **Params**
            :to_num: Convert to a number an haplotype attribute number.
                     The default behavior of ``to_num`` is a sumatory of
                     base64 ord value of every attribute value or

                    .. code-block:: python

                        def to_num(attr):
                            value = 0
                            for c in str(attr).encode("base64"):
                                value += ord(c)
                            return value

                        to_num("h") # 294

        """
        def to_num_default(attr):
            value = 0
            for c in str(attr).encode("base64"):
                value += ord(c)
            return value

        self.to_num = to_num_default if to_num is None else to_num

    def weight(self, hap0, hap1):
        """A ``float`` distance between 2 ``dom.Haplotype`` instances"""

        s = 0.0
        for name in set(hap0.names_attrs() + hap1.names_attrs()):
            v0 = self.to_num(hap0.get_attr(name, ""))
            v1 = self.to_num(hap1.get_attr(name, ""))
            s += (v1 - v0) ** 2
        return numpy.sqrt(s)


#===============================================================================
# LEVENSHTEIN
#===============================================================================

class Levenshtein(AbstractWeight):
    """The Levenshtein distance between two haplotypes is defined as the minimum
    number of edits needed to transform one haplotype as squence (sumatory of
    attribute values) into the other, with the  allowable edit operations
    being insertion, deletion, or substitution of a single character

    Note: Previously the haplotypes attribute values are *base64* endoced
    """

    def weight(self, hap0, hap1):
        """A ``float`` distance between 2 ``dom.Haplotype`` instances"""

        def levenshtein(a, b):
            """Calculates the Levenshtein distance between a and b.

            Found at: http://hetland.org/coding/
            """
            n, m = len(a), len(b)
            if n > m:
                # Make sure n <= m, to use O(min(n,m)) space
                a, b = b, a
                n, m = m, n
            current = range(n + 1)
            for i in range(1, m + 1):
                previous, current = current, [i] + [0] * n
                for j in range(1, n + 1):
                    add, delete = previous[j] + 1, current[j - 1] + 1
                    change = previous[j - 1]
                    if a[j - 1] != b[i - 1]:
                        change = change + 1
                    current[j] = min(add, delete, change)
            return current[n]

        values = []
        for name in sorted(set(hap0.names_attrs() + hap1.names_attrs())):
            as0 = str(hap0.get_attr(name, "")).encode("base64")
            as1 = str(hap1.get_attr(name, "")).encode("base64")
            values.append(levenshtein(as0, as1))
        return sum(values)


#===============================================================================
# DAMERAU-LEVENSHTEIN
#===============================================================================

class DamerauLevenshtein(AbstractWeight):
    """Calculate the Damerau-Levenshtein distance between haplotypes.

    This distance is the number of additions, deletions, substitutions,
    and transpositions needed to transform the first haplotypes as sequences
    into the second.

    Transpositions are exchanges of *consecutive* characters; all other
    operations are self-explanatory.

    This implementation is O(N*M) time and O(M) space, for N and M the
    lengths of the two sequences.

    Note: Previously the haplotypes attribute values are *base64* endoced

    """

    def weight(self, hap0, hap1):
        """A ``float`` distance between 2 ``dom.Haplotype`` instances"""

        def dameraulevenshtein(seq1, seq2):
            """This is the original code found in:

            http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance/

            The code is available under the MIT licence, in the hope that it
            will be useful, but without warranty of any kind. I have also
            included a codesnippet  GUID in line with the linked post, as a sort
            of experiment. Please leave that comment intact if you’re
            posting a derivative somewhere, and add your own.

            """
            # codesnippet:D0DE4716-B6E6-4161-9219-2903BF8F547F
            # Conceptually, this is based on a len(seq1) + 1 * len(seq2) + 1
            # matrix.
            # However, only the current and two previous rows are needed at once,
            # so we only store those.
            oneago = None
            thisrow = range(1, len(seq2) + 1) + [0]
            for x in xrange(len(seq1)):
                # Python lists wrap around for negative indices, so put the
                # leftmost column at the *end* of the list. This matches with
                # the zero-indexed strings and saves extra calculation.
                twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
                for y in xrange(len(seq2)):
                    delcost = oneago[y] + 1
                    addcost = thisrow[y - 1] + 1
                    subcost = oneago[y - 1] + (seq1[x] != seq2[y])
                    thisrow[y] = min(delcost, addcost, subcost)
                    # This block deals with transpositions
                    if (x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                        and seq1[x - 1] == seq2[y] and seq1[x] != seq2[y]):
                        thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)
            return thisrow[len(seq2) - 1]

        values = []
        for name in sorted(set(hap0.names_attrs() + hap1.names_attrs())):
            as0 = str(hap0.get_attr(name, "")).encode("base64")
            as1 = str(hap1.get_attr(name, "")).encode("base64")
            values.append(dameraulevenshtein(as0, as1))
        return sum(values)

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)






