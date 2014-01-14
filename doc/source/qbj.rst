Especificación de QBJ
=====================

**Query By JSON** (QBJ) surge con la necesidad de un lenguaje de consulta
agnóstico a bases de datos de MNwOLAP (redes multidimencionales,
del ingles 'Multidimensional Networks OLAP_') que brinda yatel.


Características
---------------

- Declarativo.
- Tipado.
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

#. **Consulta simple**

    .. code-block:: javascript

        {
            "id": "123",
            "function": {
                "name": "ping",
                "args": [],
                "kwargs": {}
            }
        }

    - ``id`` es un identificador de la consulta. Puede ser un valor numérico
      entero un string o ``null``. Este valor sera retornado en la respuesta de
      la consulta.Si usted esta procesando esto asincronamente puede utilizar
      este campo para discriminar su procesamiento.
    - ``function`` es la segunda, y ultima, llave obligatoria en la consulta.
      Consiste en la consulta en sí que va a ser validada y ejecutada, la cual
      tiene a su ves varias llaves.

        - ``name`` es el nombre de la función a ser ejecutada, en este caso
          *ping*
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

        {
            'id': '123',
            'error': false,
            'error_msg': '',
            'stack_trace': null,
            'result': {
                'type': 'bool',
                'value': true
            }
        }

    Donde:

    - ``id`` es el mismo id de la consulta.
    - ``error`` es un valor booleanno que se ra falso mientras la consulta se
      haya procesado con éxito.
    - ``error_msg`` Si el valor de ``error`` es *true* esta llave contendra una
      descripción del error ocurrido.
    - ``stack_trace`` si el valor de ``error`` es *true* y la consulta se
      ejecuto en modo debug, contiene toda la  secuencias de llamadas de cuando
      sucedio el error.
    - ``result`` siempre vale *null* si el valor de ``error`` es *true*. Por
      otro lado si no sucedio ningun error result posee el valor resultante de
      la funcion (en nuestro *ping*) el cual esta en formato de
      ``yatel.typeconv`` e indica que el resultado es del tipo boleano y su
      valor es verdadero.

    En resumen nuestro ejemplo simplemente dice que no sucedio ningun error y
    como resultado se devuelve un valor de verdad boleano.

#. **Una consulta con errores**

    Supongamos la llamada a una funcion inexistente para ver un resultado de una
    consulta con errores.

    .. code-block:: javascript

        {
            "id": 31221220,
            "function": {
                "name": "fail!",
            }
        }

    En qbj la funcion *fail!* no existe por lo tanto el resultado seria si lo
    ejecutamos en modo debug el siguiente

    .. code-block:: javascript

        {
            'id': 31221220,
            'error': true,
            'error_msg': "'fail!'",
            'stack_trace': "Traceback (most recent call last):...",
            'result': null
        }

    Donde:

    - El ``id`` es el mismo de la consulta.
    - ``error`` es *true*.
    - ``error_msg`` nor informa que algo que enviamos con el valor *fail* es
      producto del error.
    - ``stack_trace`` contiene toda la sucecion de llamadas donde sucedio el
      error dentro de Yatel (cortado para el ejemplo)
    - ``result`` regresa vacio ya que sucedio un error durante el procesamiento
      de la consulta.


