Command Line Interface
======================

For common maintenance, startup and general configuration Yatel has a 
comfortable set of commands for use from console.


Some use cases for better understanding exemplified below.


Yatel has three global options:

    #. ``-k`` | ``--ful-stack`` indicates that if a command fails, show full 
       exception output and not just the error message.
    #. ``-l`` | ``--log`` enables log of the database to standard output.


Commands
--------

- ``describe``: Receives a single parameter that is the connection string to 
  the database and prints on the screen description of the network.

  ::

    yatel describe sqlite:///my_nwwharehouse.db

    {description}

  Old command::

    yatel --database sqlite:///my_nwwharehouse.db --describe

- ``test``: Runs all tests of Yatel. Receives a single parameter that refers 
  to the level of verbosity of the tests.

  ::

    yatel test 1
    ....

  Old command::

    yatel --test 1

- ``dump``: Persists all data from a nwolap to a file in *JSON* 
  or *XML* format. It is important to note that *JSON* is very fast but 
  memory intensive for large networks; so *JSON* is recommended for small 
  networks to large networks *XML*. Dump receives two parameters:

    #. URI of the database to dump
    #. The name of the file where the information will be dumped.
       The persistence format is given by the extension of the file. To use 
       the *JSON* extension must be ``.json`` or ``.yjf`` and for XML 
       extensions are ``.xml`` or ``.yxf``

  ::

    yatel dump sqlite:///my_nwwharehouse.db dump.xml


  Old command::

    yatel --database sqlite:///my_nwwharehouse.db --dump dump.xml


- ``backup``: Similar to dump and it does the same function. The only 
  difference that the file name to be parameterized as target is not the 
  final name but a template, between the name and the extension ALWAYS a 
  timestamps is added to always create a new file. It is useful for automated 
  backup tasks.

  ::

    yatel backup sqlite:///my_nwwharehouse.db backup.xml


  Old command::

    yatel --database sqlite:///my_nwwharehouse.db --backup backup.xml


- ``load``: Restores data from a file created by the ``dump`` or ``backup`` 
  command. The first parameter of the command is the target database. The 
  second parameter is the open mode of the db, *w* (erases previous contents) 
  or *a* (adds new content to the network) and the third it's a path to 
  the file with the data.

  ::

    yatel load sqlite:///my_nwwharehouse.db a backup.xml


  Old command::

    yatel --database sqlite:///my_nwwharehouse.db --load backup.xml --mode a --force


- ``copy``: Copy an entire nwolap into another nwolap. The command takes as 
  first parameter the URI of the source network, the second parameter is the 
  open mode of the db that can be *w* (erases previous content) or *a* (adds 
  new content to the network) and the third one it is the URI of 
  destination network.

  ::

    yatel copy sqlite:///my_nwwharehouse.db w mysql://user:password@host:port/copy_nwwharehouse


  Old command::

    yatel --database sqlite:///my_nwwharehouse.db --copy mysql://user:password@host:port/copy_nwwharehouse --force --mode w


- ``createconf``: create a new configuration to run Yatel as a service in 
  *JSON* format. Receives as a parameter the name of the file to create. 
  (For the syntax of this file see: )

  ::

    yatel createconf my_new_conf.json


  Old command::

    yatel --create-server-conf my_new_conf.json


- ``createwsgi``: Create a new wsgi file to deploy Yatel to a server in 
  production mode. Receives two parameters: The first should be an absolute 
  path (preferably), to where the configuration file was created with the 
  command ``createconf`` and second the name of the wsgi file.


  ::

    yatel createwsgi my_new_conf.json my_new_wsgi.py


  Old command::

    yatel --create-wsgi my_new_conf.json my_new_wsgi.py


- ``runserver``: Runs Yatel as an HTTP service. Receives two parameters: 
  The first is the path to the configuration file created with ``createconf`` 
  command and the second IP and port where the service will be listening 
  separated by a ``:``

  ::

    yatel runserver my_new_conf.json localhost:8080


  Old command::

    yatel --runserver my_new_conf.json localhost:8080


- ``createetle``: Create a new file to extract, transform, and load data (ETL) 
  in a path specified as a parameter.

  ::

    yatel createetl my_new_etl.py

  Old command::

    yatel --create-etl my_new_etl.py


- ``describeetl``: Describe the documentation and parameters of the ETL 
  constructor passed as a parameter.

  ::

    yatel describeetl my_new_etl.py

  Old command::

    yatel --desc-etl my_new_etl.py


- ``runetl``: Runs an ETL. Receives three parameters.

    #. Destination database
    #. Open mode of the databse (*w* o *a*)
    #. ETL path

  Keep in mind that the ETL may receive more parameters in its constructor; to 
  be passed after the path to the ETL.

  ::

    yatel runetl sqlite:///my_nwwharehouse.db a my_new_etl.py param param param


  Old command::

    yatel --database sqlite:///my_nwwharehouse.db --run-etl my_new_etl.py param param param --mode a --force


