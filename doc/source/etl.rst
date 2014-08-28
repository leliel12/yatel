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

Creando Un Etl
^^^^^^^^^^^^^^

El primer paso para crear un ETL_ es utilizar Yatel para que nos genere un
template sobre el cual trabajar

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

Analizaremos las lineas una por una omitiendo los comentarios:


Como condicion hay que aclarar que **siempre** que se utilice las herramientas
de lineas de comando la clase con el ETL_ a correr debe llamarse
``ETL`` (Line 13).

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
