#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dom.py
     
# Copyright 2011 Juan BC <jbc dot develop at gmail dot com>

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
# DOCS
#===============================================================================

"""This module is used for calculate weights of edgest in yatel

"""


#===============================================================================
# ERROR
#===============================================================================

class AbstractWeight(object):
    """"""
    
    def weight(self, hap0, hap1):
        """"""
        raise NotImplementedError()
        

#===============================================================================
# FACT
#===============================================================================


class Hamming(AbstractWeight):
    
    def weight(self, hap0, hap1):
        w = 0
        for name in set(hap0.names_attrs() + hap1.names_attrs()):
            if name not in h0.names_attrs() \
               or name not in h1.names_attrs() \
               or h0.get_attr(name) != h1.get_attr(name):
                w += 1
        return w
        
            




#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    import dom

    h0 = dom.Haplotype("h0", a0="0", a1="1")
    h1 = dom.Haplotype("h1", a0="1", a1="1")

    hamming = Hamming()

    print __doc__




