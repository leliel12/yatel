Yatel ETL Framework
===================

Una de las principales problematicas que se enfrentan los almacenes de datos
orientados al ánalisis es la forma en el cual se cargan incrementalmente o
se actualizan sus datos.

La tecnica utilizada es la conocida como ETL_, que a grandes rasgos consiste en
**Extraer** datos de una fuente, **Transformalos** para que tengan sentido
en el contexto de nuestro almacen; y finalmente **Cargarlos** (cargar en
ingles es LOAD) a nuestra base de datos.

Yatel brinda un modesto framework para la creación de ETL para la carga de
NW-OLAP de una forma consistente.

Creando Un ETL
^^^^^^^^^^^^^^

El primer paso para crear un ETL_ es utilizar Yatel para que nos genere un
template sobre el cual trabajar en un archivo de nombre, por ejemplo,

.. code-block:: bash

    $ yatel createetl myetl.py


Si lo abrimos veremos el siguiente codigo

.. code-block:: python
    :linenos:

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    '''auto created template to create a custom ETL for yatel'''

    from yatel import etl, dom


    #===============================================================================
    # PUT YOUR ETLs HERE
    #===============================================================================

    class ETL(etl.BaseETL):

        # you can access the current network from the attribute 'self.nw'
        # You can access all the allready created haplotypes from attribute
        # 'self.haplotypes_cache'. If you want to disable the cache put a class
        # level attribute 'HAPLOTYPES_CACHE = False'


        def haplotype_gen(self):
            raise NotImplementedError()

        def edge_gen(self):
            raise NotImplementedError()

        def fact_gen(self):
            raise NotImplementedError()


    #===============================================================================
    # MAIN
    #===============================================================================

    if __name__ == "__main__":
        print(__doc__)


.. note:: Como condicion hay que aclarar que **siempre** que se utilice las herramientas
          de lineas de comando la clase con el ETL_ a correr debe llamarse
          ``ETL`` (Line 13).


.. note:: Es buena practica que solo haya un ETL por archivo, para evitar confusiones
          problematicas al momento de la ejecucion y poner en riesgo la consistencia de
          su wharehouse.


- La linea 6 son los imports que se utilizan sin ecepcion en todos los ETL
- La linea 13 crea la clase ETL que contendra toda la logica para la extraccion,
  transformacion y carga de datos.


Cabe aclarar que existen muchos metodos que pueden redefinirse (tienen una seccion mas
adelante) pero los unicos que hay que redefinir obligatoriamente son los generadores:
``haplotype_gen``, ``edge_gen``, ``fact_gen``.


- ``haplotype_gen`` (linea 21) debe retornar o bien un iterable o en el mejor de los
  casos un generador de los haplotypes que desea que se cargen en la base de datos.
  Por ejemplo podriamos decidir que los haplotypes se lean de un CSV_ utilizando el
  modulo csv de Python:

  .. code-block:: python

    def haplotype_gen(self):
        with open("haplotypes.csv") as fp:
            reader = csv.reader(fp)
            for row in reader:
                hap_id = row[0] # suponemos que el id esta en la primer columna
                name = row[1] # suponemos que la columna 1 tiene un atributo name
                yield dom.Haplotype(hap_id, name=name)


  Como es muy comun utilizar estos haplotypes en las siguientes funciones, el ETL
  se encarga de guardarlos en una variable llamada **haplotypes_cache**. Este
  cache es un un *dict-like* cuya llave son los `hap_id` y los valores los haplotypos
  en si mismo (la manipulacion del cache se vera en su propia seccion mas adelante).


