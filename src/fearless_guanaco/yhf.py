#!/usr/bin/env python
# coding=utf-8

# "yhf.py" is part of "Fearless Guanaco"
#                                    (http://code.google.com/p/fearlessguanaco/)
# Copyright (C) 2010 UTN-KDD Group <UTN_KDD@googlegroups.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


################################################################################
# DOCS
################################################################################

"""Fearless Guanaco 'YHF' file parser"""

################################################################################
# META
################################################################################

__version__ = "0.1"
__license__ = "GPL3"
__author__ = "JBC"
__since__ = "0.1"
__date__ = "2010/04/19"


################################################################################
# IMPORTS
################################################################################

import yaml


################################################################################
# YHF ERROR CLASS
################################################################################

class YHFError(Exception):
    pass


################################################################################
# YHF ATT CLASS
################################################################################

class YHFAttribute(object):

    def __init__(self, name, desc, v_values):
        self.name = name
        self.description = desc
        self.valid_values = v_values
    
    def __eq__(self, obj):
        if isinstance(obj, YHFAttribute):
            return self.name == obj.name
    
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)
    
    def to_dict(self):
        return {self.name: {"description": self.description,
                            "valid_values": self.valid_values}}


################################################################################
# YHF HAPLOTYPE CLASS
################################################################################

class YHFHaplotype(object):

    def __init__(self, name, desc, value):
        self.name = name
        self.description = desc
        self._value = value
    
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)
        
    def to_dict(self):
        return {self.name: {"description": self.description,
                            "value": self._value}}
    
    @property
    def value(self):
        return self._value


################################################################################
# YHF SPECIE CLASS
################################################################################

class YHFSpecie(object):

    def __init__(self, name, desc, atts):
        self.name = name
        self.description = desc
        self._haps = []
        self._atts = []
        for i, a in enumerate(atts):
            if not isinstance(a, YHFAttribute):
                msg = "atts[%i] is not a YHFAttribute instance" % i
                raise YHFError(msg)
            if a in self._atts:
                msg = "Attribute with name '%s' already exist" % a.name
                raise YHFError(msg)
            self._atts.append(a)
    
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)
    
    def to_dict(self):
        return {self.name:{"description": self.description,
                           "attributes": [a.to_dict() for a in self._atts],
                           "haplotypes": [h.to_dict() for h in self._haps]}}
    
    def add_haplotype(self, hap):
        if not isinstance(hap, YHFHaplotype):
            msg = "hap is not a YHFHaplotype instance"
            raise YHFError(msg)
        if len(hap.value) != len(self._atts):
            msg = "Haplotype '%s' has diferent number of" \
                  "attributes (%i) of this specie (%i)" % (hap.name,
                                                           len(hap.value),
                                                           len(self._atts))
            raise YHFError(msg)
        if hap in self._haps:
            msg = "Haplotype with name '%s' already exist" % name
            raise YHFError(msg)
        for value_part, att in zip(hap.value, self._atts):
            if att.valid_values and value_part not in att.valid_values:
                msg = "Value '%s' in haplotype '%s' not match with any of '%s'" \
                      % (value_part, hap.name, str(list(att.valid_values)))
                raise YHFError(msg)
        self._haps.append(hap)
        
    @property
    def haplotypes(self):
        return tuple(self._haps)
    
    @property
    def attributes(self):
        return tuple(self._atts)


################################################################################
# FUNCTIONS
################################################################################

def load(yhf_file):
    """Parse a yhf file into YHFSpecie object"""
    yhf_src = yhf_file.read()
    return loads(yhf_src)


def loads(yhf_src):
    """Parse a yhf source code into YHFSpecie object"""
    data = yaml.load(yhf_src)
    name, specie_data = data.items()[0]
    name = str(name)
    description = str(specie_data["description"])
    atts = []
    for att in specie_data["attributes"]:
        if len(att) > 1:
            msg = "To many values in '%s'" % str(att)
            raise YHFError(msg)
        a_name = str(att.keys()[0])
        a_desc = str(att.values()[0]["description"])
        a_v_values = str(att.values()[0]["valid_values"] or "")
        atts.append(YHFAttribute(a_name, a_desc, a_v_values))
    specie = YHFSpecie(name, description, atts)
    for hap in specie_data["haplotypes"]:
        if len(hap) > 1:
            msg = "To many values in '%s'" % str(hap)
            raise YHFError(msg)
        h_name = str(hap.keys()[0])
        h_desc = str(hap.values()[0]["description"])
        h_value = str(hap.values()[0]["value"])
        specie.add_haplotype(YHFHaplotype(h_name, h_desc, h_value))
    return specie


def dumps(specie):
    """Convert an YHFSpecie object into yhf file code"""
    if not isinstance(specie, YHFSpecie):
        msg = "'specie' must be a YHFSpecie instance"
        raise YHFError(msg)
    return yaml.dump(specie.to_dict())


def dump(specie, yhf_file):
    """Dumps an YHFSpecie object as yhf file code into a given file"""
    yhf_src = dumps(specie)
    yhf_file.write(yhf_src)


################################################################################
# MAIN
################################################################################

if __name__ == "__main__":
    print __doc__



