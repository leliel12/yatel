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
        with open("file.csv") as fp:
            reader = csv.reader(fp)
            for row in reader:
                hap_id = row[0] # suponemos que el id esta en la primer columna
                name = row[1] # suponemos que la columna 1 tiene un atributo name
                yiel dom.Haplotype(hap_id, name=name)
    
        
  Como es muy comun utilizar estos haplotypes en las siguientes funciones, el ETL
  se encarga de guardarlos en una variable llamada **haplotypes_cache**; 
  la manipulacion del cache se vera en su propia seccion mas adelante.


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
