Command Line Interface
======================

Para tareas comunes de mantenimiento, puesta en marcha y configuración general
Yatel posee una cómoda serie de comandos para utilizarlo desde consola.


Se ejemplifican a continuación algunos casos de uso para su mejor comprensión.


Yatel posee tres opciones globales:

    #. ``-k``|``--ful-stack`` que indica que de fallar un comando se mostrará
       completa la salida de excepciones y no solo el mensaje de error.
    #. ``-l``|``--log`` activara el logeo de la base de datos a en la salida
       estandar.


Comandos
--------

- ``describe``: Recibe un único parámetro que es el string de conexión a la
  base de datos e imprime por pantalla la descripción de dicha red.

  ::

    yatel describe sqlite:///my_nwwharehouse.db

    {description}

  Comando viejo::

    yatel --database sqlite:///my_nwwharehouse.db --describe

- ``test``: Ejecuta todos los test de yatel. Recibe un único parámetero que
  se refiere al nivel de verborragia de los test.

  ::

    yatel test 1
    ....

  Comando viejo::

    yatel --test 1

- ``dump``: Persiste toda los datos de una nwolap en un archivo en formato
  *JSON* o *XML*. Es importante aclarar que *JSON* es muy rápido pero consume
  mucha memoria en redes grandes; por lo cual se recomienda *JSON* para redes
  pequeñas y *XML* para redes grandes. Dump recibe dos parámetros:

    #. La URI de la base de datos a volcar
    #. El nombre del archivo donde se volcará la información. El formato de
       persistencia esta dado por la extensión de dicho archivo. Si desea usar
       el formato *JSON* la extensión debe ser ``.json`` o ``.yjf`` mientras
       que para *XML* las alternativas son ``.xml`` o ``.yxf``

  ::

    yatel dump sqlite:///my_nwwharehouse.db dump.xml


  Comando viejo::

    yatel --database sqlite:///my_nwwharehouse.db --dump dump.xml


- ``backup``: Es similar a dump y cumple su misma función. La única diferencia
  que el nombre del archivo que se le parametriza como destino no es el nombre
  final sino una plantilla, Donde entre el nombre la extensión SIEMPRE se agrega
  una marca de fecha y hora para crear siempre un archivo nuevo. Es útil para
  tareas de de backup automatizado.

  ::

    yatel backup sqlite:///my_nwwharehouse.db backup.xml


  Comando viejo::

    yatel --database sqlite:///my_nwwharehouse.db --backup backup.xml


- ``load``: Restaura los datos de una archivo creado con el comando ``dump``
  o ``backup`` a una base de datos. El primer parámetro del comando es la
  base de datos destino, el segundo parámetro es el modo de apertura de la db
  que pueder *w* (pisa todo el contenido) o *a* (agrega el nuevo contenido a la red)
  y el tercero el path al archivo con los datos.

  ::

    yatel load sqlite:///my_nwwharehouse.db a backup.xml


  Comando viejo::

    yatel --database sqlite:///my_nwwharehouse.db --load backup.xml --mode a


- ``copy``: Copia toda una nwolap a otra nwolap. El comando recibe como primer
  parámetro la URI de origen de datos, cel segundo parámetro es el
  modo de apertura de la db que pueder *w* (pisa todo el contenido) o
  *a* (agrega el nuevo contenido a la red) y como tercero la URI a donde se
  copiaran los datos.

  ::

    yatel copy sqlite:///my_nwwharehouse.db mysql://user:password@host:port/copy_nwwharehouse -f


  Comando viejo::

    yatel --database sqlite:///my_nwwharehouse.db --copy mysql://user:password@host:port/copy_nwwharehouse --force


- ``createconf``: crea una nueva configuración para correr yatel como servicio
  en formato *JSON*. Recibe como parámetro el nombre del archivo a crear.
  (Para ver la sintaxis de dicho archivo ver: )

  ::

    yatel createconf my_new_conf.json


  Comando viejo::

    yatel --create-server-conf my_new_conf.json


- ``createwsgi``: Crea un nuevo archivo wsgi para desplegar yatel contra un
  servidor en modo producción. Recibe dos parámetros: El primero debe ser
  un path, de preferencia, absoluto al lugar donde esta la configuración creada
  con el comando ``createconf`` y el segundo el nombre del archivo wsgi a
  crear.


  ::

    yatel createwsgi my_new_conf.json my_new_wsgi.py


  Comando viejo::

    yatel --create-wsgi my_new_conf.json my_new_wsgi.py


