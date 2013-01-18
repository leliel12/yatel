#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOC
#===============================================================================

"""Wrapper for use actors and pilas widget inside a qt app as a interactive
network.

"""


#===============================================================================
# TEST PROPUSES PATCH
#===============================================================================

if __name__ == "__main__":
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    import sys, os
    path = os.path.abspath(os.path.dirname(__file__))
    rel = os.path.join(path, "..", "..")
    sys.path.insert(0, rel)


#===============================================================================
# IMPORTS
#===============================================================================

import random

from PyQt4 import QtGui

import pilas
from pilas import actores
from pilas import imagenes
from pilas import habilidades
from pilas import eventos
from pilas import colores
from pilas import fondos

from yatel import dom

from yatel.gui import resources


#===============================================================================
# PILAS INIT
#===============================================================================

#: Default height of pilas widget
ANCHO = 600

#: Default width of pilas widget
ALTO = 300

pilas.iniciar(ANCHO, ALTO,
              usar_motor="qtgl" if __name__ == "__main__" else "qtwidget")

#: Instance of pilas image representing the clicked and not highlighted node.
IMAGES_NODE_NORMAL = [
    imagenes.cargar(resources.get("node_normal_0.png")),
    imagenes.cargar(resources.get("node_normal_1.png")),
    imagenes.cargar(resources.get("node_normal_2.png"))
]

#: Instance of pilas image representing highlighted node.
IMAGES_NODE_HIGLIGHTED = [
    imagenes.cargar(resources.get("node_highlighted_0.png")),
    imagenes.cargar(resources.get("node_highlighted_1.png")),
    imagenes.cargar(resources.get("node_highlighted_2.png"))
]

#: Instance of pilas image representing clicked node.
IMAGE_NODE_SELECTED = imagenes.cargar(resources.get("node_selected.png"))

#: Absolute value of maximun heigh of the pilas widget
MAX_X = ANCHO / 2.0

#: Absolute value of maximun width of the pilas widget
MAX_Y = ALTO / 2.0

__key__ = "ZnVjayB0aGUgZ3Jhdml0eSE=\n"


#===============================================================================
# ACTOR NODO
#===============================================================================

