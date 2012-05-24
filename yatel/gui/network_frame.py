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
# CONSTANTS
#===============================================================================

IMAGE_NODE_NORMAL = resources.get("node_normal.svg")
"""IMAGE_NODE_FACT = pilas.imagenes.cargar(resources.get("node_fact.svg"))
IMAGE_NODE_SELECTED = pilas.imagenes.cargar(resources.get("node_select.svg"))
"""
#===============================================================================
# ACTOR NODO
#===============================================================================

class HaplotypeActor(actores.Texto):
    
    def __init__(self, hap, x=0, y=0, z=0):
        assert isinstance(hap, dom.Haplotype)
        super(HaplotypeActor, self).__init__()
        self.haplotype = hap
        
        # conf
        self.x, self.y, self.z = x, y, z
        self.aprender(habilidades.Arrastrable)
        
    @property
    def haplotype(self):
        return self._hap
        
    @haplotype.setter
    def haplotype(self, hap):
        self._hap = hap
        self.texto = unicode(hap.hap_id)
        self.imagen = IMAGE_NODE_NORMAL
        

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    motor = pilas._crear_motor("qt")
    pilas.mundo = pilas.Mundo(motor, ancho=800, alto=600, titulo="Yatel")
    a0=HaplotypeActor(dom.Haplotype("jjj"), x=10)
    a1=HaplotypeActor(dom.Haplotype("kkk"), z=5)
    
    pilas.ejecutar()
    
    
    print a0, a1
    
