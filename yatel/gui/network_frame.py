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
from pilas import habilidades

from yatel import dom

#===============================================================================
# ACTOR NODO
#===============================================================================

class HaplotypeActor(actores.Actor, actores.Texto):
    
    def __init__(self, hap, x, y):
        self._hap = hap
        
        self.texto
        self.aprender(habilidades.Arrastrable)
        
        


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    motor = pilas._crear_motor("qt")
    pilas.mundo = pilas.Mundo(motor, ancho=800, alto=600, titulo="Yatel")
    pilas.ejecutar()
