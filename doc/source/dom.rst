Yatel Objects
=============

Yatel has a series of classes in the file ``yatel.dom`` that serve to abstarct 
the information into data structures that we conceptually use in *nw-olap*

All classes defined there having behavior like immutable dictionaries and most 
notably of all is probably ``dom.Haplotype.``. So assuming two objects of 
either class, the following statements are equivalent ``obj.attribute`` o 
``ob["attribute"]``.

Like any dictionary, they have available methods like ``items()``, ``keys()``
``values()`` y ``get(k)``.

All instances of ``yatel.dom`` for being immutable can be used as keys in a 
dictionary except that the object contains a non hasheable element. Example:

.. code-block:: python

    >>> from yatel import dom

    >>> hap = dom.Haplotype(1)
    >>> data = {hap: 1} # works

    >>> hap = dom.Haplotype(2, attr=[1,2,3]) # warning list is unhashable
    >>> data = {hap: 1} # works
    ...
    TypeError: unhashable type: 'list'


Classes
-------

- ``dom.Haplotype`` represents a node in a nw-olap and receives at least one 
  parameter (el *hap_id*) others being named optionally. Two haplotypes are 
  equal if they have the same hap_id regardless of other attributes. Another 
  important feature is that attributes with values ​​*None* are not taken into 
  account and removed.
  Example:

.. code-block:: python

    >>> from yatel import dom
    >>> hap0 = dom.Haplotype(1)
    >>> hap1 = dom.Haplotype(1, attr="foo", attr2=None)
    >>> hap0 == hap1
    True

    >>> "attr" in hap0
    False
    >>> "attr" in hap1
    True

    >>> hap1.attr2 # invalid because is None
    AttributeError: 'Haplotype' object has no attribute 'attr2'

    >>> hap1.attr
    "foo"
    >>> hap1["attr"]
    "foo"
    >>hap0.get("wat?", "default")
    "default"

    >>> hash(hap0) == hash(hap1)
    True

    >>> id(hap0) == id(hap1)
    False

    >>> hap0 is hap1
    False

    >>> len(hap0)
    1
    >>> len(hap1)
    2

    >>> d = {hap0: "foo"}
    >>> d[hap1] # remember same hap_id
    "foo"

      >>> hap1 in d and hap0 in d
      True

- ``dom.Edge`` represents an edge in the nw-olap. Receives two parameters in 
  its constructor: The first is the weight of arc (always converted to float) 
  and the second is an iterable with the ``hap_id`` of the haplotypes 
  associated. Two edges are equal only if they have the same weight and the 
  same haplotypes connected. Only have two attributes that are the same as the 
  constructor: it's weight ``edge.weight`` and connections in a tuple ``edge.haps_id``

.. code-block:: python

    >>> from yatel import dom
    >>> edge0 = dom.Edge(1, [1, 2]) # weight 1 and connect haps 1 and 2
    >>> edge1 = dom.Edge(1.0, [1, 3]) # weight 1 and connect haps 1 and 3
    >>> edge0 == edge1
    False

    >>> edge0.haps_id
    (1, 2)

    >>> d = {edge0: "foo", edge1: "waa"}
    >>> d
    {<Edge (1.0 (1, 2)) at 0x259a710>: 'foo',
    <Edge (1.0 (1, 3)) at 0x259a750>: 'waa'}


- ``dom.Fact`` are the meta data of the analysis of haplotypes. Only their 
  first parameter is required,  ``hap_id`` of the haplotype to which they 
  belong, and all other named parameters are optional.
  ``dom.Fact`` are equal only if they belong to the same haplotype and 
  possesses the same attributes with the same values. Another important feature
  is that attributes with values ​​*None* are not taken into account and removed.

.. code-block:: python

    >>> from yatel import dom
    >>> fact0 = dom.Fact(0, attr0=1, attr1=None)
    >>> fact1 = dom.Fact(1, attr0=1)

    >>> fact0 == fact1
    False

    >>> fact0 is fact1
    False

    >>> set([fact0, fact1])
    {<Fact (of Haplotype '0') at 0x22e75d0>,
     <Fact (of Haplotype '1') at 0x22e78d0>}



