# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.


#===============================================================================
# FUTURE
#===============================================================================

from __future__ import absolute_import


#===============================================================================
# DOCS
#===============================================================================

"""


"""


#===============================================================================
# META
#===============================================================================

__version__ = "0.1"
__license__ = "gpl3"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2010-08-04"

#===============================================================================
# IMPORT
#===============================================================================

import abc
import cStringIO

import json

from yatel import haps, distances

#===============================================================================
# PARSERS REGISTER
#===============================================================================

_parsers = {}

def register(name, cls=None):

    def iregister(cls):
        assert issubclass(cls, AbstractParser)
        _parsers[name] = cls
        return cls

    return iregister(cls) if cls else iregister


def parsers():
    return _parsers.keys()


def loads(parsername, src):
    return _parsers[parsername]().loads(src)


def dumps(parsername, nw):
    return _parsers[parsername]().dumps(nw)


def load(parsername, stream):
    return _parsers[parsername]().load(stream)


def dump(parsername, nw, stream):
    return _parsers[parsername]().dumps(nw, stream)


#===============================================================================
# ABSTRACT
#===============================================================================

class AbstractParser(abc.ABCMeta):

    @abc.abstractmethod
    def  loads(self, src):
        raise NotImplementedError()

    @abc.abstractmethod
    def dumps(self, nw):
        raise NotImplementedError()

    def load(self, stream):
        return self.loads(stream.read())

    def dump(self, nw, stream):
        stream.write(self.dumps(nw))


#===============================================================================
# NJD PARSER
#===============================================================================

@register("njd")
class NJDParser(AbstractParser):

    def loads(self, src):
        nw_as_dict = json.loads(src)
        
        id = nw_as_dict["id"]
        name = nw_as_dict["name"]
        annotations = nw_as_dict["annotations"]
        
        haplotypes  = {}
        for name, atts in nw_as_dict["haplotypes"].items():
            haplotypes[name] = haps.haplotype(name, **atts)
            
        distance_calculator = distances.ExpertDistance()
        for haps, distance in nw_as_dict["distances"].items()
            hap0, hap1 = haplotypes[haps[0]], haplotypes[haps[1]]
            distance = float(distance)
            distance_calculator.add_distance(hap0, hap1, distance)

        nw = network.Network(id=id, name=name,
                             haplotypes=haplotypes,
                             distance_calculator=distance, 
                             annotations=annotations)
        return nw
    
    def dumps(self, nw):
        nw_as_dict = {}
        nw_as_dict["id"] = nw.id
        nw_as_dict["name"] = nw.name
        nw_as_dict["annotations"] = dict([(unicode(k), unicode(v))
                                           for k, v in nw.annotations.items()])
        haps_as_dict = {}
        distances_as_dict = {}
        for hap0 in nw.happlotypes():
            haps_as_dict[hap0.name] = dict([(k, v) for k, v in hap0.items()])
            for hap1 in nw.happlotypes():
                distance = nw.distance(hap0, hap1)
                if distance != None:
                    distances_as_dict[(hap0.name, hap1.name)] = None
        
        nw_as_dict["haplotypes"] = haps_as_dict
        nw_as_dict["distances"] = distances_as_dict

        return json.dumps(nw_as_dict, indent=4)
        

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

