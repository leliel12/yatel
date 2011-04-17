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
import csv

import yaml
from lxml import etree, builder


from yatel import haps, distances, network


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


def msg_on_load(parsername):
    return _parsers[parsername]().msg_on_load()


def msg_on_dump(parsername):
    return _parsers[parsername]().msg_on_dump()


def loads(parsername, src, **kwargs):
    return _parsers[parsername]().loads(src, **kwargs)


def dumps(parsername, nw, **kwargs):
    return _parsers[parsername]().dumps(nw, **kwargs)


def load(parsername, stream, **kwargs):
    return _parsers[parsername]().load(stream, **kwargs)


def dump(parsername, nw, stream, **kwargs):
    return _parsers[parsername]().dump(nw, stream, **kwargs)


#===============================================================================
# ABSTRACT
#===============================================================================

class AbstractParser(object):
    
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def  loads(self, src, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def dumps(self, nw, **kwargs):
        raise NotImplementedError()
    
    def msg_on_load(self):
        return ()
    
    def msg_on_dump(self):
        return ()

    def load(self, stream, **kwargs):
        return self.loads(stream.read(), **kwargs)

    def dump(self, nw, stream, **kwargs):
        stream.write(self.dumps(nw, **kwargs))


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
        return nw
    
    def dumps(self, nw, **kwargs):
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
            haps_as_dict[hap0.name] = dict([(k, v) for k, v in hap0.items()])
            
            # parse distances
            distances = {}
            for hap1 in nw.haplotypes:
                distance = nw.distance(hap0, hap1)
                if distance != None:
                    distances[hap1.name] = distance
            distances_as_dict[hap0.name] = distances
        
        nw_as_dict["haplotypes"] = haps_as_dict
        nw_as_dict["distances"] = distances_as_dict

        return json.dumps(nw_as_dict, **kwargs)
        
        
#===============================================================================
# CSV PARSER
#===============================================================================

@register("csv")
class CSVParser(AbstractParser):
    
    def loads(self, src, **kwargs):
        if "dialect" not in kwargs:
            kwargs["dialect"] = csv.Sniffer().sniff(src) \
                                or csv.get_dialect("excel")
        haplotypes = {}
        distance_calculator = distances.ExpertDistance()
        for h0n, h1n, d in csv.reader(src.splitlines(), **kwargs):
            if h0n not in haplotypes:
                haplotypes[h0n] = haps.Haplotype(h0n)
            if h1n not in haplotypes:
                haplotypes[h1n] = haps.Haplotype(h1n)
            distance_calculator.add_distance(haplotypes[h0n],
                                             haplotypes[h1n], float(d))
        nw = network.Network(id="", name="",
                             haplotypes=haplotypes.values(),
                             distance_calculator=distance_calculator)
        return nw
    
    def msg_on_dump(self):
        return ("CSVParser can't handle metadata of Network or Haplotypes",)
    
    def dumps(self, nw, **kwargs):
        
        stream = cStringIO.StringIO()
        csv_writer = csv.writer(stream, **kwargs)

        for hap0 in nw.haplotypes:
            n0 = hap0.name
            for hap1 in nw.haplotypes:
                n1 = hap1.name
                distance = nw.distance(hap0, hap1)
                if distance != None:
                    csv_writer.writerow([n0, n1, distance])
        return stream.getvalue()


#===============================================================================
# NYD
#===============================================================================

@register("nyd")
class NYDParser(AbstractParser):

    def loads(self, src, **kwargs):
        if not isinstance(src, basestring):
            raise TypeError("'src' must be basestring instance")
        nw_as_dict = yaml.load(src, **kwargs)
        
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
        return nw
    
    def dumps(self, nw, **kwargs):
        
        kwargs["stream"] = None
        if "indent" not in kwargs:
            kwargs["indent"] = True
        if "default_flow_style" not in kwargs:
            kwargs["default_flow_style"] = False
            
        nw_as_dict = {}
        nw_as_dict["id"] = nw.id
        nw_as_dict["name"] = nw.name
        nw_as_dict["annotations"] = dict([(str(k), str(v))
                                           for k, v in nw.annotations.items()])
        haps_as_dict = {}
        distances_as_dict = {}
        for hap0 in nw.haplotypes:
            # parse attributes
            haps_as_dict[hap0.name] = dict([(k, v) for k, v in hap0.items()])
            
            # parse distances
            distances = {}
            for hap1 in nw.haplotypes:
                distance = nw.distance(hap0, hap1)
                if distance != None:
                    distances[hap1.name] = distance
            distances_as_dict[hap0.name] = distances
        
        nw_as_dict["haplotypes"] = haps_as_dict
        nw_as_dict["distances"] = distances_as_dict

        return yaml.dump(nw_as_dict, **kwargs)

#===============================================================================
# NXD
#===============================================================================

@register("nxd")
class NXDParser(AbstractParser):
    
    def loads(self, src, **kwargs):
        nw = etree.XML(src, **kwargs)
        nwname = nw.attrib["name"]
        nwid = nw.attrib["id"]
        haplotypes = {}
        for hx in nw.iterfind("haplotypes/haplotype"):
            hname = hx.attrib["name"]
            hatts = {}
            for ax in hx.iterfind("attribute"):
                hatts[ax.attrib["name"]] = ax.text
            haplotypes[hname] = haps.Haplotype(hname, **hatts)
        distance_calculator = distances.ExpertDistance()
        for dx in nw.iterfind("distances/distance"):
            hap0 = haplotypes[dx.attrib["namefrom"]]
            hap1 = haplotypes[dx.attrib["nameto"]]
            distance = float(dx.text)
            distance_calculator.add_distance(hap0, hap1, distance)
        annotations = {}
        for ax in nw.iterfind("annotations/annotation"):
            annotations[ax.attrib["name"]] = ax.text
            
        nw = network.Network(id=nwid, name=nwname,
                             haplotypes=haplotypes.values(),
                             distance_calculator=distance_calculator,
                             annotations=annotations)
        return nw
    
    
    def dumps(self, nw, **kwargs):
        if "pretty_print" not in kwargs:
            kwargs["pretty_print"] = True
        
        e = builder.E
         
        def distances():
            distances = []
            for h0 in nw.haplotypes:
                for h1 in nw.haplotypes:
                    d = nw.distance(h0, h1)
                    if d != None:
                        distances.append(e.distance(str(d),
                                                    namefrom=h0.name,
                                                    nameto=h1.name))
            return distances
       
        haplotype = lambda h: e.haplotype(*[e.attribute(str(v), name=str(k))
                                              for k, v in h.items()], name=str(h.name))
        annotation = lambda k, v:e.annotation(str(v), name=str(k)) 
        nw_as_xml = e.network(
                              e.haplotypes(*[haplotype(h) for h in nw.haplotypes]),
                              e.distances(*distances()),
                              e.annotations(*[annotation(k, v) 
                                              for k, v in nw.annotations.items()]),
              name=nw.name,
              id=nw.id
        )
        
        return etree.tostring(nw_as_xml, **kwargs)
    

        
        
            
        



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

