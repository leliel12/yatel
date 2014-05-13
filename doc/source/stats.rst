Stats
=====

El modulo estadísticas una de las partes fundamentales de Yatel, ayuda a la
toma de desiciones por medio de la extraccion de medidas de posicion,
variacion, asimetria y puntiagudes de la variabilidad de un ambiente dado.

Las funcionalidades de este modulo se dividen en 2 grupos bien diferenciados:

- *Transformacion:* Se encarga de convertir un ambiente de una red dada en un
  array de numpy para acelerar el calculo de las estadísticas.
- *Calculo:* Calcula las estadisticas propiamente dichas. Soportan como
  parametro una red de haplotipos y filtros para determinar un ambiente o un
  array-like con los valores ya precalculados del ambiente.

Si bien todas las funciones de cálculo utilizan internamente las de
transformación, es muchas veces determinante para el rendimiento precalcular
un array con los valores a utilizar.

Funciones de Transformación
---------------------------

Las funciones de transformacion son dos:

- ``weights2array``: dado un iterable de instancias ``dom.Edges`` esta funcion
  devuelve un array de *numpy* con todos los valores de los pesos de dichos
  arcos. Los pesos se convierten (por cuestiones de rendimiento) en flotantes
  de 128 bytes (``numpy.float128``).
  Por ejemplo:

.. code-block:: python

    >>> from yatel import dom, db, stats

    # Nuestra red de ejemplo clasica
    >>> nw = db.YatelNetwork("memory", mode="w")

    >>> nw.add_elements([
    ... dom.Haplotype(0, name="Cordoba", clima="calor", edad=200, frio=True), # left
    ...     dom.Haplotype(1, name="Cordoba", poblacion=12), # right
    ...     dom.Haplotype(2, name="Cordoba"), # bottom

    ... dom.Edge(6599, (0, 1)),
    ... dom.Edge(8924, (1, 2)),
    ... dom.Edge(9871, (2, 0)),

    ... dom.Fact(0, name="Andalucia", lang="sp", timezone="utc-3"),
    ... dom.Fact(1, lang="sp"),
    ... dom.Fact(1, timezone="utc-6"),
    ... dom.Fact(2, name="Andalucia", lang="sp", timezone="utc")
    ... ])
    ... nw.confirm_changes()

    # extraemos todos los arcos
    edges = nw.edges()
    stats.weights2array(edges)
    array([ 6599.0,  8924.0,  9871.0], dtype=float128)


- ``env2weightarray``: Esta funcion se encarga de convertir una red, en un
  array con todos los pesos de los arcos que contiene o alguno de ellos
  filtrados por ambientes. Tambien por motivos de implementacione puede recibir
  cualquier iterable y convertirlo en un array de numpy.


.. code-block:: python

    >>> stats.env2weightarray(nw)
    array([ 6599.0,  8924.0,  9871.0], dtype=float128)

    # con un ambiente
    >>> stats.env2weightarray(nw, name="Andalucia")
    array([ 9871.0], dtype=float128)


Funciones de Calculo
--------------------

Las funciones de calculo son las encargadas de calcular eficientemente
estadisticas sobre la variabilidad de una red o ambiente de una red.
El listado completo de funciones las puede encontrar en el la referencia
del módulo stats.

.. code-block:: python

    # calulamos la media
    >>> stats.average(nw)

    # o de un ambiente
    >>> stats.average(nw, , name="Andalucia")


Por motivos de rendimiento muchas veces es conveniente extraer todos los pesos
de un ambiente antes de realizar muchos calculos (esto puede acelerar varios
cientos de veces los calculos sucesivos ya que obvia el acceso a a base de
datos)

.. code-block:: python

    # extraemos el array con los valores
    >>> arr = stats.env2weightarray(nw, name="Andalucia")

    # calculamos la desviacion
    >>> stats.std(arr)


Las funciones tambien soportan iterables de python como pueden ser listas
o tuplas

.. code-block:: python

    >>> stats.average([1, 2, 3])

    # esto va a devolver no es un numero
    >>> stats.average([])
    nan


Un ejemplo mas avanzado
-----------------------

Vamos a calcular un
`One-Way ANOVA <http://en.wikipedia.org/wiki/Analysis_of_variance>`_ con
dos ambientes de nuestra red.

.. code-block:: python

    # importamos el one-way anova
    >>> from scipy.stats import f_oneway

    # primera muestra
    >>> arr0 = stats.env2weightarray(nw, lan="sp")

    # segunda muestra
    >>> arr1 = stats.env2weightarray(nw, name="Andalucia")

    # tercera muestra
    >>> arr2 = stats.env2weightarray(nw, timezone="utc")

    >>> f, p = f_oneway(arr0, arr1, arr2)

    # valor de F
    >>> f

    # valor de P
    >>> p

Se podria continuar el analisis viendo las medias y desviaciones de
cada uno de los ambientes o realizando test a posteriori