- ``runserver``: Pone a correr Yatel como un servicio *HTTP*. Recibe dos
  parámetros: El primero es el path al archivo de configuración creado con el
  comando ``createconf`` y el segundo la IP y el puerto donde quedara escuchando
  el servicio separado por un ``:``

  ::

    yatel runserver my_new_conf.json localhost:8080


  Comando viejo::

    yatel --runserver my_new_conf.json localhost:8080


- ``createetle``: Crea un nuevo archivo de lectura, transformación y carga de
  datos (ETL) en un path especificado como parámetro.

  ::

    yatel createetl my_new_etl.py

  Comando viejo::

    yatel --create-etl my_new_etl.py


- ``describeetl``: Describe la documentación y los parámetros del constructor
  del ETL que se pasa como parámetro.

  ::

    yatel describeetl my_new_etl.py

  Comando viejo::

    yatel --desc-etl my_new_etl.py


- ``runetl``: Corre un ETL. Recibe tres parámetros.

    #. La la base de datos destino
    #. El modo de apertura de la base de datos (*w* o *a*)
    #. El path al ETL

  Hay que tener en cuenta que el ETL puede recibir mas parámetros en su constructor;
  que se deben pasarse luego del parámetro con el path al ETL en sí.

  ::

    yatel runetl sqlite:///my_nwwharehouse.db a my_new_etl.py param param param


  Comando viejo::

    yatel --database sqlite:///my_nwwharehouse.db --run-etl my_new_etl.py param param param --mode a














::

    usage: Yatel [-h] [--version] [-f] [--full-stack] [--log]
             [--list-connection-strings] [--database CONNECTION_STRING]
             [--test LEVEL] [--mode [r|w|a]] [--describe]
             [--fake-network N_HAPLOTYPES APROX_N_FACTS WEIGHT_CALCULATOR]
             [--dump FILENAME.EXT] [--backup FILENAME_TEMPLATE.json]
             [--load FILENAME.EXT] [--copy CONNECTION_STRING]
             [--create-wsgi FILE.wsgi CONF.json FILE.wsgi CONF.json]
             [--create-server-conf CONF.json]
             [--runserver CONF.json HOST:PORT] [--create-etl ETL_FILENAME.py]
             [--desc-etl PATH/TO/MODULE.py] [--run-etl ARG [ARG ...]]

    Yatel allows the creation of user-profile-distance-based of OLAP Network and
    their multidimensional analysis through a process of exploration.

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -f, --force           If you perform some action like import orcopy this
                            option destroya network in this connection
      --full-stack          If yatel fails, show all the stack trace of the error
      --log                 log all backend info to stdio
      --list-connection-strings
                            List all available connection strings in yatel
      --database CONNECTION_STRING
                            database to be open with yatel (see yatel --list-
                            conection-strings)
      --test LEVEL          Run all yatel test suites
      --mode [r|w|a]        The mode to open the database [r|w|a]
      --describe            Print information about the network
      --fake-network N_HAPLOTYPES APROX_N_FACTS WEIGHT_CALCULATOR
                            Create a new fake full conected network with on given
                            connection string. The first parameter is the number
                            of haplotypes, the second one is the number of maximun
                            facts of every haplotype and the third is the algoritm
                            to calculate the distance
      --dump FILENAME.EXT   Export the given database to EXT format.
      --backup FILENAME_TEMPLATE.json
                            Like dump but always create a new file with the format
                            'filename_template<TIMESTAMP>.EXT'.
      --load FILENAME.EXT   Import the given file to the given database.
      --copy CONNECTION_STRING
                            Copy the database of `database` to this connection
      --create-wsgi FILE.wsgi CONF.json FILE.wsgi CONF.json
                            Create a new wsgi file for a given configuration
      --create-server-conf CONF.json
                            Create a new configuration file for runserver
      --runserver CONF.json HOST:PORT
                            Run yatel as http server with a given config file
      --create-etl ETL_FILENAME.py
                            Create a template file for write yout own etl
      --desc-etl PATH/TO/MODULE.py
                            Return a list of parameters and documentataton about
                            the etl The argument is in the format
                            path/to/module.py The BaseETL subclass must be names
                            after ETL
      --run-etl ARG [ARG ...]
                            Run one or more etl inside of a given script. The
                            first argument is in the format path/to/module.py the
                            second onwards parameter are parameters of the setup
                            method of the given class.
