#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# TEST PROPUSES PATCH
#===============================================================================

if __name__ == "__main__":
    import sys, os
    path = os.path.abspath(os.path.dirname(__file__))
    rel = os.path.join(path, "..", "..")
    print rel
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

IMAGE_NODE_NORMAL = pilas.imagenes.cargar(resources.get("node_normal.svg"))
IMAGE_NODE_FACT = pilas.imagenes.cargar(resources.get("node_fact.svg"))
IMAGE_NODE_SELECTED = pilas.imagenes.cargar(resources.get("node_selected.svg"))


#===============================================================================
# ACTOR NODO
#===============================================================================

class _HaplotypeActor(actores.Actor):
    
    def __init__(self, hap, x=0, y=0):
        super(_HaplotypeActor, self).__init__()
        
        # internal data
        self._texto = actores.Texto()
        
        # conf
        self.haplotype = hap
        self.x, self.y = x, y
        self.aprender(habilidades.Arrastrable)
        self._texto.aprender(habilidades.Imitar, self)
    
    def destruir(self):
        self._texto.destruir()
        super(_HaplotypeActor, self).destruir()
    
    @property
    def haplotype(self):
        return self._hap
        
    @haplotype.setter
    def haplotype(self, hap):
        assert isinstance(hap, dom.Haplotype)
        self._hap = hap
        self._texto.texto = unicode(self._hap.hap_id)
        self.imagen = IMAGE_NODE_NORMAL
        

#===============================================================================
# EDGE ACTOR
#===============================================================================

class _EdgesDrawActor(actores.Pizarra):

    def __init__(self):
        pilas.actores.Pizarra.__init__(self)
        self._edges = set()

    def del_edge(self, n0, n1):
        self._edges.remove(n0, n1)

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
# MAIN
#===============================================================================

if __name__ == "__main__":
    
    edges = _EdgesDrawActor()
    a0=_HaplotypeActor(dom.Haplotype("jjj"), x=100)
    a1=_HaplotypeActor(dom.Haplotype("kkk"))
    
    edges.add_edge(a0, a1)
    
    pilas.ejecutar()
    
    
    print a0, a1
    
