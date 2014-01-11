Especificación de QBJ
=====================

**Query By JSON** (QBJ) surge con la necesidad de un lenguaje de consulta
agnóstico a bases de datos de MNwOLAP (redes multidimencionales,
del ingles 'Multidimensional Networks OLAP_') que brinda yatel.


Características
---------------

- Declarativo.
- Diseñado basandose en JSON dada su ampla difusion en Python_ (lenguaje
  utilizado para implementar Yatel).
- Para el parseo de tipos de datos se utiliza el modulo ``yatel.typeconv``
  que tambien es aprobechado en las funcionalidades de exportanción e
  importación de Yatel.
- Previo al parseo de datos QBJ valida la consulta con json-schema_ para evitar
  calculos inútiles.
- Se considera un lenguaje de bajo nivel.


Syntaxis: Consulta y Respuesta
------------------------------

Partamos de un ejemplo con la función mas simple que posee QBJ, *ping*

El objetivo de la funcion *ping* es simplemente recibir una respuesta sin
contenido que indique que Yatel esta escuchando nuestras consultas.

**Ejemplo 1**

.. code-block:: javascript
    :linenos:

    {
        "id": "123",
        "function": {
            "name": "ping",
            "args": [],
            "kwargs": {}
        }
    }

- ``id`` es un identificador de la consulta. Puede ser un valor numérico entero
  un string o ``null``. Este valor sera retornado en la respuesta de la
  consulta.Si usted esta procesando esto asincronamente puede utilizar este
  campo para discriminar su procesamiento.
- ``function`` es la segunda, y ultima, llave obligatoria en la consulta.
  Consiste en la consulta en sí que va a ser validada y ejecutada, la cual
  tiene a su ves varias llaves.

    - ``name`` es el nombre de la función a ser ejecutada, en este caso *ping*
    - ``args`` son los argumentos posicionales de la función. En este caso
       *ping* no posee ningun parámetro con lo cual la totalidad de la llave
       y el valor pueden ser oviados.
    - ``kwargs`` son los parametros nombrados de la funcion y al estar vacio
      pueden oviarse de la declaración total.

Quitando los parametros inecesarios la funcion completa podria escribirse

.. code-block:: javascript

    {
        'id': '123',
        'function': {
            'name': 'ping'
        }
    }

La respuesta de esta consulta tiene la forma:

.. code-block:: javascript
    :linenos:

    {
        'id': '123',
        'error': false,
        'error_msg': '',
        'stack_trace': None,
        'result': {
            'type': 'bool',
            'value': true
        }
    }

Donde:

- ``id`` es el mismo id de la consulta.
- ``error`` es un valor booleanno que se ra falso mientras la consulta se haya
  procesado con éxito.
- ``error_msg`` Si el valor de ``error`` es *true* esta llave contendra una
  descripción del error ocurrido.
- ````



Funciones
---------


El proceso de resolución
------------------------
