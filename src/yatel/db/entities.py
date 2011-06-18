#!/usr/bin/env python
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
__license__ = "GPL3"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2011-06-11"


#===============================================================================
# IMPORTS
#===============================================================================

import inspect

import elixir


#===============================================================================
# FUNCTIONS
#===============================================================================

def create(session, metadata):

    #===========================================================================
    # ENTITIES
    #===========================================================================
    
    class Network(elixir.Entity):
        name = elixir.Field(elixir.UnicodeText)
        elixir.using_options(metadata=metadata,
                             session=session,
                             tablename="networks")


    class Haplotype(elixir.Entity):
        name = elixir.Field(elixir.UnicodeText)
        elixir.using_options(metadata=metadata,
                             session=session,
                             tablename="haplotypes")
    
    
    #===========================================================================
    # END ENTITIES
    #===========================================================================
    
    entities = {}
    for k, v in locals().items():
            if inspect.isclass(v) and issubclass(v, elixir.Entity):
                entities[k] = v
    return entities


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
