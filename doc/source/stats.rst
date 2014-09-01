Stats
=====

The statistics module is one of the fundamental parts of Yatel. It's
designed to support decision making through extraction of measure of 
positions, variation, skewness and peak analysis of arc weights in a given 
environment.

The features of this module are divided into 2 distinct groups:

- Transformation Functions: Is responsible for converting an environment of
  a given network into a *numpy array* to accelerate the calculation 
  of statistics.
- Calculation Functions: Are used for calculating statistical measures
  on a haplotypes environment.

While all calculation functions use internally the transformation functions, 
it is often critical to the performance of processing to precalculate in an 
array with the values ​​of the distances of an environment.


Transformation Functions
------------------------

The transformation functions are two:

- ``weights2array``: given a ``dom.Edges`` iterable this function returns a 
  ``numpy.ndarray`` with all weight values ​​of said arcs.

.. code-block:: python

    >>> from yatel import dom, db, stats

    # Our classic network example
    >>> nw = db.YatelNetwork("memory", mode="w")

    >>> nw.add_elements([
    ...     dom.Haplotype(0, name="Cordoba", clima="calor", edad=200, frio=True), # left
    ...     dom.Haplotype(1, name="Cordoba", poblacion=12), # right
    ...     dom.Haplotype(2, name="Cordoba"), # bottom

    ...     dom.Edge(6599, (0, 1)),
    ...     dom.Edge(8924, (1, 2)),
    ...     dom.Edge(9871, (2, 0)),

    ...     dom.Fact(0, name="Andalucia", lang="sp", timezone="utc-3"),
    ...     dom.Fact(1, lang="sp"),
    ...     dom.Fact(1, timezone="utc-6"),
    ...     dom.Fact(2, name="Andalucia", lang="sp", timezone="utc")
    ... ])
    ... nw.confirm_changes()

    # we extract all edges
    edges = nw.edges()
    stats.weights2array(edges)
    array([ 6599.,  8924.,  9871.])


- ``env2weightarray``: This function is responsible for converting a 
  ``db.YatelNetwork`` instance into an array with all weights of the edges 
  contained; or any of them filtered by environments. Also for reasons of 
  implementations can receive any iterable and turn it into a numpy array.


.. code-block:: python

    >>> stats.env2weightarray(nw)
    array([ 6599.,  8924.,  9871.])

    # with an environment
    >>> stats.env2weightarray(nw, name="Andalucia")
    array([ 9871.])


Calculation Functions
---------------------

Calculation functions are responsible for efficiently calculating statistics 
on the variability of a network or a network environment.
The full list of functions can be found on the reference module :py:mod:`yatel.stats`

.. code-block:: python

    # we could calculate for example, the mean (or average) in a network
    >>> stats.average(nw)
    8464.666666666666667

    # or in a environment
    >>> stats.average(nw, name="Andalucia")
    9871.0


For performance reasons is desirable to calculate all weights from an 
environment before before making many calculations (this can speed up to 
several hundred times the data analysis)

.. code-block:: python

    # we get the array with it's values
    >>> arr = stats.env2weightarray(nw, lang="sp")

    # calculate the deviation
    >>> stats.std(arr)
    1374.7087772405551286


The functions also support python iterables such as lists or tuples

.. code-block:: python

    >>> stats.average([1, 2, 3])
    0.81649658092772603

    # this wont return a number
    >>> stats.average([])
    nan


A More Advanced Example
-----------------------

While Yatel provides for the calculation of common statistics, ``stats`` 
module for its architecture facilitates data analysis of more complex 
environments easily integrating itself with the functionality of SciPy_.

For example if we wanted to calculate
`One-Way ANOVA <http://en.wikipedia.org/wiki/Analysis_of_variance>`_ with two 
environments of our network.

.. code-block:: python

    # import the one-way ANOVA
    >>> from scipy.stats import f_oneway

    # first sample
    >>> arr0 = stats.env2weightarray(nw, lang="sp")

    # second sample
    >>> arr1 = stats.env2weightarray(nw, name="Andalucia")

    >>> f, p = f_oneway(arr0, arr1)

    # value of F
    >>> f
    0.5232691541329888

    # value of P
    >>> p
    0.54461284339730176


