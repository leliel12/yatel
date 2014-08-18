Command Line Interface
======================

For common maintenance, startup and general configuration Yatel has a
comfortable set of commands for use from console.


Some use cases for better understanding exemplified below.


Yatel has three global options:

    #. ``-k`` | ``--ful-stack`` indicates that if a command fails, show full
       exception output and not just the error message.
    #. ``-l`` | ``--log`` enables log of the database to standard output.
    #. ``-f`` | ``--force`` if a database is try to open in 'w' or 'a'
       and a Yatel Network is discovered overwrite it.
    #. ``-h`` | ``--help`` show the help os all yatel or a single command.


Commands
--------

- ``version``: Print the Yatel version and exit.

.. code-block:: bash

    $ yatel version
    0.3


- ``list``: Lists all available connection strings in yatel.

.. code-block:: bash

    $ yatel list
    sqlite: sqlite:///${database}
    memory: sqlite://
    mysql: mysql://${user}:${password}@${host}:${port}/${database}
    postgres: postgres://${user}:${password}@${host}:${port}/${database}



- ``describe``: Receives a single parameter that is the connection string to
  the database and prints on the screen description of the network.

.. code-block:: bash

    $ yatel describe sqlite:///my_nwwharehouse.db
    {description}


- ``test``: Runs all tests of Yatel. Receives a single parameter that refers
  to the level of verbosity [0|1|2] of the tests.

.. code-block:: bash

    $ yatel test 1
    ....


- ``dump``: Persists all data from a nwolap to a file in *JSON*
  or *XML* format. It is important to note that *JSON* is very fast but
  memory intensive for large networks; so *JSON* is recommended for small
  networks to large networks *XML*. Dump receives two parameters:

    #. URI of the database to dump
    #. The name of the file where the information will be dumped.
       The persistence format is given by the extension of the file. To use
       the *JSON* extension must be ``.json`` or ``.yjf`` and for XML
       extensions are ``.xml`` or ``.yxf``

.. code-block:: bash

    $ yatel dump sqlite:///my_nwwharehouse.db dump.xml


- ``backup``: Similar to dump and it does the same function. The only
  difference that the file name to be parameterized as target is not the
  final name but a template, between the name and the extension ALWAYS a
  timestamps is added to always create a new file. It is useful for automated
  backup tasks.

.. code-block:: bash

    $ yatel backup sqlite:///my_nwwharehouse.db backup.xml


- ``load``: Restores data from a file created by the ``dump`` or ``backup``
  command. The first parameter of the command is the target database. The
  second parameter is the open mode of the db, *w* (erases previous contents)
  or *a* (adds new content to the network) and the third it's a path to
  the file with the data.

.. code-block:: bash

    $ yatel load sqlite:///my_nwwharehouse.db a backup.xml


- ``copy``: Copy an entire nwolap into another nwolap. The command takes as
  first parameter the URI of the source network, the second parameter is the
  open mode of the db that can be *w* (erases previous content) or *a* (adds
  new content to the network) and the third one it is the URI of
  destination network.

.. code-block:: bash

    $ yatel copy sqlite:///my_nwwharehouse.db w mysql://user:password@host:port/copy_nwwharehouse


- ``pyshell``: Abre una interprete python (Ipython_ or Bpython_ if it posible)
  con la NWOLAP pasada como parametro en el contexto

.. code-block:: bash

    $ yatel pyshell sqlite:///my_nwwharehouse.db

        Welcome to Yatel Interactive mode.
        Yatel is ready to use. You only need worry about your project.
        If you install IPython, the shell will use it.
        For more info, visit http://getyatel.org/
        Available modules:
            Your NW-OLAP: nw
            from yatel: db, dom, stats
            from pprint: pprint

    >>>

- ``qbjshell``: Abre una interprete QBJ con la NWOLAP pasada como parametro
  en el contexto.

.. code-block:: bash

    $ yatel qbjshell sqlite:///my_nwwharehouse.db
    Yatel QBJ Console

    QBJ [sqlite://***/my_nwwharehouse.db]>


- ``createconf``: create a new configuration to run Yatel as a service in
  *JSON* format. Receives as a parameter the name of the file to create.
  (For the syntax of this file see: )

.. code-block:: bash

    $ yatel createconf my_new_conf.json


- ``createwsgi``: Create a new wsgi file to deploy Yatel to a server in
  production mode. Receives two parameters: The first should be an absolute
  path (preferably), to where the configuration file was created with the
  command ``createconf`` and second the name of the wsgi file.


.. code-block:: bash

    $ yatel createwsgi my_new_conf.json my_new_wsgi.py


- ``runserver``: Runs Yatel as an HTTP service. Receives two parameters:
  The first is the path to the configuration file created with ``createconf``
  command and the second IP and port where the service will be listening
  separated by a ``:``

.. code-block:: bash

    $ yatel runserver my_new_conf.json localhost:8080


- ``createetle``: Create a new file to extract, transform, and load data (ETL)
  in a path specified as a parameter.

.. code-block:: bash

    $ yatel createetl my_new_etl.py


- ``describeetl``: Describe the documentation and parameters of the ETL
  constructor passed as a parameter.

.. code-block:: bash

    $ yatel describeetl my_new_etl.py


- ``runetl``: Runs an ETL. Receives three parameters.

    #. Destination database
    #. Open mode of the databse (*w* o *a*)
    #. ETL path

  Keep in mind that the ETL may receive more parameters in its constructor; to
  be passed after the path to the ETL.

.. code-block:: bash

    $ yatel runetl sqlite:///my_nwwharehouse.db a my_new_etl.py param param param

