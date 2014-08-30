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


.. note::

    Como condicion hay que aclarar que **siempre** que se utilice las herramientas
    de lineas de comando la clase con el ETL_ a correr debe llamarse
    ``ETL`` (Line 13).
    Es buena practica que solo haya un ETL por archivo, para evitar confusiones
    problematicas al momento de la ejecucion y poner en riesgo la consistencia de
    su wharehouse.
    

- La linea # son los imports que se utilizan sin ecepcion en todos los ETL
- La linea # crea la clase ETL que contendra toda la logica para la extraccion, 
  transformacion y carga de datos.

Cabe aclarar que existen muchos metodos que pueden redefinirse (tienen una seccion mas 
adelante) pero los unicos que hay que redefinir obligatoriamente son los generadores:
``haplotype_gen``, ``edge_gen``, ``fact_gen``.

- ``haplotype_gen`` (linea #) debe retornar o bien un iterable o en el mejor de los 
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
  
- ``edge_gen`` (linea #) debe retornar o bien un iterable o en el mejor de los 
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
            

- ``fact_gen`` (linea #) debe retornar o bien un iterable o en el mejor de los 
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

Funciones intermedias a los generadores
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
