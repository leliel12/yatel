=================
Yatel Yaml Format
=================

The *Yatel Yaml Format* (or yyf) is a YAML_ based file format for export Yatel
graphs.


File Extension
--------------

We recommend to use **.yyf** as Yatel Yaml Format file extension.

Yatel Gui also support *.yaml* and *.yml*.


Declaration
-----------

The version `0.1` of the format has four elements on the root of declaration.

- ``version``: A string with the version of the format (actually *0.1*)

  example:

  .. code-block:: yaml

        version: "0.1"

- ``haplotypes``: A list of objects representing ``yatel.dom.Haplotype``
  instances.

  Every object and has a ``hap_id`` key containing a string with the unique id
  of this haplotype; all the other elements has arbitrary data types and values
  representing all the attributes of the haplotype.

  Also maybe two haplotypes hasn't the same attributes, but if it two or more
  has the same attribute name the value must be of the same type.

  example:

  .. code-block:: yaml

        haplotypes:
            - hap_id: "hap0"
              name: "the good"
              has_color: false
            - hap_id: "hap1"
              name: "the bad"
              has_color: true


- ``facts``: A list of objects representing ``yatel.dom.Fact`` instances.

  Every object and has a ``hap_id`` key containing a string with the unique id
  of his haplotype; all the other elements has arbitrary data types and values
  representing all the meta-attributes of the haplotype.

  Also maybe two haplotypes hasn't the same attributes, but if it two or more
  has the same attribute name the value must be of the same type.

  example:

  .. code-block:: yaml

        facts:
            - hap_id: "hap02"
              place: "Rio IV"
              weather: "Rain"
              year: 2012
            - hap_id: "hap0"
              found_by: "Armando Estaban Quito"
              place: "Rio III"
              weather: "Cold"
              year: 2011
            - hap_id: "hap1"
              found_by: "Nadia Luczywo"
              place: "Cordoba Argentina"
              weather: "Rain"
              year: 1998


- ``edge``: A list of objects representing ``yatel.dom.Edge`` instances.

  Every object and has a ``weight`` key containing a float of the value of the
  edge and ``haps_id`` containing a list of string of the haplotypes that this
  edge links.

  example:

  .. code-block:: yaml

        edges:
            - weight: 10
              haps_id:
                  - "hap0"
                  - "hap1"
            - weight: 30
              haps_id:
                  - "hap0"
                  - "hap1"

Full example
------------

.. code-block:: yaml

    # this is an example of Yatel Yaml Format or YYF
    version: "0.1"

    haplotypes:
        - hap_id: "hap0"
          name: "the good"
          has_color: false
        - hap_id: "hap1"
          name: "the bad"
          has_color: true


    facts:
        - hap_id: "hap02"
          place: "Rio IV"
          weather: "Rain"
          year: 2012
        - hap_id: "hap0"
          found_by: "Armando Estaban Quito"
          place: "Rio III"
          weather: "Cold"
          year: 2011
        - hap_id: "hap1"
          found_by: "Nadia Luczywo"
          place: "Cordoba Argentina"
          weather: "Rain"
          year: 1998

    edges:
        - weight: 10
          haps_id:
              - "hap0"
              - "hap1"
        - weight: 30
          haps_id:
              - "hap0"
              - "hap1"



.. _YAML: http://yaml.org/
