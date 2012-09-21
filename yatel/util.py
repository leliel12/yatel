#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# DOCS
#===============================================================================

"""This module several usefull functions used in yatel

"""


#===============================================================================
# IMPORTS
#===============================================================================

import re
import collections
from unicodedata import normalize


#===============================================================================
# CONSTANTS
#===============================================================================

_RX_A = re.compile(u"á|à|ä|â", re.UNICODE)
_RX_I = re.compile(u"í|ì|ï|î", re.UNICODE)
_RX_U = re.compile(u"ú|ù|ü|û", re.UNICODE)
_RX_E = re.compile(u"é|è|ë|ê", re.UNICODE)
_RX_O = re.compile(u"ó|ò|ô|ö", re.UNICODE)
_RX_N = re.compile(u"ñ", re.UNICODE)
_RX_START_END_WORD = re.compile("^\W+|\W+$", re.UNICODE)
_RX_SPLITTER = re.compile("[^a-zA-Z0-9-_]*", re.UNICODE)


#===============================================================================
# CLASSES
#===============================================================================

class UniqueNonUnicodeKey(collections.MutableMapping):
    
    def __init__(self, d=None, **kwargs):
        self._d = {}
        if isinstance(d, dict):
            for k in d:
                self[k] = d[k]
        for k in kwargs:
            self[k] = kwargs[k]

    def __repr__(self):
        return "<{} {} at {}>".format(self.__class__.__name__,
                                       str(self._d),
                                       hex(id(self)))

    def __iter__(self):
        return iter(self._d)
        
    def __len__(self):
        return len(self._d)

    def __getitem__(self, k):
        return self._d[k]

    def __setitem__(self, k, v):
        if not isinstance(k, basestring):
            msg = "Key must be a instance of 'str' or 'unicode', found {}"
            raise TypeError(msg.format(type(k)))
        norm = norm_text(k)
        if norm in self._d:
            norm += "_"
            idx = 1
            while (norm + str(idx)) in self._d:
                idx += 1
            norm += str(idx)
        self._d[norm] = v
        
    def __delitem__(self, k):
        self._d.__delitem__(k)
    

#===============================================================================
# FUNCTIONS
#===============================================================================

def norm_text(text):
    """Convert a unicode or string in cleaned version of it, replacing all
    non alpha character for equivalent version or "_"
    
    """
    
    if isinstance(text, str):
        text = unicode(text)
    text = text.lower()
    text = text.strip()
    text = _RX_A.sub(u"a", text)
    text = _RX_I.sub(u"i", text)
    text = _RX_U.sub(u"u", text)
    text = _RX_E.sub(u"e", text)
    text = _RX_O.sub(u"o", text)
    text = _RX_N.sub(u"n", text)
    text = u"_".join(_RX_SPLITTER.split(text))
    text = _RX_START_END_WORD.sub(u"", text)
    while text.endswith("_"):
        text = text[:-1]
    while text.startswith("_"):
        text = text[1:]
    return str(normalize('NFKD', text).encode('ASCII', 'ignore').lower())