#. **Consulta tipica de Yatel**


    Veremos ahora un ejemplo con una funcion mas tipica del dominio de Yatel
    como la consulta de obtener un haplotypo por su id.

    .. code-block:: javascript

        {
            "id": null,
            "function": {
                "name": "haplotype_by_id",
                "args": [
                    {
                        "type": "literal",
                        "value": "01"
                    }
                ]
            }
        }

    En este caso la funcion *haplotype_by_id* recibe un parametro con el valor
    *01* que sera el id del haplotypo a buscar. El valor de ``type`` es
    *literal* con lo cual el valor no sera transformado del tipo de dato json
    (en este caso string) antes de ser enviado a la función. Si pensamos esto
    como en un llamado a una funcion Python podria imaginarse como
    ``haplotype_by_id("01")``

    .. code-block:: javascript

        {
            'id': null,
            'error': false,
            'error_msg': '',
            'stack_trace': null,
            'result': {
                'type': 'Haplotype',
                'value': {
                    'hap_id': {'type': 'int', 'value': 1},
                    'name': {'type': 'unicode', 'value': 'Amet'},
                    'special': {'type': 'bool', 'value': false}
                }
            }
        }

    El resultado entrega  un valor del tipo *Haplotype* cuyos atributos son:
    ``hap_id`` entero de valor *1*, ``name`` unicode de valor *Amet* y un *bool*
    llamado ``special`` con el valor *false*


#. **Consulta con un manejo mas avanzado de tipos**

    La siguiente consulta es una consulta ``sum`` que suma dos o mas valores
    cualesquiera se los pase.

    .. code-block:: javascript

        {
            "id": "someid",
            "function": {
                "name": "sum",
                "kwargs": {
                    "nw": {
                        "type": "list",
                        "value": [
                            {"type": "literal", "value": 1},
                            {"type": "int", "value": "2"}
                        ]
                    }
                }
            }
        }

    Como vemos en esta consulta el parametro ``nw`` es una lista que contiene
    los valores 1 (definido como literal, asi que Yatel toma el valor json)
    y el segundo *int* con el valor representado con un string "2". Yatel con
    esto convierte automáticamnte el segundo elemento al tipo entero

    Una version mas corta de la misma consulta seria:

    .. code-block:: javascript

        {
            "id": "someid",
            "function": {
                "name": "sum",
                "kwargs": {
                    "nw": {"type": "literal", "value": [1, 2]}
                }
            }
        }


    El resultado tiene la forma

    .. code-block:: javascript

        {
            'id': "someid",
            'error': false,
            'error_msg': '',
            'stack_trace': null,
            'result': {'type': 'float', 'value': 3.0}
        }

#. **Consultas anidadas**

    .. code-block:: javascript

        {
            "id": 1545454845,
            "function": {
                "name": "haplotype_by_id",
                "args": [
                    {
                        "type": "unicode",
                        "function": {
                            "name": "slice",
                            "kwargs": {
                                "iterable": {"type": "unicode",
                                             "value": "id_01_"},
                                "f": {"type": "int", "value": "-3"},
                                "t": {"type": "int", "value": "-1"}
                            }
                        }
                    }
                ]
            }
        }

    Esta consulta muesta realmente la potencia de QBJ. La primero que hay que
    notar es que la funcion principal, *haplotype_by_id*, recibe como primer
    argumento la resolucion de la función *slice*.
    El valor de la llave type dentro del argumento indica que el resultado de
    la funcion interna si no es un texto debe convertirse a el.

    *slice*, por otra parte, lo que hace es recortar el texto *id_01_* desde
    su posicion *-3* hasta la *-1*.

    si esto lo imaginaramos como codigo Python la funcion seria algo similar a

    .. code-block:: python

        haplotype_by_id(
            unicode(slice(iterable="id_01_", f=int("-3"), t=int("-1")))
        )

    o lo que es lo mismo

    .. code-block:: python

        haplotype_by_id("01")

    El resultado de esta consulta devolveria un *haplotipo* de la DB de la
    siguiente forma:

    .. code-block:: javascript

        {
            'id': "someid",
            'error': false,
            'error_msg': '',
            'stack_trace': null,
            'result': {
                'type': 'Haplotype',
                'value': {
                    'hap_id': {'type': 'int', 'value': 1},
                    'color': {'type': 'unicode', 'value': 'y'},
                    'description': {'type': 'unicode', 'value': '...'},
                    'height': {'type': 'float', 'value': 92.00891409813752},
                    'number': {'type': 'int', 'value': 16}
                }
            }
        }



Funciones
---------


El proceso de resolución
------------------------
