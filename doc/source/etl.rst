Yatel ETL Model
===============

Sugested *bash* (posix) script
------------------------------

.. code-block:: bash

    #!/usr/bin/sh
    # -*- coding: utf-8 -*-


    DATABASE="engine://your_usr:your_pass@host:port/database";
    BACKUP_TPL="/path/to/your/backup.json";
    ETL="/path/to/your/etl_file.py";

    yatel --no-gui --database $DATABASE --backup $BACKUP_TPL;
    yatel --no-gui --database $DATABASE --run-etl $ETL;


Sugested *bat* (Windows) script
-------------------------------

.. code-block:: bat

    set BACKUP_TPL=c:\path\to\your\backup.json
    set ETL=c:\path\to\your\etl_file.py
    set DATABASE=sqlite://to/thing

    yatel --no-gui --database %DATABASE% --backup %BACKUP_TPL%
    yatel --no-gui --database %DATABASE% --run-etl %ETL%
