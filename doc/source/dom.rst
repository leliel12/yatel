Objetos de Yatel
================

Yatel posee en el archivo ``yatel.dom`` una serie de clases que sirven para
abstraer la información en las estructuras de datos que conceptualmente
utilizamos en los *nw-olap*

Todas las clases ahi definidas tienen comportamientos de diccionarios
inmutables y la mas particular de todas es probablemente ``dom.Haplotype.``.
Asi suponiendo dos objetos cualesquiera de cualquiera de las clases es
son sentencias equivalentes ``obj.attribute`` o ``ob["attribute"]``.

Como todos diccionarios estan diponibles los metodos ``items()``, ``keys()``
``values()`` y ``get(k)``.

Todos las instancias de ``yatel.dom`` por ser inmutables pueden ser utilizadas
como llaves en un diccionario excepto que el objeto contenga algun elemento
no hasheable. Ejemplo:

.. code-block:: python

    >>> from yatel import dom

    >>> hap = dom.Haplotype(1)
    >>> data = {hap: 1} # works

    >>> hap = dom.Haplotype(2, attr=[1,2,3]) # warning list is unhashable
    >>> data = {hap: 1} # works
    ...
    TypeError: unhashable type: 'list'


Clases
------

- ``dom.Haplotype`` representa un nodo en una nw-olap y
  recibe almenos un parametro (el *hap_id*) siendo los
  demas nombrados opcionales. Dos haplotipos son iguales si
  tienen el mismo hap_id independiente mente de los demas atributos.
  Otra característica importante es que los atributos con valores *None* no
  son tomados en cuenta y se eliminan.
  Ejemplo:

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

- ``dom.Edge`` representa un arco de una nw-olap. Recibe en su contructor
  dos parametros: El primero es el peso del arco (se transforma siempre
  a flotante) y el segundo es un iterable con los ``hap_id`` de los
  haplotipos que relaciona. Dos arcos son iguales solamente si tienen el
  mismo peso y conectan a los mismos haplotipos. Solo podeen dos atributos
  que son los mismos del constructor: el peso ``edge.weight`` y las
  coxiones en una tupla ``edge.haps_id``

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


- ``dom.Fact`` son la meta data de analisis de los haplotipos. Solo tienen
  el primer parametro obligatorio que es el ``hap_id`` del haplotipo al
  cual pertenecen y todos los demas son parametros nombrados opcionales.
  Los ``dom.Fact`` son iguales solamente si pertenecen al mismo haplotipo
  y posee los mismos atributos con los mismos valores. Otra característica
  importante es que los atributos con valores *None* no son tomados en cuenta
  y se eliminan.

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