- ``edge_gen`` (linea 24) debe retornar o bien un iterable o en el mejor de los
  casos un generador de los edges que desea que se cargen en la base de datos.
  Es normal querer utilizar el cache de haplotypes para de alguna manera compararlos
  y cargar el peso deseado en cada arco. Para comparar cada haplotipo con todos
  los demas excepto con el mismo podemos utilizar la funcion *itertools.combinations*
  que viene con python (si se quiere comparar los haplotypos con ellos mismos se puede
  utilizar por otro lado la funcion *itertools.combinations.with_replacement*). El peso
  finalmente estara dada por la
  `distancia de hamming <http://en.wikipedia.org/wiki/Hamming_distance>`_ entre los
  dos haplotypos utilizando el modulo *weights* presente en Yatel:


  .. code-block:: python

    def edge_gen(self):
        # combinamos de a dos haplotypos
        for hap0, hap1 in itertools.combinations(self.haplotypes_cache.values(), 2):
            w = weight.weight("hamming", hap0, hap1)
            haps_id = hap0.hap_id, hap1.hap_id
            yield dom.Edge(w, haps_id)


- ``fact_gen`` (linea 27) debe retornar o bien un iterable o en el mejor de los
  casos un generador de los facts que desea que se cargen en la base de datos.
  Normalmente la mayor complejidad de los ETL radica en esta función.
  Podemos imaginar en nuestro caso (par agregar algo de complegidad al ejemplo)
  que los facts provienen de un archivo JSON_, cuyo elemento principal es un
  objeto y sus llaves son equivalentes al atributo *name* de cada haplotype; a
  su ves los valores son un array el cual cada uno debe ser un *fact* de dicho
  haplotypo. Un ejemplo sencillo seria:


  .. code-block:: javascript


        {
            "hap_name_0": [
                {"year": 1978, "description": "something..." },
                {"year": 1990},
                {"notes": "some notes", "year": 1986},
                {"year": 2014, "active": false}
            ]
            ...
        }


  Asi la funcion que procese dichos datos debe primero determinar cual es el ``hap_id``
  para cada haplotipo antes de crear el fact. Podemos (por una cuestion de facilidad)
  guardar un *dict* cuyo valor sea el *name* del haplotipo (asumimos unico) y el valor el
  *hap_id*. Para no hacer bucles inutiles podemos hacerlo directamente en el método
  ``haplotype_gen`` con o cual quedaria de la siguiente forma:


  .. code-block:: python

    def haplotype_gen(self):
        self.name_to_hapid = {}
        with open("haplotypes.csv") as fp:
            reader = csv.reader(fp)
            for row in reader:
                hap_id = row[0]
                name = row[1]
                hap = dom.Haplotype(hap_id, name=name)
                self.name_to_hapid[name] = hap_id
                yield hap

  Ahora podemos crear los facts facilmente utilizando el mòdulo json de Python


  .. code-block:: python

    def fact_gen(self):
        with open("facts.json", "rb") as fp:
            data = json.load(fp)
            for hap_name, facts_data in data.items():
                hap_id = self.name_to_hapid[hap_name]
                for fact_data in facts_data:
                    yield dom.Fact(hap_id, **fact_data)


Por ùltimo teniendo una base de datos objetivo podemos cargarla con nuestro ETL con el comando:

.. code-block:: bash

    $ yatel runetl sqlite:///my_database.db my_etl.py


Inicialidador y limpieza de un ETL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Puede ser necesario, en algunos caso que su ETL necesite algunos recursos y que sea conveniente
liberarlos recien al termina todo el procesamiento (una conexion a una base de datos por ejemplo);
o por otro lado, crear variables globales a los mètodos

Para estos casos Yatel cuenta con dos metodos extra que se pueden redefinir en su ETL estos son:

- ``setup`` que se ejecuta previamente a **todos** los demas metodos del ETL. Sumado a esto; tambien
  puede recibir paràmetros posicionales (los parametros variables o con valores por defecto no son
  aceptados) los cuales se pueden pasar desde la linea de comando.
- ``teardown`` Este mètodo se ejeuta al finalizar todo el procesamiento y es el ultimo responsable
  en dejar el sistema en estable luego de liberar todos los recursos utilizados en la ejecucion del ETL.


