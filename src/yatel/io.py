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

import json

from yatel import haps, distances, network, facts


#===============================================================================
# PARSERS REGISTER
#===============================================================================

_parsers = {}

def register(parsername, cls=None):

    def iregister(cls):
        assert issubclass(cls, AbstractParser)
        _parsers[parsername] = cls
        return cls

    return iregister(cls) if cls else iregister


def unregister(parsername):
    _parsers.pop(parsername)


def list_parsers():
    return _parsers.keys()


def loads(parsername, src, **kwargs):
    return _parsers[parsername]().loads(src, **kwargs)


def dumps(parsername, nw, facts, **kwargs):
    return _parsers[parsername]().dumps(nw, facts, **kwargs)


def load(parsername, stream, **kwargs):
    return _parsers[parsername]().load(stream, **kwargs)


def dump(parsername, nw, facts, stream, **kwargs):
    return _parsers[parsername]().dump(nw, facts, stream, **kwargs)


#===============================================================================
# ABSTRACT
#===============================================================================

class AbstractParser(object):
    
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def  loads(self, src, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def dumps(self, nw, facts, **kwargs):
        raise NotImplementedError()

    def load(self, stream, **kwargs):
        return self.loads(stream.read(), **kwargs)

    def dump(self, nw, facts, stream, **kwargs):
        stream.write(self.dumps(nw, facts, **kwargs))


#===============================================================================
# NJD PARSER
#===============================================================================

@register("njd")
class NJDParser(AbstractParser):

    def loads(self, src, **kwargs):
        nw_as_dict = json.loads(src, **kwargs)
        
        nwid = nw_as_dict["id"]
        nwname = nw_as_dict["name"]
        annotations = nw_as_dict["annotations"]
        
        haplotypes = {}
        for name, atts in nw_as_dict["haplotypes"].items():
            haplotypes[name] = haps.Haplotype(name, **atts)
            
        distance_calculator = distances.ExpertDistance()
        for name0, hap0_distances in nw_as_dict["distances"].items():
            hap0 = haplotypes[name0]
            for name1, distance in hap0_distances.items():
                hap1 = haplotypes[name1]
                distance = float(distance)
                distance_calculator.add_distance(hap0, hap1, distance)

        nw = network.Network(id=nwid, name=nwname,
                             haplotypes=haplotypes.values(),
                             distance_calculator=distance_calculator,
                             annotations=annotations)
        nwfacts = []
        for id, fd in nw_as_dict["facts"].items():
            fact_haps = [haplotypes[hname] for hname in fd["haplotypes"]]
            fact_atts = fd["attributes"]
            nwfacts.append(facts.Fact(id, fact_haps, **fact_atts))
        return nw, tuple(nwfacts)
    
    def dumps(self, nw, facts, **kwargs):
        if "indent" not in kwargs:
            kwargs["indent"] = 4
        nw_as_dict = {}
        nw_as_dict["id"] = nw.id
        nw_as_dict["name"] = nw.name
        nw_as_dict["annotations"] = dict([(unicode(k), unicode(v))
                                           for k, v in nw.annotations.items()])
        haps_as_dict = {}
        distances_as_dict = {}
        for hap0 in nw.haplotypes:
            
            # parse attributes
            haps_as_dict[hap0.name] = dict([(k, v)
                                            for k, v in hap0.attributes.items()])
            # parse distances
            distances = {}
            for hap1 in nw.haplotypes:
                distance = nw.distance(hap0, hap1)
                if distance != None:
                    distances[hap1.name] = distance
            distances_as_dict[hap0.name] = distances
        
        nw_as_dict["haplotypes"] = haps_as_dict
        nw_as_dict["distances"] = distances_as_dict

        # parse facts0
        facts_as_dicts = {}
        for f in facts:
            facts_as_dicts[f.id] = {}
            facts_as_dicts[f.id]["attributes"] = dict([(k, v)
                                                       for k, v in f.attributes.items()])
            facts_as_dicts[f.id]["haplotypes"] = [h.name 
                                                    for h in f.haplotypes
                                                    if h.name in haps_as_dict]
        nw_as_dict["facts"] = facts_as_dicts

        return json.dumps(nw_as_dict, **kwargs)
        

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

