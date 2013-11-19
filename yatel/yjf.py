#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# DOC
#===============================================================================

"""Persist yatel db in json format"""


#===============================================================================
# IMPORTS
#===============================================================================

import json

try:
    import cStringIO as StringIO
except:
    import StringIO

from yatel import typeconv

#===============================================================================
# CONSTANTS
#===============================================================================

YJF_VERSION = (0, 5)
YJF_STR_VERSION = ".".join(YJF_VERSION)


#===============================================================================
# CLASS
#===============================================================================

class JSONParser(object):

    def dump(self, nw, fp, *args, **kwargs):
        kwargs["ensure_ascii"] = kwargs.get("ensure_ascii", True)
        kwargs["indent"] = 2
        data = {
            "haplotypes":  map(typeconv.simplifier, nw.haplotypes()),
            "facts": map(typeconv.simplifier, nw.facts()),
            "edges": map(typeconv.simplifier, nw.edges()),
            "version": YJF_STR_VERSION,
        }
        json.dump(data, fp, *args, **kwargs)

    def load(self, nw, fp, *args, **kwargs):
        data = json.load(fp, *args, **kwargs)
        nw.add_elements(map(typeconv.parse, data["haplotypes"]))
        nw.add_elements(map(typeconv.parse, data["facts"]))
        nw.add_elements(map(typeconv.parse, data["edges"]))

    def dumps(self, nw, *args, **kwargs):
        fp = StringIO.StringIO()
        self.dump(nw, fp, *args, **kwargs)
        return fp.getvalue()

    def loads(self, nw, string, *args, **kwargs):
        fp = StringIO.StringIO(string)
        self.loads(nw, fp, *args, **kwargs)


#===============================================================================
# FUNCTIONS
#===============================================================================

def load(nw, stream, *args, **kwargs):
    parser = JSONParser()
    if isinstance(stream, basestring):
        return parser.loads(nw, stream, *args, **kwargs)
    return parser.load(nw, stream, *args, **kwargs)

def dump(nw, stream=None, *args, **kwargs):
    parser = JSONParser()
    if stream is None:
        return parser.dumps(nw, *args, **kwargs)
    return parser.dump(nw, stream, *args, **kwargs)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
