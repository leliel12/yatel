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

from yatel import haps, distances, network


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

class AbstractParser(object):
    
    __metaclass__ = abc.ABCMeta
    
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
            haplotypes[name] = haps.Haplotype(name, **atts)
            
        distance_calculator = distances.ExpertDistance()
        for haps, distance in nw_as_dict["distances"].items():
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
# CSV PARSER
#===============================================================================

@register("csv")
class CSVParser(AbstractParser):
    
    def loads(self, src):
        dialect = csv.Sniffer().sniff(src) or csv.get_dialect("excel")
        haplotypes = {}
        distance_calculator = distances.ExpertDistance()
        for h0n, h1n, d in csv.reader(src.splitlines(), dialect=dialect):
            if h0n not in haplotypes:
                haplotypes[h0n] =  haps.Haplotype(h0n)
            if h1n not in haplotypes:
                haplotypes[h1n] =  haps.Haplotype(h1n)
            distance_calculator.add_distance(haplotypes[h0n], 
                                             haplotypes[h1n], float(d))
        nw = network.Network(id="", name="",
                             haplotypes=haplotypes.values(),
                             distance_calculator=distance_calculator)
        return nw
        
    def dumps(self, nw):
        pass


a='MTsxOzAKMTsyOzIKMTszOzMKMTs0OzIKMTs1OzIKMTs2OzEKMTs3OzQKMTs4OzQKMTs5OzMKMTsx\nMDszCjE7MTE7NAoxOzEyOzMKMTsxMzs1CjE7MTQ7NAoxOzE1OzMKMTsxNjsyCjE7MTc7MwoxOzE4\nOzQKMTsxOTszCjE7MjA7NAoxOzIxOzMKMjsxOzIKMjsyOzAKMjszOzIKMjs0OzEKMjs1OzIKMjs2\nOzMKMjs3OzIKMjs4OzIKMjs5OzEKMjsxMDszCjI7MTE7MwoyOzEyOzMKMjsxMzszCjI7MTQ7Mgoy\nOzE1OzMKMjsxNjsyCjI7MTc7MQoyOzE4OzQKMjsxOTszCjI7MjA7NAoyOzIxOzMKMzsxOzMKMzsy\nOzIKMzszOzAKMzs0OzEKMzs1OzIKMzs2OzMKMzs3OzMKMzs4OzMKMzs5OzIKMzsxMDsyCjM7MTE7\nMQozOzEyOzMKMzsxMzs0CjM7MTQ7MwozOzE1OzQKMzsxNjszCjM7MTc7MwozOzE4OzQKMzsxOTsy\nCjM7MjA7NAozOzIxOzQKNDsxOzIKNDsyOzEKNDszOzEKNDs0OzAKNDs1OzEKNDs2OzIKNDs3OzIK\nNDs4OzIKNDs5OzEKNDsxMDszCjQ7MTE7Mgo0OzEyOzIKNDsxMzszCjQ7MTQ7Mgo0OzE1OzMKNDsx\nNjsyCjQ7MTc7Mgo0OzE4OzMKNDsxOTszCjQ7MjA7Mwo0OzIxOzMKNTsxOzIKNTsyOzIKNTszOzIK\nNTs0OzEKNTs1OzAKNTs2OzEKNTs3OzIKNTs4OzIKNTs5OzEKNTsxMDszCjU7MTE7Mgo1OzEyOzEK\nNTsxMzszCjU7MTQ7Mgo1OzE1OzMKNTsxNjsyCjU7MTc7Mwo1OzE4OzIKNTsxOTszCjU7MjA7Mgo1\nOzIxOzMKNjsxOzEKNjsyOzMKNjszOzMKNjs0OzIKNjs1OzEKNjs2OzAKNjs3OzMKNjs4OzMKNjs5\nOzIKNjsxMDsyCjY7MTE7Mwo2OzEyOzIKNjsxMzs0CjY7MTQ7Mwo2OzE1OzIKNjsxNjsxCjY7MTc7\nNAo2OzE4OzMKNjsxOTs0CjY7MjA7Mwo2OzIxOzIKNzsxOzQKNzsyOzIKNzszOzMKNzs0OzIKNzs1\nOzIKNzs2OzMKNzs3OzAKNzs4OzEKNzs5OzEKNzsxMDszCjc7MTE7Mwo3OzEyOzMKNzsxMzsxCjc7\nMTQ7Mgo3OzE1OzIKNzsxNjsyCjc7MTc7Mwo3OzE4OzQKNzsxOTs1Cjc7MjA7Mgo3OzIxOzMKODsx\nOzQKODsyOzIKODszOzMKODs0OzIKODs1OzIKODs2OzMKODs3OzEKODs4OzAKODs5OzEKODsxMDsz\nCjg7MTE7Mwo4OzEyOzMKODsxMzsyCjg7MTQ7Mgo4OzE1OzIKODsxNjsyCjg7MTc7Mwo4OzE4OzQK\nODsxOTs1Cjg7MjA7Mwo4OzIxOzMKOTsxOzMKOTsyOzEKOTszOzIKOTs0OzEKOTs1OzEKOTs2OzIK\nOTs3OzEKOTs4OzEKOTs5OzAKOTsxMDsyCjk7MTE7Mgo5OzEyOzIKOTsxMzsyCjk7MTQ7MQo5OzE1\nOzIKOTsxNjsxCjk7MTc7Mgo5OzE4OzMKOTsxOTs0Cjk7MjA7Mwo5OzIxOzIKMTA7MTszCjEwOzI7\nMwoxMDszOzIKMTA7NDszCjEwOzU7MwoxMDs2OzIKMTA7NzszCjEwOzg7MwoxMDs5OzIKMTA7MTA7\nMAoxMDsxMTsyCjEwOzEyOzQKMTA7MTM7NAoxMDsxNDszCjEwOzE1OzIKMTA7MTY7MQoxMDsxNzs0\nCjEwOzE4OzUKMTA7MTk7NAoxMDsyMDs1CjEwOzIxOzIKMTE7MTs0CjExOzI7MwoxMTszOzEKMTE7\nNDsyCjExOzU7MgoxMTs2OzMKMTE7NzszCjExOzg7MwoxMTs5OzIKMTE7MTA7MgoxMTsxMTswCjEx\nOzEyOzMKMTE7MTM7NAoxMTsxNDszCjExOzE1OzQKMTE7MTY7MwoxMTsxNzs0CjExOzE4OzQKMTE7\nMTk7MwoxMTsyMDs0CjExOzIxOzQKMTI7MTszCjEyOzI7MwoxMjszOzMKMTI7NDsyCjEyOzU7MQox\nMjs2OzIKMTI7NzszCjEyOzg7MwoxMjs5OzIKMTI7MTA7NAoxMjsxMTszCjEyOzEyOzAKMTI7MTM7\nMgoxMjsxNDsxCjEyOzE1OzQKMTI7MTY7MwoxMjsxNzs0CjEyOzE4OzMKMTI7MTk7MgoxMjsyMDsx\nCjEyOzIxOzIKMTM7MTs1CjEzOzI7MwoxMzszOzQKMTM7NDszCjEzOzU7MwoxMzs2OzQKMTM7Nzsx\nCjEzOzg7MgoxMzs5OzIKMTM7MTA7NAoxMzsxMTs0CjEzOzEyOzIKMTM7MTM7MAoxMzsxNDsxCjEz\nOzE1OzMKMTM7MTY7MwoxMzsxNzs0CjEzOzE4OzUKMTM7MTk7NAoxMzsyMDsxCjEzOzIxOzIKMTQ7\nMTs0CjE0OzI7MgoxNDszOzMKMTQ7NDsyCjE0OzU7MgoxNDs2OzMKMTQ7NzsyCjE0Ozg7MgoxNDs5\nOzEKMTQ7MTA7MwoxNDsxMTszCjE0OzEyOzEKMTQ7MTM7MQoxNDsxNDswCjE0OzE1OzMKMTQ7MTY7\nMgoxNDsxNzszCjE0OzE4OzQKMTQ7MTk7MwoxNDsyMDsyCjE0OzIxOzEKMTU7MTszCjE1OzI7Mwox\nNTszOzQKMTU7NDszCjE1OzU7MwoxNTs2OzIKMTU7NzsyCjE1Ozg7MgoxNTs5OzIKMTU7MTA7Mgox\nNTsxMTs0CjE1OzEyOzQKMTU7MTM7MwoxNTsxNDszCjE1OzE1OzAKMTU7MTY7MQoxNTsxNzs0CjE1\nOzE4OzUKMTU7MTk7NgoxNTsyMDs0CjE1OzIxOzIKMTY7MTsyCjE2OzI7MgoxNjszOzMKMTY7NDsy\nCjE2OzU7MgoxNjs2OzEKMTY7NzsyCjE2Ozg7MgoxNjs5OzEKMTY7MTA7MQoxNjsxMTszCjE2OzEy\nOzMKMTY7MTM7MwoxNjsxNDsyCjE2OzE1OzEKMTY7MTY7MAoxNjsxNzszCjE2OzE4OzQKMTY7MTk7\nNQoxNjsyMDs0CjE2OzIxOzEKMTc7MTszCjE3OzI7MQoxNzszOzMKMTc7NDsyCjE3OzU7MwoxNzs2\nOzQKMTc7NzszCjE3Ozg7MwoxNzs5OzIKMTc7MTA7NAoxNzsxMTs0CjE3OzEyOzQKMTc7MTM7NAox\nNzsxNDszCjE3OzE1OzQKMTc7MTY7MwoxNzsxNzswCjE3OzE4OzMKMTc7MTk7NAoxNzsyMDs1CjE3\nOzIxOzQKMTg7MTs0CjE4OzI7NAoxODszOzQKMTg7NDszCjE4OzU7MgoxODs2OzMKMTg7Nzs0CjE4\nOzg7NAoxODs5OzMKMTg7MTA7NQoxODsxMTs0CjE4OzEyOzMKMTg7MTM7NQoxODsxNDs0CjE4OzE1\nOzUKMTg7MTY7NAoxODsxNzszCjE4OzE4OzAKMTg7MTk7NQoxODsyMDs0CjE4OzIxOzUKMTk7MTsz\nCjE5OzI7MwoxOTszOzIKMTk7NDszCjE5OzU7MwoxOTs2OzQKMTk7Nzs1CjE5Ozg7NQoxOTs5OzQK\nMTk7MTA7NAoxOTsxMTszCjE5OzEyOzIKMTk7MTM7NAoxOTsxNDszCjE5OzE1OzYKMTk7MTY7NQox\nOTsxNzs0CjE5OzE4OzUKMTk7MTk7MAoxOTsyMDszCjE5OzIxOzQKMjA7MTs0CjIwOzI7NAoyMDsz\nOzQKMjA7NDszCjIwOzU7MgoyMDs2OzMKMjA7NzsyCjIwOzg7MwoyMDs5OzMKMjA7MTA7NQoyMDsx\nMTs0CjIwOzEyOzEKMjA7MTM7MQoyMDsxNDsyCjIwOzE1OzQKMjA7MTY7NAoyMDsxNzs1CjIwOzE4\nOzQKMjA7MTk7MwoyMDsyMDswCjIwOzIxOzMKMjE7MTszCjIxOzI7MwoyMTszOzQKMjE7NDszCjIx\nOzU7MwoyMTs2OzIKMjE7NzszCjIxOzg7MwoyMTs5OzIKMjE7MTA7MgoyMTsxMTs0CjIxOzEyOzIK\nMjE7MTM7MgoyMTsxNDsxCjIxOzE1OzIKMjE7MTY7MQoyMTsxNzs0CjIxOzE4OzUKMjE7MTk7NAoy\nMTsyMDszCjIxOzIxOzA=\n'
a = a.decode("base64")
print CSVParser().loads(a)




#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