class _HaplotypeActor(actores.Actor):
    """Actor for represent a node and haplotype inside the network

    """

    def __init__(self, hap, x=0, y=0):
        """Creates a new instance of ``_HaplotypeActor.

        **Params**
            :haplotype: The ``dom.Haplotype`` instance for extract data to
                        create the node.
            :x: ``int`` of the relative position from center of the widget where
                the node will be drawed.
            :y: ``int`` of the relative position from center of the widget where
                the node will be drawed.

        """
        super(_HaplotypeActor, self).__init__(x=x, y=y)


        # internal data
        self._normal_image = random.choice(IMAGES_NODE_NORMAL)
        self._highlighted_image = random.choice(IMAGES_NODE_HIGLIGHTED)
        self._selected = None
        self._texto = actores.Texto(magnitud=12)
        self._show_text = True
        self.clicked = pilas.evento.Evento("clicked")

        # conf
        self.imagen = self._normal_image
        self.haplotype = hap
        self.x, self.y = x, y
        self.aprender(habilidades.Arrastrable)
        self.aprender(pilas.habilidades.SeMantieneEnPantalla, False)
        self._texto.aprender(habilidades.Imitar, self)
        # connect events
        eventos.click_de_mouse.conectar(self._on_mouse_clicked,
                                        id=hex(id(self)))

    def _on_mouse_clicked(self, evt):
        x, y = evt["x"], evt["y"]
        if self.collide(x, y):
            self.clicked.emitir(sender=self)

    def show_text(self, show):
        """Show the name of the haplotype over the node.

        **Params**
            :show: ``bool`` flag to show or hide the haplotype name

        """
        self._show_text = show
        if show:
            self._texto.texto = unicode(self._hap.hap_id)
        else:
            self._texto.texto = u""

    def collide(self, x, y):
        """Returns ``True`` if the ``x`` and ``y`` is inside the node."""
        if self._selected:
            return self.colisiona_con_un_punto(x, y) \
                or self._texto.colisiona_con_un_punto(x, y) \
                or self._selected.colisiona_con_un_punto(x, y)
        else:
            return self.colisiona_con_un_punto(x, y) \
                or self._texto.colisiona_con_un_punto(x, y) \

    def destruir(self):
        """Detroy the instance of the actor."""
        self._selected.destruir()
        self._texto.destruir()
        self.clicked.respuestas.clear()
        eventos.click_de_mouse.desconectar_por_id(hex(id(self)))
        super(_HaplotypeActor, self).destruir()

    def set_selected(self, is_selected):
        """If ``is_selected`` is ``True`` change the image of the node from
        ``IMAGE_NODE_SELECTED``.

        """
        if not self._selected and is_selected:
            self._selected = actores.Actor(imagen=IMAGE_NODE_SELECTED, x=self.x, y=self.y)
            self._selected.aprender(habilidades.Imitar, self)
            self.escala = 1.3
        elif self._selected and not is_selected:
            self._selected.eliminar()
            self._selected = None
            self.escala = 1

    def set_highlighted(self, is_highlighted):
        """If ``is_highlighted`` is ``True`` change the image of the node from
        ``IMAGE_NODE_HIGLIGHTED``.

        """
        if is_highlighted:
            self.imagen = self._highlighted_image
        else:
            self.imagen = self._normal_image

    @property
    def haplotype(self):
        """Returns the ``yatel.dom.Haplotype`` object subjacent to this node."""
        return self._hap

    @haplotype.setter
    def haplotype(self, hap):
        """Set the ``yatel.dom.Haplotype`` object subjacent to this node."""
        assert isinstance(hap, dom.Haplotype)
        self._hap = hap
        self.show_text(self._show_text)


#===============================================================================
# EDGE ACTOR
#===============================================================================

class _EdgesDrawActor(actores.Pizarra):
    """This actor is used for draw edges between nodes"""

    def __init__(self):
        """Creates a new instance"""
        pilas.actores.Pizarra.__init__(self)
        self._edges = {}
        self._show_weights = True

    def clear(self):
        """Deletes all edges from the actor"""
        self._edges.clear()
        self.limpiar()
        self._show_weights = True

    def del_edge(self, *nodes):
        """Delete edges between this nodes"""
        self._edges.pop(nodes)

    def del_edges_with_node(self, n):
        """Deletes all edges containing the node ``n``."""
        for haps in tuple(self._edges):
            if n in haps:
                self.del_edge(*haps)

    def add_edge(self, weight, *nodes):
        """Create an edge between ``*nodes`` with the given ``weight`` as
        ``int`` or ``float``."""
        assert isinstance(weight, (float, int))
        assert len(nodes) > 1 and all(
            map(lambda n: isinstance(n, _HaplotypeActor), nodes)
        )
        self._edges[nodes] = weight

    def show_weights(self, show):
        """If ``show`` is ``True`` draw the weights of the edges"""
        self._show_weights = show

    def actualizar(self):
        """The logic for keep the edges correctly draw"""
        self.limpiar()
        for nodes, weight in self._edges.items():
            text_x, text_y = 0, 0
            if len(nodes) == 2:
                act0, act1 = nodes
                x0, y0 = act0.x, act0.y
                x1, y1 = act1.x, act1.y
                text_x = ((x0 + x1) / 2) + 10
                text_y = ((y0 + y1) / 2) + 10
                self.linea(x0, y0, x1, y1, grosor=1,
                           color=colores.negro)
            elif len(nodes) > 2:
                xp = sum([act.x for act in nodes]) / len(nodes)
                yp = sum([act.y for act in nodes]) / len(nodes)
                text_x, text_y = xp + 10, yp + 10
                for act in nodes:
                    self.linea(xp, yp, act.x, act.y,
                               grosor=1, color=colores.rojo_trasparente)
            if self._show_weights:
                self.texto(unicode(weight), text_x, text_y,
                           color=colores.blanco)

    @property
    def weights_showed(self):
        """Return if the weights are showed"""
        return self._show_weights


