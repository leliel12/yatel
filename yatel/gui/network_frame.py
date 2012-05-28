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
        self._texto = actores.Texto()
        self._selected = actores.Actor(image=IMAGE_NODE_SELECTED)
        
        # conf
        self.haplotype = hap
        self.x, self.y = x, y
        self.aprender(habilidades.Arrastrable)
        self._texto.aprender(habilidades.Imitar, self)
        self._selected.aprender(habilidades.Imitar, self)
        self._selected.trasparencia = 100
        
    
    def destruir(self):
        self._selected.destruir()
        self._texto.destruir()
        super(_HaplotypeActor, self).destruir()
    
    def set_selected(self, is_selected):
        self._selected = 0 if is_selected else 100
        
    def set_highlighted(self, is_highlighted):
        self.imagen = IMAGE_NODE_HIGLIGHTED if is_highlighted else IMAGE_NODE_NORMAL
    
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
        self._edges = set()

    def clear(self):
        self._edges.clear()
        self.limpiar()

    def del_edge(self, n0, n1):
        self._edges.remove((n0, n1))
        
    def del_edges_with_node(self, n):
        for haps in tuple(self._edges):
            if n in haps:
                self.del_edge(*haps)

    def add_edge(self, n0, n1):
        assert isinstance(n0, _HaplotypeActor) \
            and isinstance(n1, _HaplotypeActor)
        self._edges.add((n0, n1))

    def actualizar(self):
        self.limpiar()
        for act0, act1 in self._edges:
            x0, y0 = act0.x, act0.y
            x1, y1 = act1.x, act1.y
            self.linea(x0, y0, x1, y1, grosor=2)


#===============================================================================
# NETWORK WIDGET
#===============================================================================

class NetworkWidget(object):
    
    def __init__(self):
        self._nodes = {}
        self._edges = _EdgesDrawActor()

    def clear(self):
        self._nodes.clear()
        self._eges.clear()
    
    def select_node(self, hap):
        for h, n in self._nodes.items():
            n.set_selected(h == hap)

    def highlight_nodes(self, **haps):
        for h, n in self._nodes.items():
            n.set_highlighted(h in haps)
    
    def add_node(self, hap, x=0, y=0):
        node = _HaplotypeActor(hap, x=x, y=y)
        self._nodes[hap] = node
        
    def del_node(self, hap):
        node = self._nodes.pop(hap)
        self._edges.del_edges_with_node(node)
        node.destruir()
        
    def add_edge(self, hap0, hap1):
        self._edges.add_edge(self._nodes[hap0], self._nodes[hap1])
        
    def add_edges(self, *edges):
        for hap0, hap1 in edges:
            self.add_edge(hap0, hap1)
        
    def del_edge(self, hap0, hap1):
        self._edges.del_edge(self._nodes[hap0], self._nodes[hap1])
        
    def del_edges_with_node(self, hap):
        self._edges.del_edges_with_node(self._nodes[hap])
        
    def node_of(self, hap):
        return self._nodes[hap]


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    
    n = NetworkWidget()
    
    a0 = dom.Haplotype("hap0")
    a1 = dom.Haplotype("hap1")
    a2 = dom.Haplotype("hap2")
    a3 = dom.Haplotype("hap3")
    n.add_node(a0, 100, 200)
    n.add_node(a1, -100)
    n.add_node(a2, 200)
    n.add_node(a3, 0,-100)
    n.add_edge(a0, a1)
    n.add_edge(a1, a2)
    n.add_edge(a2, a3)
    
    
    
    pilas.ejecutar()
    
