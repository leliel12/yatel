Quick Start
===========

¿Que es Yatel?
--------------

**Pequeña descripcion de que es Yatel**

Caso de estudio (ejemplo)
-------------------------

Supongamos que tenemos el siguiente problema:

.. image:: imagen_al_grafico

Tenemos tres lugares llamados Córdoba, cada uno separada de la otro
por una determinada distancia.

Cargando el problema en Yatel
-----------------------------

Cargamos el anterior modelo en yatel, de la siguiente manera::

    from yatel import dom, db
    from pprint import pprint
    # postgres, oracle, mysql, and many more
    nw = db.YatelNetwork("memory", mode="w")
    elems = [
        dom.Haplotype(0, name="Cordoba"), # left
        dom.Haplotype(1, name="Cordoba"), # right
        dom.Haplotype(2, name="Cordoba"), # bottom
        
        dom.Edge(6599, (0, 1)),
        dom.Edge(8924, (1, 2)),
        dom.Edge(9871, (2, 0)),
        
        dom.Fact(0,name="Andalucia", lang="sp", timezone="utc-3"),
        dom.Fact(1, lang="sp"),
        dom.Fact(1, timezone="utc-6"),
        dom.Fact(2, name="Andalucia", lang="sp", timezone="utc"),
        
    ]
    nw.add_elements(elems)
    nw.confirm_changes()

**Descripción de que estamos haciendo en las lineas anteriores.**

Modelos y atributos
^^^^^^^^^^^^^^^^^^^

Mostramos la descripción::

    descriptor =  nw.describe()
    
    pprint(dict(descriptor))
    
    {'edge_attributes': {u'max_nodes': 2, u'weight': <type 'float'>},
     'fact_attributes': {'hap_id': <type 'int'>,
                         'lang': <type 'str'>,
                         'name': <type 'str'>,
                         'timezone': <type 'str'>},
     'haplotype_attributes': {'hap_id': <type 'int'>, 'name': <type 'str'>},
     'mode': 'r',
     'size': {u'edges': 3, u'facts': 4, u'haplotypes': 3}
    }

Mostramos los haplotipos::

    for hap in nw.haplotypes():
        print hap

    <Haplotype (0) at 0x24faa50>
    <Haplotype (1) at 0x24eae50>
    <Haplotype (2) at 0x24fa990>

Mostramos los arcos::

    for edge in nw.edges():
        print edge

    <Edge ([6599.0 [0, 1]]  ) at 0x1f64c50>
    <Edge ([8924.0 [1, 2]]  ) at 0x24fa0d0>
    <Edge ([9871.0 [2, 0]]  ) at 0x1f64c50>

Mostramos los hechos::

    for fact in nw.facts():
        print fact

    <Fact (of Haplotype '0') at 0x24eae50>
    <Fact (of Haplotype '1') at 0x24fad10>
    <Fact (of Haplotype '1') at 0x24eae50>
    <Fact (of Haplotype '2') at 0x24fad10>

Consultas
^^^^^^^^^

Ahora pasemos a las consultas::

    hap = nw.haplotype_by_id(2)
    
Arcos por haplotipo::

    for edge in nw.edges_by_haplotype(hap):
        print edge

    <Edge ([9871.0 [2, 0]]  ) at 0x24fa710>
    <Edge ([8924.0 [1, 2]]  ) at 0x1f64c50>

Hechos por haplotipo::

    for fact in nw.facts_by_haplotype(hap):
        print dict(fact)

    {u'lang': u'sp', u'timezone': u'utc', 'hap_id': 2, u'name': u'Andalucia'}

Haplotipos por el ambiente lang::

    for hap in nw.haplotypes_by_enviroment(lang="sp"):
        print hap

    <Haplotype (0) at 0x24fa2d0>
    <Haplotype (1) at 0x25c5350>
    <Haplotype (2) at 0x24fa2d0>

Haplotipos por el ambiente timezone::

    for hap in nw.haplotypes_by_enviroment(timezone="utc-6"):
        print hap

    <Haplotype (1) at 0x24eae50>

Haplotipos por el ambiente name::

    for hap in nw.haplotypes_by_enviroment(name="Andalucia"):
        print hap

    <Haplotype (0) at 0x25c5350>
    <Haplotype (2) at 0x24eae50>

Arcos por el ambiente Andalucia::

    for edge in nw.edges_by_enviroment(name="Andalucia"):
        print edge

    <Edge ([9871.0 [2, 0]]  ) at 0x24fa7d0>

Todos los ambientes::

    for env in nw.enviroments():
        print env

    <Enviroment {u'lang': u'sp', u'timezone': u'utc-3', u'name': u'Andalucia'} at 0x24faad0>
    <Enviroment {u'lang': u'sp', u'timezone': None, u'name': None} at 0x24db490>
    <Enviroment {u'lang': None, u'timezone': u'utc-6', u'name': None} at 0x24faad0>
    <Enviroment {u'lang': u'sp', u'timezone': u'utc', u'name': u'Andalucia'} at 0x24db490>

Estadisticas
^^^^^^^^^^^^

Veamos algunas estadisticas::

    from yatel import stats

Promedio::

    print stats.average(nw)
    8464.66666667

Std::

    print stats.std(nw, name="Andalucia")
    0.0                                                                         # Porque esto me da 0? esperaba 1374.70877724

Mineria de datos
^^^^^^^^^^^^^^^^

Pasemos a mineria de datos::

    from scipy.spatial.distance import euclidean
    from yatel.cluster import kmeans

    cbs, distortion = kmeans.kmeans(nw, nw.enviroments(), 2)

    for env in nw.enviroments():
        coords = kmeans.hap_in_env_coords(nw, env)
        min_euc = None
        closest_centroid = None
        for cb in cbs:
            euc = euclidean(cb, coords)
            if min_euc is None or euc < min_euc:
            min_euc = euc
            closest_centroid = cb
        print "{} || {} || {}".format(dict(env), closest_centroid, euc)

    {u'lang': u'sp', u'timezone': u'utc-3', u'name': u'Andalucia'} || [0 0 0] || 1.0
    {u'lang': u'sp', u'timezone': u'utc-3', u'name': u'Andalucia'} || [0 0 0] || 1.41421356237
    {u'lang': u'sp', u'timezone': None, u'name': None} || [0 0 0] || 1.0
    {u'lang': u'sp', u'timezone': None, u'name': None} || [0 1 0] || 0.0
    {u'lang': None, u'timezone': u'utc-6', u'name': None} || [0 0 0] || 1.0
    {u'lang': None, u'timezone': u'utc-6', u'name': None} || [0 1 0] || 0.0
    {u'lang': u'sp', u'timezone': u'utc', u'name': u'Andalucia'} || [0 0 0] || 1.0
    {u'lang': u'sp', u'timezone': u'utc', u'name': u'Andalucia'} || [0 0 0] || 1.41421356237
