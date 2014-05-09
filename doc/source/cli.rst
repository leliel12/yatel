Command Line Interface
======================

Para tareas comunes de mantenimiento, puesta en marcha y configuración general
Yatel posee una cómoda serie de comandos para utilizarlo desde consola.


Se ejemplifican a continuación algunos casos de uso para su mejor comprensión.


Yatel posee tres opciones globales:

    #. ``-k`` | ``--ful-stack`` que indica que de fallar un comando se mostrará
       completa la salida de excepciones y no solo el mensaje de error.
    #. ``-l`` | ``--log`` activara el logeo de la base de datos a en la salida
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

    yatel --database sqlite:///my_nwwharehouse.db --load backup.xml --mode a --force


- ``copy``: Copia toda una nwolap a otra nwolap. El comando recibe como primer
  parámetro la URI de origen de datos, cel segundo parámetro es el
  modo de apertura de la db que pueder *w* (pisa todo el contenido) o
  *a* (agrega el nuevo contenido a la red) y como tercero la URI a donde se
  copiaran los datos.

  ::

    yatel copy sqlite:///my_nwwharehouse.db w mysql://user:password@host:port/copy_nwwharehouse


  Comando viejo::

    yatel --database sqlite:///my_nwwharehouse.db --copy mysql://user:password@host:port/copy_nwwharehouse --force --mode w


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

    yatel --database sqlite:///my_nwwharehouse.db --run-etl my_new_etl.py param param param --mode a --force


