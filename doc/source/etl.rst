Yatel ETL Framework
===================

One of the main problems faced of data warehouses oriented to analysis is the 
way in which their data is loaded or updated incrementally.

The technique used is known as ETL_, which roughly consists in **Extract** 
data from source, **Transform** them to make sense in the context of our 
warehouse, and finally **Load** them to our database.

Yatel provides a modest framework for creating ETL for loading NW-OLAP 
consistently.

Creation of a full ETL
^^^^^^^^^^^^^^^^^^^^^^

The first step in creating a ETL is using Yatel to generate us a template on 
which to work in a file name, for example,

.. code-block:: bash

    $ yatel createetl myetl.py


If we open it we will see the following code

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


.. note:: As a condition should be clarified that whenever the command line 
          tools the class with the ETL_ to be called must be called 
          ``ETL`` (Line 13).


.. note:: It is good practice to have only one ETL per file, to prevent 
          problems at the time of execution and jeopardize the consistency of 
          your data wharehouse.


- Line 6 are the imports used without exception in all the ETL
- Line 13 creates the ETL class that will contain the logic for extraction, 
  transformation and load of the data



Should be noted that there are many methods that can be overridden (there is a 
sectino for ahead) but the ones that are mandatory to redefine are the 
generators: ``haplotype_gen``, ``edge_gen``, ``fact_gen``.


