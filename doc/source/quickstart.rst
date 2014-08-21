Quick Start
===========

What is Yatel?
--------------

It's a reference implementation of NW-OLAP

- Wiskey-Ware License
- It is largely implementing the aforementioned process.
- Soon to arrive it's first usable version 0.3

`Read more <http://getyatel.org/>`_



Case study (example)
--------------------

Suppose we have the following problem:

.. graph:: Example

    ar [label="Córdoba"];
    mx [label="Córdoba"];
    sp [label="Córdoba"];

    ar -- mx [label="6599"];
    mx -- sp [label="8924"];
    sp -- ar [label="9871"];


We have three places called Cordoba [0]_ [1]_ [2]_, each separated one from the other
by a certain distance. We can use Yatel to state the
problem and make queries:

- Which ones have an area between 200km2 and 600km2?
- Which ones speak Spanish?
- Those with the time zone utc-6?
- Who has in his name Andalucía?

Loading problem into Yatel
--------------------------

We load the previous model into Yatel, as follows:

.. code-block:: python

    >>> from yatel import dom, db
    >>> from pprint import pprint
    # postgres, oracle, mysql, and many more
    >>> nw = db.YatelNetwork("memory", mode="w")
    >>> elems = [
    ...    dom.Haplotype(0, name="Cordoba"), # left
    ...    dom.Haplotype(1, name="Cordoba"), # right
    ...    dom.Haplotype(2, name="Cordoba"), # bottom
    ...
    ...    dom.Edge(6599, (0, 1)),
    ...    dom.Edge(8924, (1, 2)),
    ...    dom.Edge(9871, (2, 0)),
    ...
    ...    dom.Fact(0,name="Andalucia", lang="sp", timezone="utc-3"),
    ...    dom.Fact(1, lang="sp"),
    ...    dom.Fact(1, timezone="utc-6"),
    ...    dom.Fact(2, name="Andalucia", lang="sp", timezone="utc"),
    ... ]
    >>> nw.add_elements(elems)
    >>> nw.confirm_changes()

In the above code, we create a database in memory and define:

- A haplotype for each Córdoba.
- An edge to match each Córdoba by a distance.
- Facts that give us information about the haplotypes.


Models and Attributes
^^^^^^^^^^^^^^^^^^^^^

Showing the description

.. code-block:: python

    >>> descriptor =  nw.describe()
    >>> pprint(dict(descriptor))
    {'edge_attributes': {u'max_nodes': 2, u'weight': <type 'float'>},
     'fact_attributes': {'hap_id': <type 'int'>,
                         'lang': <type 'str'>,
                         'name': <type 'str'>,
                         'timezone': <type 'str'>},
     'haplotype_attributes': {'hap_id': <type 'int'>, 'name': <type 'str'>},
     'mode': 'r',
     'size': {u'edges': 3, u'facts': 4, u'haplotypes': 3}
    }


Showing Haplotypes:

.. code-block:: python

    >>> for hap in nw.haplotypes():
    ...     print hap
    <Haplotype (0) at 0x24faa50>
    <Haplotype (1) at 0x24eae50>
    <Haplotype (2) at 0x24fa990>


Showing Edges:

.. code-block:: python

    >>> for edge in nw.edges():
    ...     print edge
    <Edge ([6599.0 [0, 1]]  ) at 0x1f64c50>
    <Edge ([8924.0 [1, 2]]  ) at 0x24fa0d0>
    <Edge ([9871.0 [2, 0]]  ) at 0x1f64c50>


Showing Facts:

.. code-block:: python

    >>> for fact in nw.facts():
    ...     print fact
    <Fact (of Haplotype '0') at 0x24eae50>
    <Fact (of Haplotype '1') at 0x24fad10>
    <Fact (of Haplotype '1') at 0x24eae50>
    <Fact (of Haplotype '2') at 0x24fad10>


Query
^^^^^

Now for the queries:

.. code-block:: python

    >>> hap = nw.haplotype_by_id(2)
    >>> hap
    <Haplotype (2) at 0x24fa990>


Edges by haplotype:

.. code-block:: python

    >>> for edge in nw.edges_by_haplotype(hap):
    ...     print edge
    <Edge ([9871.0 [2, 0]]  ) at 0x24fa710>
    <Edge ([8924.0 [1, 2]]  ) at 0x1f64c50>


