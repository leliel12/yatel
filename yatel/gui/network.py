#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

ANCHO = 600

ALTO = 300

pilas.iniciar(ANCHO, ALTO,
              usar_motor="qt" if __name__ == "__main__" else "qtsugar")


#===============================================================================
# CONSTANTS
#===============================================================================

IMAGE_NODE_NORMAL = imagenes.cargar(
    resources.get("node_normal.png")
)

IMAGE_NODE_HIGLIGHTED = imagenes.cargar(
    resources.get("node_highlighted.png")
)

IMAGE_NODE_SELECTED = imagenes.cargar(
    resources.get("node_selected.png")
)

IMAGE_NODE_UNSELECTED = imagenes.cargar(
    resources.get("node_unselected.png")
)

MAX_X = ANCHO / 2.0

MAX_Y = ALTO / 2.0


#===============================================================================
# HABILIDADES
#===============================================================================

class NoSaleDeEcena(habilidades.Habilidad):
    
    def actualizar(self):
        if self.receptor.derecha > MAX_X:
            self.receptor.derecha = MAX_X
        elif self.receptor.izquierda < -MAX_X:
            self.receptor.izquierda = -MAX_X
        if self.receptor.arriba > MAX_Y:
            self.receptor.arriba = MAX_Y
        elif self.receptor.abajo < -MAX_Y:
            self.receptor.abajo = -MAX_Y
        

#===============================================================================
# ACTOR NODO
#===============================================================================

class _HaplotypeActor(actores.Actor):
    
    def __init__(self, hap, x=0, y=0):
        super(_HaplotypeActor, self).__init__(imagen=IMAGE_NODE_NORMAL, 
                                              x=x, y=y)
        
        # internal data
        self._selected = actores.Actor(imagen=IMAGE_NODE_UNSELECTED)
        self._texto = actores.Texto(magnitud=12)
        self._show_text= True
        self.clicked = eventos.Evento("clicked")
        
        # conf
        self.haplotype = hap
        self.x, self.y = x, y
        self.aprender(habilidades.Arrastrable)
        self.aprender(NoSaleDeEcena)
        self._texto.aprender(habilidades.Imitar, self)
        self._selected.aprender(habilidades.Imitar, self)
        
        # connect events
        eventos.click_de_mouse.conectar(
            self._on_mouse_clicked,
            id=hex(id(self))
        )
    
    def show_text(self, show):
        self._show_text = show
        if show:
            self._texto.texto = unicode(self._hap.hap_id)
        else:
            self._texto.texto = u""
    
    def collide(self, x, y):
        return self.colisiona_con_un_punto(x, y) \
            or self._texto.colisiona_con_un_punto(x, y) \
            or self._selected.colisiona_con_un_punto(x, y)
    
    def _on_mouse_clicked(self, evt):
        x, y = evt["x"], evt["y"]
        if self.collide(x, y):
                self.clicked.emitir(sender=self)
        
    def destruir(self):
        self._selected.destruir()
        self._texto.destruir()
        self.clicked.respuestas.clear()
        eventos.click_de_mouse.desconectar_por_id(hex(id(self)))
        super(_HaplotypeActor, self).destruir()
    
    def set_selected(self, is_selected):
        if is_selected:
            self._selected.imagen = IMAGE_NODE_SELECTED
        else:
            self._selected.imagen = IMAGE_NODE_UNSELECTED
        
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
        self.show_text(self._show_text)
        
        

#===============================================================================
# EDGE ACTOR
#===============================================================================

class _EdgesDrawActor(actores.Pizarra):

    def __init__(self):
        pilas.actores.Pizarra.__init__(self)
        self._edges = {}
        self._show_weights = True

    def clear(self):
        self._edges.clear()
        self.limpiar()
        self._show_weights = True

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

    def show_weights(self, show):
        self._show_weights = show

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
                self.linea(x0, y0, x1, y1, grosor=2, color=colores.negro)
            elif len(nodes) > 2:
                xp = sum([act.x for act in nodes]) / len(nodes)
                yp = sum([act.y for act in nodes]) / len(nodes)
                text_x, text_y = xp + 10, yp + 10
                for act in nodes:
                    self.linea(xp, yp, act.x, act.y, 
                               grosor=2, color=colores.rojo)
            if self._show_weights:
                self.texto(unicode(weight), text_x, text_y, 
                           color=colores.blanco)
        
    @property
    def weights_showed(self):
        return self._show_weights


#===============================================================================
# NETWORK WIDGET
#===============================================================================

class NetworkProxy(object):
    
    _instance = None
    
    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not NetworkProxy._instance:
            instance = super(NetworkProxy, cls).__new__(cls, *args, **kwargs)
            NetworkProxy._instance = instance
        return NetworkProxy._instance
            
    def __init__(self):
        self._nodes = {}
        self._edges = _EdgesDrawActor()
        self._bounds = None
        self._selected = None
        self._highlighted = ()
        self._haps_names_showed = True
        self.node_clicked = eventos.Evento("node_clicked")
        fondos.Color(colores.grisoscuro)
        
    def __getattr__(self, att_name):
        return getattr(self.widget, att_name)
        
    def _on_node_clicked(self, evt):
        sender = evt["sender"]
        self.node_clicked.emitir(node=sender.haplotype)
    
    def get_unussed_coord(self):
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
        for n in self._nodes.values():
            n.destruir()
        self._nodes.clear()
        self._edges.clear()
        self._selected = None
        self._highlighted = ()
    
    def select_node(self, hap):
        for hid, n in self._nodes.items():
            if hid == hap.hap_id:
                n.set_selected(True)
                self._selected = n.haplotype
            else:
                n.set_selected(False)
    
    def show_haps_names(self, show):
        self._haps_names_showed = show
        for n in self._nodes.values():
            n.show_text(show)
            
    def show_weights(self, show):
        self._edges.show_weights(show)
        
    def highlight_nodes(self, *haps):
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
        for n in self._nodes.values():
            n.set_highlighted(False)
        self._highlighted = ()
                
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
            
    def filter_edges(self, *edges):
        self._edges.clear()
        for edge in edges:
            self.add_edge(edge)
        
    def del_edge(self, edge):
        assert isinstance(edge, dom.Edge)
        nodes = []
        for hap_id in edge.haps_id:
            self._nodes.append(hap_id)
        self._edges.del_edge(*nodes)
        
    def del_edges_with_node(self, hap):
        self._edges.del_edges_with_node(self._nodes[hap.hap_id])
        
    def actor_of(self, hap):
        return self._nodes[hap.hap_id]
    
    def topology(self):
        top = {}
        for actor in self._nodes.values():
            top[actor.haplotype] = (actor.x, actor.y)
        return top
        
    def move_node(self, hap, x, y):
        actor = self.actor_of(hap)
        actor.x = x
        actor.y = y
    
    @property
    def haps_names_showed(self):
        return self._haps_names_showed
        
    @property
    def weights_showed(self):
        return self._edges.weights_showed
    
    @property
    def bounds(self):
        if self._bounds is None:
            width = self.widget.size().width() / 2 #xs
            height = self.widget.size().height() / 2 #ys
            self._bounds = (-width, height, width, -height)
        return self._bounds
    
    @property
    def widget(self):
        return pilas.mundo.motor.widget
    
    @property
    def selected_node(self):
        return self._selected
        
    @property
    def highlighted_nodes(self):
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
    
    
    print n.bounds
    print n.get_unussed_coord()
    print n.size()
    pilas.ejecutar()
    
