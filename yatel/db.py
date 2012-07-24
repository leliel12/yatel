#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.


#===============================================================================
# CLASS
#===============================================================================


class YatelConnection(object):
    """Representa una coneccion a la base de datos"""
    
    
    def __init__(self, engine, name, 
                  host="localhost", port="", user="", password=""):
        """Este es el constructor de la clase recibe como parametros:
        
            engine: es el nombre del motor de la base de datos mysql, sqlite
                    postgre, oracle o lo que fuere (supongo que esos nombres
                    ya estan definidos en alchemy)
            name: es el nombre de la base de datos o el path al archivo en
                  el caso de sqlite
            host: el host donde corre el motor (no se usa en sqlite)
            port: el puerto donde se escucha el motor (no se usa en sqlite)
            user: el usuario para acceder a la base de datos (no se usa en sqlite)
            password: el password para acceder a la base de datos (no se usa en sqlite)
        """
        pass
        
    def close(self):
        """cierra la coneccion con la base de datos"""
        pass
        
    def commit(self):
        """comitea una transaccion"""
        pass
        
    def store(self, *yatelobjects):
        """Recibe una lista variable de objetos del dom de yatel (Haplotypes,
           Edges o Facts) y los almacena en la db (recordemos que los objetos
           ya vienen con el id ya insertado en el caso de los haplotypos)
           
           (el isinstance te va a ayudar a determinar cada uno de los elementos
           de la coleccion de que tipo son)
           
        """
        pass
        
    def get_haplotypes(self):
        """Retorna una tupla con todos los dom.Haplotype existentes en la db"""
        pass
        
    def get_edges(self):
        """Retorna una tupla con todos los dom.Edge existentes en la db"""
        pass
        
    def get_facts(self):
        """Retorna una tupla con todos los dom.Fact existentes en la db"""
        pass
    
    def filter(self, **ambient):
        """Recibe como parametro set de argumentos variables con el nombre
        de un attributo de un fact y el valor que se espera a buscar
        
        ambier={"att0": "value0".....}
        
        y retorna una tupla con todos los haplotypos que tienen esa condicion
        
        """
        pass
        
    def get_fact_attributes_names(self):
        """ devuelve una tupla con strings con todos los nombres de todos los
        atributos de todos los Fact
        
        """
        pass
        
    def get_fact_attribute_values(self, att_name):
        """ que me devuelve una tupla con strings con todos los valores posibles 
        de un atributo dad
        
        """
        pass
        
    def hap_sql(self, query, *args):
        """Ejecuta la sentencia sql del tipo 'select * from Table_Haplotypes where 
           zaraza = ?' y utiliza cmo argumento la tupla variable args
           
           y retorna los dom.Haplotype que corresponda Si la sentencia no
           empieza con "select * from Table_Haplotypes" el metodo falla con
           un ValueError
           
        """
        pass
        
    def raw_sql(self, query, *args):
        """Ejecuta la sentencia sql del tipo 'select * from Table where 
        zaraza = ?' y utiliza cmo argumento la tupla variable args
           
        retorna el result set standar de sqlalchemy
        """
        pass
    
    
            
        
    