En nuesto ejemplo, podriamos imaginar que se desea ecribir el momento de inicio y finalizacion
de la ejecucion del ETL (obtenidos con el mòdulo *time* de python) en un archivo que se pasa
por paràmetro. Tambien es realmente este un mejor lugar para declrar el *dict* ``name_to_hapid``
que se utilizara en los haplotipos y los facts. Las dos funciones tendran la forma


.. code-block:: python


    def setup(self, filename):
        self.fp = open(filename, "w")
        self.name_to_hapid = {}
        self.fp.write(str(time.time()) + "\n")

    def teardown(self):
        self.fp.write(str(time.time()) + "\n")
        self.fp.close()

Finalmente para correr nuestro etl ahora deberìamos utilizar el comando pasando los parametros
para setup


.. code-block:: bash

    $ yatel runetl sqlite:///my_database.db my_etl.py timestamps.log


.. note:: Cabe aclarar que todos los parametros que llegan a ``setup`` llegan en la forma
          de texto y deben ser convertidos en la medida de lo necesario.



Funciones intermedias a los generadores
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Si bien no suele ser comun su utilizacion, los ETL poseen 6 metodos mas que permiten el
control mas atomico de los ETL. Cada una de ellos se ejecutan justo antes y justo despues
de cada generador, ellos son:

- ``pre_haplotype_gen(self)`` se ejecuta justo antes de ejecutar *haplotype_gen*.
- ``post_haplotype_gen(self)`` se ejecuta justo despues de ejecutar *haplotype_gen*.
- ``pre_edge_gen(self)`` se ejecuta justo antes de ejecutar *edge_gen*.
- ``post_edge_gen(self)`` se ejecuta justo despues de ejecutar *edge_gen*.
- ``pre_fact_gen(self)`` se ejecuta justo antes de ejecutar *fact_gen*.
- ``post_fact_gen(self)`` se ejecuta justo despues de ejecutar *fact_gen*.


Manejo de Errores
^^^^^^^^^^^^^^^^^

En caso de suceder algun error en el procesamiento de un ETL, puede redefinirse
un metodo para tratar este error: ``handle_error(exc_type, exc_val, exc_tb)``

Los parametros que recibe ``handle_error`` son los equivalente a exit de un
context manager donde: *exc_type* es la clase del error (exception) que sucecio,
*exc_val* es la exception propiamente dicha y *exc_tb* es e traceback del error.

Si este mètodo suspende toda la ejecucion el ETL (incluso ``teardown``)


.. note:: los ETL **NO** son manejadores de contexto.

.. note:: ``handle_error`` **NUNCA** debe relanzar la exception que le llega
          como paràmetro. Si decesa sileciar esa exception simplemente retorne
          ``True`` o algun valor verdadero, de lo contrario la exception se
          propagarà


Por ejemplo si quisieramos silenciar la exception solo si es TypeError


.. code-block:: python

    def handle_error(self exc_type, exc_val, exc_tb):
        return exc_type == TypeError


Cache de Haplotypos
^^^^^^^^^^^^^^^^^^^

Ciclo de vida de un ETL
-----------------------

Corriendo ETL en un cronjob
----------------------------

Sugested *bash* (posix) script
------------------------------

.. code-block:: bash

    #!/usr/bin/sh
    # -*- coding: utf-8 -*-


    DATABASE="engine://your_usr:your_pass@host:port/database";
    BACKUP_TPL="/path/to/your/backup.xml";
    ETL="/path/to/your/etl_file.py";

    yatel --no-gui --database $DATABASE --backup $BACKUP_TPL --log 2> logfile.txt;
    yatel --no-gui --database $DATABASE --run-etl $ETL --log 2> logfile.txt;


Sugested *bat* (Windows) script
-------------------------------

.. code-block:: bat

    set BACKUP_TPL=c:\path\to\your\backup.json
    set ETL=c:\path\to\your\etl_file.py
    set DATABASE=sqlite://to/thing

    yatel --no-gui --database %DATABASE% --backup %BACKUP_TPL% --log 2> logfile.txt;
    yatel --no-gui --database %DATABASE% --run-etl %ETL% --log 2> logfile.txt;