- ``haplotype_gen`` (line 21) must return an iterable or in the best of cases 
  a generator of haplotypes that you want to load into the database. For 
  example we may decide that the haplotypes are read of a CSV_ using the csv 
  module of Python:

  .. code-block:: python

    def haplotype_gen(self):
        with open("haplotypes.csv") as fp:
            reader = csv.reader(fp)
            for row in reader:
                hap_id = row[0] # assume that the id is in the first column
                name = row[1] # assume that the column 1 has an attribute name
                yield dom.Haplotype(hap_id, name=name)


  As is very common to use these haplotypes in the following functions, the ETL
  is responsible for storing them in a variable named **haplotypes_cache**. 
  This cache is a **dict-like** whose key are ``hap_id`` and the values of the 
  haplotypes themselves (cache manipulationhas it's own section ahead).


- ``edge_gen`` (line 24) must return an iterable or in the best of cases 
  a generator of edges that you want to load into the database. It is normal 
  to want to use the haplotypes cache for comparison and give the right weight 
  to each edge. To compare each happlotype with all the rest but itself we can 
  use the function **itertools.combinations**  that comes with Python (if 
  someone would want to compare the haplotypes with itself we can use another 
  function **itertools.combinations.with_replacement**). Finally the weight 
  given by the 
  `hamming distance <http://en.wikipedia.org/wiki/Hamming_distance>`_ between 
  two haplotypes using the **weights** module in Yatel:


  .. code-block:: python

    def edge_gen(self):
        # we combine  haplotypes by two
        for hap0, hap1 in itertools.combinations(self.haplotypes_cache.values(), 2):
            w = weight.weight("hamming", hap0, hap1)
            haps_id = hap0.hap_id, hap1.hap_id
            yield dom.Edge(w, haps_id)


- ``fact_gen`` (line 27) must return an iterable or in the best of cases 
  a generator of facts that you want to load into the database.
  Normally the greater complexity of the ETL is in this function.
  We can imagine in our case (to add some complexity to this example) that the
  facts com from a JSON_, whose main element is an object and its keys are 
  equivalent to the attribute **name** of each haplotype; the values ​​in turn 
  are an array which each one must be a **fact** of said haplotype. A simple 
  example would be:


  .. code-block:: javascript


        {
            "hap_name_0": [
                {"year": 1978, "description": "something..." },
                {"year": 1990},
                {"notes": "some notes", "year": 1986},
                {"year": 2014, "active": false}
            ],
            ...
        }


  So the function to process the data must first determine what the ``hap_id`` 
  for each haplotype is before creating fact. We could (by a matter of ease) 
  save a *dict* whose value is the *name* of the haplotype (assuming it's 
  unique) and the value of *hap_id*. To not do useless loops we can do it 
  directly in the method ``haplotype_gen`` with which would be as follows:


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

  Now we can easily create the facts using the json module in Python.


  .. code-block:: python

    def fact_gen(self):
        with open("facts.json", "rb") as fp:
            data = json.load(fp)
            for hap_name, facts_data in data.items():
                hap_id = self.name_to_hapid[hap_name]
                for fact_data in facts_data:
                    yield dom.Fact(hap_id, **fact_data)


Finally having a destination database we can load it with our ETL with the 
command:

.. code-block:: bash

    $ yatel runetl sqlite:///my_database.db my_etl.py


Initializer and cleanup of an ETL
---------------------------------

It may be necessary in some cases your ETL needs some resources and it is 
convenient that they are freed at the finish of the process (a connection to a 
database for example); or otherwise create global variables to the methods.

For this cases Yatel has two extra methods than can be redefined in your ETL:

- ``setup`` which is executed before **all** other methods in the ETL. Added 
  to this; also can receive positional parameters (variable parameters and 
  those with default values are not accepted) wich can be given through the 
  command line.
- ``teardown`` this method is executed at the end of all processing and is 
  the last responsible for leaving the system in a stable estate after 
  freeing all resources of the ETL execution.


In our example, We might want to write the time of start and end of the ETL 
execution (obtained with the *time* module in Python) into a file given as 
a parameter. This is really a better place to declare *dict* ``name_to_hapid`` 
that will be used with the haplotypes and facts. the two functions have the 
form:


.. code-block:: python

    def setup(self, filename):
        self.fp = open(filename, "w")
        self.name_to_hapid = {}
        self.fp.write(str(time.time()) + "\n")

    def teardown(self):
        self.fp.write(str(time.time()) + "\n")
        self.fp.close()


Finally to run our ETL we should use the command passing it parameters for 
the setup


.. code-block:: bash

    $ yatel runetl sqlite:///my_database.db my_etl.py timestamps.log


.. note:: Should be pointed that all the parameters arriving to ``setup`` do 
          as text and must be converted to the extent necessary.



Intermediate functions to generators
------------------------------------

While it is not commonly use, the ETL has six more methods that give more 
atomic control of the ETL. Each one of them are executed right before and 
after each generator, they are:

- ``pre_haplotype_gen(self)`` executed right before *haplotype_gen*.
- ``post_haplotype_gen(self)`` executed right after *haplotype_gen*.
- ``pre_edge_gen(self)`` executed right before *edge_gen*.
- ``post_edge_gen(self)`` executed right after *edge_gen*.
- ``pre_fact_gen(self)`` executed right before *fact_gen*.
- ``post_fact_gen(self)`` executed right after *fact_gen*.


Error Handling
--------------

In case of encountering an error in the processing of an ETL, a method can be 
overridden to treat it: ``handle_error(exc_type, exc_val, exc_tb)``

The parameters that ``handle_error`` receives are equivalent to the exit from 
a context manager where: *exc_type* is the error class (exception) that 
happened, *exc_val* its the exception itself and *exc_tb* its the error 
traceback.

Yes, this method 
Si este mètodo suspends all execution of ETL (even ``teardown``)


.. note:: ETL **ARENT** context managers.

.. note:: ``handle_error`` should **NEVER** relaunch the exception that 
          reaches it as parameter. If you want to silence said exception 
          simply return ``True`` or a true value, otherwise the exception 
          will propagate.


For example if we want to silence the exception only if it is TypeError


.. code-block:: python

    def handle_error(self, exc_type, exc_val, exc_tb):
        return exc_type == TypeError


Haplotypes cache
----------------

The last functionality that can be altered in a ETL is the operation of the 
cache haplotypes, for example if the haplotypes are too many to keep in 
memory at the same time we could replace the double dictionary (internal 
cache and the one that links names with its id) by a single cache that 
contains the data internally neatly.

The ETL use as cache classes that inherit from ``collections.MutableMapping``.

.. code-block:: python

    import collections

    class DoubleDictCache(collections.MutableMapping):

        def __init__(self, path):
            self.by_hap_id = {}
            self.name_to_hap_id = {}

        # all this methods have to be redefined in a mutable mapping
        def __delitem__(self, hap_id):
            hap = self.by_hap_id.pop(hap_id)
            self.name_to_hap_id.pop(hap.name)

        def __getitem__(self, hap_id):
            return self.by_hap_id[hap_id]

        def __iter__(self):
            return iter(self.by_hap_id)

        def __len__(self):
            return len(self.by_hap_id)

        def __setitem__(self, hap_id, hap):
            self.by_hap_id[hap_id] = hap
            self.name_to_hap_id[hap.name] = hap_id

        def get_hap_id(self, name):
            return self.name_to_hap_id[name]

To use this class level cache of the ETL we need to redefine an attribute 
called ``HAPLOTYPES_CACHE``
Para utilizar este cache a nivel de clase del ETL hay que redefinir un atributo
que se llama ``HAPLOTYPES_CACHE`` and have the class value 
``DoubleDictCache``.

.. note:: If you want to disable the cache completely, put the value of 
          ``HAPLOTYPES_CACHE`` as *None*

In our example the code would be:

.. code-block:: python

    class ETL(etl.BaseETL):

        HAPLOTYPES_CACHE = DoubleDictCache

        ...

.. note:: Note that it may be required depends on the size of your cache that 
          suits you to implement something on a key value database (Riak_ o 
          Redis_), OO (ZODB_) or directly
          Tenga en cuenta que es posible que sea necesario depende el tamaño de
          su cache que le convenga implementar algo sobre una base de datos
          llave valor (Riak_ o Redis_), OO (ZODB_) or directly a relational 
          database lia a small SQLite_


Full example
------------

Full example code can be seen `here <_static/examples/myetl.zip>`_


Life cycle of a ETL
^^^^^^^^^^^^^^^^^^^

#. First it verifies that the class inherits from :py:class:``yatel.etl.BaseETL``.
#. Cache class is extracted and if is not found disabled.
#. If cache class is:
    #. ``None`` no cache is created.
    #. ``!= None`` it verifies that is a subclass of 
       ``collections.MutableMapping`` then an instance is created and asigned 
       to the etl in ``haplotypes_cache`` variable.
#. The ``db.YatelNetwork`` instance is assigned to the variable ``nw`` in the 
   ETL.
#. ``setup`` method of the ETL is executed passing all arguments.
#. ``pre_haplotype_gen`` is executed.
#. Iterating over the ``dom.Haplotype`` that returns ``haplotype_gen`` and 
   they are added to the database. If something is returned at some point 
   other than a ``dom.Haplotype`` an ``TypeError`` is thrown. If there is a cache 
   each ``dom.Haplotype`` is assigned to the cache putting the key as 
   *hap_id* and for value the *Haplotype*.
#. ``post_haplotype_gen`` is executed.
#. ``pre_edge_gen`` is executed.
#. Iterating over the ``dom.Edge`` that returns ``edge_gen`` and they are 
   added to the database. If something is returned at some point other than a 
   ``dom.Edge`` an ``TypeError`` is thrown.
#. ``post_edge_gen`` is executed.
#. ``pre_fact_gen`` is executed.
#. Iterating over the ``dom.Fact`` that returns ``fact_gen`` and they are 
   added to the database. If something is returned at some point other than a 
   ``dom.Fact`` an ``TypeError`` is thrown.
#. ``post_fact_gen`` is executed.
#. ``teardown`` is executed.
#. Returns ``True``.

**If something Fails**

A. ``handle_error`` is executed passing it the error information. if 
   ``handle_error`` returns ``False`` the exception is not stopped.
B. Returns ``None``.

.. warning:: If you are running your ETL directly using the function 
             ``etl.execute`` changes are not confirmed and It is your 
             responsibility to run ``nw.confirm_changes()``.

             If on the other hand you are running with the command line the 
             confirmation is run only if ``etl.execute`` does not fail at any 
             time.


Running a ETL in a cronjob
^^^^^^^^^^^^^^^^^^^^^^^^^^

It is highly recommended that before running an ETL to always backup the data 
for that we suggest the following scripts (for windows and posix) that 
facilitate this task.


**Sugested *bash* (posix) script**

.. code-block:: bash

    #!/usr/bin/sh
    # -*- coding: utf-8 -*-


    DATABASE="engine://your_usr:your_pass@host:port/database";
    BACKUP_TPL="/path/to/your/backup.xml";
    ETL="/path/to/your/etl_file.py";
    LOGFILE="/var/yatel/log.txt"

    yatel backup $DATABASE $BACKUP_TPL --log --full-stack 2> $LOGFILE;
    yatel runetl $DATABASE $ETL --log --full-stack 2> $LOGFILE;


**Sugested *bat* (Windows) script**

.. code-block:: bat

    set BACKUP_TPL=c:\path\to\your\backup.json
    set ETL=c:\path\to\your\etl_file.py
    set DATABASE=sqlite://to/thing
    set LOGFILE=logfile.txt

    yatel backup %DATABASE% %BACKUP_TPL% --log --full-stack 2> %LOGFILE%;
    yatel runetl %DATABASE% %ETL% --log --full-stack 2> %LOGFILE%;
