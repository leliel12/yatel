#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# TEST PROPUSES PATCH
#===============================================================================

if __name__ == "__main__":
    import sys, os
    path = os.path.abspath(os.path.dirname(__file__))
    rel = os.path.join(path, "..", "..")
    sys.path.insert(0, rel)


#===============================================================================
# IMPORTS
#===============================================================================

import pilas
from pilas import actores
from pilas import imagenes
from pilas import habilidades
from pilas import eventos
from pilas import colores

from PyQt4 import QtCore

from yatel import dom

from yatel.gui import resources


#===============================================================================
# PILAS INIT
#===============================================================================

pilas.iniciar()


#===============================================================================
# CONSTANTS
#===============================================================================

IMAGE_NODE_NORMAL = pilas.imagenes.cargar(
    resources.get("node_normal.svg")
)

IMAGE_NODE_HIGLIGHTED = pilas.imagenes.cargar(
    resources.get("node_highlighted.svg")
)

IMAGE_NODE_SELECTED = pilas.imagenes.cargar(
    resources.get("node_selected.svg")
)

IMAGE_EMPTY = pilas.imagenes.cargar(
    resources.get("empty.svg")
)

#===============================================================================
# ACTOR NODO
#===============================================================================

class _HaplotypeActor(actores.Actor):
    
    def __init__(self, hap, x=0, y=0):
        super(_HaplotypeActor, self).__init__(
            imagen=IMAGE_NODE_NORMAL,
            x=x, y=y
        )
        
        # internal data
        self._selected = actores.Actor(imagen=IMAGE_EMPTY)
        self._texto = actores.Texto()
        self.clicked = eventos.Evento("clicked")
        
        # conf
        self.haplotype = hap
        self.x, self.y = x, y
        self.aprender(habilidades.Arrastrable)
        self._texto.aprender(habilidades.Imitar, self)
        self._selected.aprender(habilidades.Imitar, self)
        
        # connect events
        eventos.click_de_mouse.conectar(self._on_mouse_clicked)
        
    def _on_mouse_clicked(self, evt):
        x, y = evt["x"], evt["y"]
        if self.colisiona_con_un_punto(x, y) \
            or self._texto.colisiona_con_un_punto(x, y) \
            or self._selected.colisiona_con_un_punto(x,y):
                self.clicked.emitir(sender=self)
    
    def destruir(self):
        self._selected.destruir()
        self._texto.destruir()
        super(_HaplotypeActor, self).destruir()
    
    def set_selected(self, is_selected):
        if is_selected:
            self._selected.imagen = IMAGE_NODE_SELECTED
        else:
            self._selected.imagen = IMAGE_EMPTY
        
    def set_highlighted(self, is_highlighted):
        if is_highlighted:
            self.imagen = IMAGE_NODE_HIGLIGHTED
        else:
            self.imagen = IMAGE_NODE_NORMAL
    
    @property
    def haplotype(self):
        return self._hap
        
    @haplotype.setter
    def haplotype(self, hap):
        assert isinstance(hap, dom.Haplotype)
        self._hap = hap
        self._texto.texto = unicode(self._hap.hap_id)
        

#===============================================================================
# EDGE ACTOR
#===============================================================================

