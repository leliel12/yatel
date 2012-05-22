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
# ACTOR NODO
#===============================================================================

class HaplotypeActor(actores.Texto):
    
    def __init__(self, hap, x=0, y=0):
        assert isinstance(hap, dom.Haplotype)
        super(HaplotypeActor, self).__init__()
        self.haplotype = hap
        
        # conf
        self.x, self.y = x, y
        self.aprender(habilidades.Arrastrable)
        
    @property
    def haplotype(self):
        return self._hap
        
    @haplotype.setter
    def haplotype(self, hap):
        self._hap = hap
        self.texto = unicode(hap.hap_id)
        self.imagen = imagenes.cargar_grilla(resources.get("node.svg"), 2)
        

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    motor = pilas._crear_motor("qt")
    pilas.mundo = pilas.Mundo(motor, ancho=800, alto=600, titulo="Yatel")
    a0=HaplotypeActor(dom.Haplotype("jjj"), x=10)
    a1=HaplotypeActor(dom.Haplotype("kkk"))
    
    pilas.ejecutar()
    
    
    print a0, a1
    