Facts by haplotype:

.. code-block:: python

    >>> for fact in nw.facts_by_haplotype(hap):
    ...     print dict(fact)
    {u'lang': u'sp', u'timezone': u'utc', 'hap_id': 2, u'name': u'Andalucia'}


Haplotypes by lang enviroment:

.. code-block:: python

    >>> for hap in nw.haplotypes_by_enviroment(lang="sp"):
    ...     print hap
    <Haplotype (0) at 0x24fa2d0>
    <Haplotype (1) at 0x25c5350>
    <Haplotype (2) at 0x24fa2d0>


Haplotypes by timezone enviroment:

.. code-block:: python

    >>> for hap in nw.haplotypes_by_enviroment(timezone="utc-6"):
    ...     print hap
    <Haplotype (1) at 0x24eae50>


Haplotypes by name enviroment:

    for hap in nw.haplotypes_by_enviroment(name="Andalucia"):
        print hap

    <Haplotype (0) at 0x25c5350>
    <Haplotype (2) at 0x24eae50>


Edges by Andalucia environment:

.. code-block:: python

    >>> for edge in nw.edges_by_enviroment(name="Andalucia"):
    ...     print edge
    <Edge ([9871.0 [2, 0]]  ) at 0x24fa7d0>

All environments:

.. code-block:: python

    >>> for env in nw.enviroments():
    ...     print env
    <Enviroment {u'lang': u'sp', u'timezone': u'utc-3', u'name': u'Andalucia'} at 0x24faad0>
    <Enviroment {u'lang': u'sp', u'timezone': None, u'name': None} at 0x24db490>
    <Enviroment {u'lang': None, u'timezone': u'utc-6', u'name': None} at 0x24faad0>
    <Enviroment {u'lang': u'sp', u'timezone': u'utc', u'name': u'Andalucia'} at 0x24db490>


Statistics
^^^^^^^^^^

Here are some statistics:

.. code-block:: python

    >>> from yatel import stats

    >>> stats.average(nw) # average
    8464.66666667

    >>> stats.std(nw, name="Andalucia")
    0.0


Data Mining
^^^^^^^^^^^

Now to some data mining:

.. code-block:: python

    >>> from scipy.spatial.distance import euclidean
    >>> from yatel.cluster import kmeans

    >>> cbs, distortion = kmeans.kmeans(nw, nw.enviroments(), 2)

    >>> for env in nw.enviroments():
    ...     coords = kmeans.hap_in_env_coords(nw, env)
    ...     min_euc = None
    ...     closest_centroid = None
    ...     for cb in cbs:
    ...         euc = euclidean(cb, coords)
    ...         if min_euc is None or euc < min_euc:
    ...             min_euc = euc
    ...             closest_centroid = cb
    ...     print "{} || {} || {}".format(dict(env), closest_centroid, euc)
    {u'lang': u'sp', u'timezone': u'utc-3', u'name': u'Andalucia'} || [0 0 0] || 1.0
    {u'lang': u'sp', u'timezone': u'utc-3', u'name': u'Andalucia'} || [0 0 0] || 1.41421356237
    {u'lang': u'sp', u'timezone': None, u'name': None} || [0 0 0] || 1.0
    {u'lang': u'sp', u'timezone': None, u'name': None} || [0 1 0] || 0.0
    {u'lang': None, u'timezone': u'utc-6', u'name': None} || [0 0 0] || 1.0
    {u'lang': None, u'timezone': u'utc-6', u'name': None} || [0 1 0] || 0.0
    {u'lang': u'sp', u'timezone': u'utc', u'name': u'Andalucia'} || [0 0 0] || 1.0
    {u'lang': u'sp', u'timezone': u'utc', u'name': u'Andalucia'} || [0 0 0] || 1.41421356237


References
^^^^^^^^^^

.. [0] http://en.wikipedia.org/wiki/C%C3%B3rdoba,_Argentina
.. [1] http://en.wikipedia.org/wiki/C%C3%B3rdoba,_Veracruz
.. [2] http://en.wikipedia.org/wiki/C%C3%B3rdoba,_Andalusia