class _EdgesDrawActor(actores.Pizarra):

    def __init__(self):
        pilas.actores.Pizarra.__init__(self)
        self._edges = {}

    def clear(self):
        self._edges.clear()
        self.limpiar()

    def del_edge(self, *nodes):
        self._edges.pop(nodes)
        
    def del_edges_with_node(self, n):
        for haps in tuple(self._edges):
            if n in haps:
                self.del_edge(*haps)

    def add_edge(self, weight, *nodes):
        assert isinstance(weight, (float, int))
        assert len(nodes) > 1 and all(
            map(lambda n: isinstance(n, _HaplotypeActor), nodes)
        )
        self._edges[nodes] = weight

    def actualizar(self):
        self.limpiar()
        for nodes, weight in self._edges.items():
            text_x, text_y = 0, 0
            if len(nodes) == 2:
                act0, act1 = nodes
                x0, y0 = act0.x, act0.y
                x1, y1 = act1.x, act1.y
                text_x = ((x0 + x1) / 2) + 10
                text_y = ((y0 + y1) / 2) + 10
                self.linea(x0, y0, x1, y1, grosor=2)
            elif len(nodes) > 2:
                xp = sum([act.x for act in nodes]) / len(nodes)
                yp = sum([act.y for act in nodes]) / len(nodes)
                text_x, text_y = xp + 10, yp + 10
                for act in nodes:
                    self.linea(
                        xp, yp, act.x, act.y, 
                        grosor=2, color=colores.rojo
                    )
            self.texto(
                unicode(weight), text_x, text_y, color=colores.verdeoscuro
            )


#===============================================================================
# NETWORK WIDGET
#===============================================================================

class NetworkWidget(object):
    
    def __init__(self):
        self._nodes = {}
        self._edges = _EdgesDrawActor()
        self._selected = None
        self._highlighted = ()
        self.node_selected = eventos.Evento("node_selected")

    def _on_node_clicked(self, evt):
        sender = evt["sender"]
        self.select_node(sender.haplotype)
        self.node_selected.emitir(node=sender.haplotype)

    def clear(self):
        self._nodes.clear()
        self._eges.clear()
        self._selected = None
        self._highlighted = ()
    
    def select_node(self, hap):
        for hid, n in self._nodes.items():
            if hid == hap.hap_id:
                n.set_selected(True)
                self._selected = n
            else:
                n.set_selected(False)

    def highlight_nodes(self, *haps):
        pass
        """highs = []
        for h, n in self._nodes.items():
            if h in haps:
                n.set_highlighted(True)
                highs.append(h)
            else:
                n.set_highlighted(False)
        self._highlighted = tuple(highs)"""
                
    def add_node(self, hap, x=0, y=0):
        node = _HaplotypeActor(hap, x=x, y=y)
        node.clicked.conectar(self._on_node_clicked)
        self._nodes[hap.hap_id] = node
        
    def del_node(self, hap):
        node = self._nodes.pop(hap.hap_id)
        self._edges.del_edges_with_node(node)
        node.destruir()
        
    def add_edge(self, edge):
        assert isinstance(edge, dom.Edge)
        nodes = []
        for hap_id in edge.haps_id:
            nodes.append(self._nodes[hap_id])
        self._edges.add_edge(edge.weight, *nodes)
        
    def add_edges(self, *edges):
        for edge in edges:
            self.add_edge(edge)
        
    def del_edge(self, edge):
        assert isinstance(edge, dom.Edge)
        nodes = []
        for hap_id in edges.haps_id:
            self._nodes[hap_id]
        self._edges.del_edge(*nodes)
        
    def del_edges_with_node(self, hap):
        self._edges.del_edges_with_node(self._nodes[hap.hap_id])
        
    def node_of(self, hap):
        return self._nodes[hap.hap_id]
        
    @property
    def selected_node(self):
        return self._selected.haplotype if self._selected else None
        
    @property
    def highlighted_node(self):
        return self._highlighted


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    
    def printer(evt):
        pilas.avisar(str(evt))
    
    n = NetworkWidget()
    
    a0 = dom.Haplotype("hap0")
    a1 = dom.Haplotype("hap1")
    a2 = dom.Haplotype("hap2")
    a3 = dom.Haplotype("hap3")
    n.add_node(a0, 100, 200)
    n.add_node(a1, -100)
    n.add_node(a2, 200)
    n.add_node(a3, 0,-100)
    n.add_edge(dom.Edge(555, a0.hap_id, a1.hap_id, a2.hap_id, a3.hap_id))
    n.add_edge(dom.Edge(666, a3.hap_id, a2.hap_id))

    n.select_node(a1)
    n.select_node(a0)
    
    n.node_selected.conectar(printer)
    
    
    
    pilas.ejecutar()
    