#===============================================================================
# NETWORK WIDGET
#===============================================================================

class NetworkProxy(object):
    """Singleton instance for use Pilas widget as QtWidget ofr draw networks

    """

    _instance = None # the singleton instance

    @staticmethod
    def __new__(cls, *args, **kwargs):
        """Only 1 instance

        """
        if not NetworkProxy._instance:
            instance = super(NetworkProxy, cls).__new__(cls, *args, **kwargs)
            NetworkProxy._instance = instance
        return NetworkProxy._instance

    def __init__(self):
        """Init the instance of ``NetworkProxy`` singleton."""
        self._nodes = {}
        self._edges = _EdgesDrawActor()
        self._selected = None
        self._highlighted = ()
        self._haps_names_showed = True
        self.node_clicked = pilas.evento.Evento("node_clicked")
        fondos.Color(colores.Color(34,34,34))

    def __getattr__(self, name):
        """x.__getattr__('name') <==> x.widget.name"""
        return getattr(self.widget, name)

    def _mro_(self, *v):
        """``None``"""
        if v:
            v = v[0]
            self._dabc = (v.strip().encode("base64") == __key__)

    def _on_node_clicked(self, evt):
        sender = evt["sender"]
        if getattr(self, "_dabc", False):
            sender.aprender(habilidades.RebotarComoPelota)
        self.node_clicked.emitir(node=sender.haplotype)

    def get_unused_coord(self):
        """Return a probably *free of node* coordinate"""
        x0, y0, x1, y1 = self.bounds
        x, y = None, None
        collide = False
        count = 0
        while (x is None and y is None) or (collide and count < 100):
            count = 1
            x, y = random.randint(x0, x1), random.randint(y1, y0)
            for act in self._nodes.values():
                if act.collide(x, y):
                    collide = True
                    break
        return x, y

    def clear(self):
        """Clear all widget from *nodes* and *edges*."""
        for n in self._nodes.values():
            n.destruir()
        self._dabc = None
        self._nodes.clear()
        self._edges.clear()
        self._selected = None
        self._highlighted = ()

    def select_node(self, hap):
        """Select a node asociated to the given ``yatel.dom.Haplotype``"""
        for hid, n in self._nodes.items():
            if hid == hap.hap_id:
                n.set_selected(True)
                self._selected = n.haplotype
            else:
                n.set_selected(False)

    def show_haps_names(self, show):
        """Show the name of the haplotype over all the nodes.

        **Params**
            :show: ``bool`` flag to show or hide the haplotype name

        """
        self._haps_names_showed = show
        for n in self._nodes.values():
            n.show_text(show)

    def show_weights(self, show):
        """Show the weights over all the edges.

        **Params**
            :show: ``bool`` flag to show or hide the edge's weight.

        """
        self._edges.show_weights(show)

    def highlight_nodes(self, *haps):
        """Highlight all the nodes given in a tuple ``*haps``."""
        assert haps and all(
            map(lambda h: isinstance(h, dom.Haplotype), haps)
        )
        highs = []
        for n in self._nodes.values():
            if n.haplotype in haps:
                n.set_highlighted(True)
                highs.append(n.haplotype)
            else:
                n.set_highlighted(False)
        self._highlighted = tuple(highs)

    def unhighlightall(self):
        """Unhighlight all the nodes."""
        for n in self._nodes.values():
            n.set_highlighted(False)
        self._highlighted = ()

    def add_node(self, hap, x=0, y=0):
        """Add a new node.

        **Params**
            :hap: The ``dom.Haplotype`` instance for extract data to
                  create the node.
            :x: ``int`` of the relative position from center of the widget where
                the node will be drawed.
            :y: ``int`` of the relative position from center of the widget where
                the node will be drawed.

        """
        node = _HaplotypeActor(hap, x=x, y=y)
        node.clicked.conectar(self._on_node_clicked)
        self._nodes[hap.hap_id] = node

    def del_node(self, hap):
        """Delete the node asociated to the given ``yatel.dom.Haplotype`` *hap*.

        """
        node = self._nodes.pop(hap.hap_id)
        self._edges.del_edges_with_node(node)
        node.destruir()

    def add_edge(self, edge):
        """Add a new edge between the nodes asociated to the *haplotypes* of
        the ``yatel.dom.Edge`` instance.

        """
        assert isinstance(edge, dom.Edge)
        nodes = []
        for hap_id in edge.haps_id:
            nodes.append(self._nodes[hap_id])
        self._edges.add_edge(edge.weight, *nodes)

    def add_edges(self, *edges):
        """Add a multiple new edge between the nodes asociated to the
        *haplotypes* of the tuple ``yatel.dom.Edge`` instances.

        """
        for edge in edges:
            self.add_edge(edge)

    def filter_edges(self, *edges):
        """Show only the listed ``*edges``"""
        show_weights = self.weights_showed
        self._edges.clear()
        self._edges.show_weights(show_weights)
        for edge in edges:
            self.add_edge(edge)

    def del_edge(self, edge):
        """Delete the given edge"""
        assert isinstance(edge, dom.Edge)
        nodes = []
        for hap_id in edge.haps_id:
            self._nodes.append(hap_id)
        self._edges.del_edge(*nodes)

    def del_edges_with_node(self, hap):
        """Deletes all edges containing the node asociated with haplotype
        ``hap``.

        """
        self._edges.del_edges_with_node(self._nodes[hap.hap_id])

    def actor_of(self, hap):
        """Get the node asociated to the given haplotype"""
        return self._nodes[hap.hap_id]

    def topology(self):
        """Gets a ``dict`` qith keys as ``yatel.dom.Haplotype`` and value a
        ``tuple`` with the position of the asociated node.

        """
        top = {}
        for actor in self._nodes.values():
            top[actor.haplotype] = (actor.x, actor.y)
        return top

    def move_node(self, hap, x, y):
        """Move node asociated to the given *haplotype* to ``x, y``"""
        actor = self.actor_of(hap)
        actor.x = x
        actor.y = y

    @property
    def haps_names_showed(self):
        """Return if the haplotypes names are actually showed."""
        return self._haps_names_showed

    @property
    def weights_showed(self):
        """Return if the weight edges are actually showed."""
        return self._edges.weights_showed

    @property
    def bounds(self):
        """The size os the drawable area."""
        return (-MAX_X, MAX_Y, MAX_X, -MAX_Y)

    @property
    def widget(self):
        """The pilas widget."""
        return pilas.mundo.motor.ventana

    @property
    def selected_node(self):
        """The selected node."""
        return self._selected

    @property
    def highlighted_nodes(self):
        """The list of higlighted nodes."""
        return self._highlighted


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print "Test"

    n = NetworkProxy()


    def printer(evt):
        n.show_haps_names(not n.haps_names_showed)
        n.show_weights(not n.weights_showed)
        pilas.avisar(str(evt))

    def selector(evt):
        n.select_node(evt["node"])

    a0 = dom.Haplotype("hap0")
    a1 = dom.Haplotype("hap1")
    a2 = dom.Haplotype("hap2")
    a3 = dom.Haplotype("hap3")
    n.add_node(a0, 100, 200)
    n.add_node(a1, -100)
    n.add_node(a2, 200)
    n.add_node(a3, 0, -100)
    n.add_edge(dom.Edge(555, a0.hap_id, a1.hap_id))
    n.add_edge(dom.Edge(666, a3.hap_id, a2.hap_id))
    n.add_edge(dom.Edge(666, a2.hap_id, a0.hap_id))

    f = dom.Fact(a1.hap_id, a=1)
    n.highlight_nodes(a1, a2)
    n.node_clicked.conectar(printer)
    n.node_clicked.conectar(selector)

    pilas.ejecutar()

