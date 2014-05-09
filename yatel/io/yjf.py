#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


# =============================================================================
# DOC
# =============================================================================

"""Persist yatel db in json format"""


# =============================================================================
# IMPORTS
# =============================================================================

import json

from yatel import typeconv
from yatel.io import core


# =============================================================================
# CLASS
# =============================================================================

class JSONParser(core.BaseParser):
    """A json parser to serialize from a yatel networks to a json formatted 
    file or string, and deserialize to a yatel network from a json formatted 
    file or string.
    
    """
    
    @classmethod
    def file_exts(cls):
        return ("yjf", "json")

    def dump(self, nw, fp, *args, **kwargs):
        """Serialize a yatel db in json format.
        
        Parameters
        ----------
        nw : yatel.db.YatelNetwork
            network source of data
        fp: file like object
            Destination file
        kwargs: keywords arguments for json module
        
        """
        kwargs["ensure_ascii"] = kwargs.get("ensure_ascii", True)
        data = {
            "haplotypes":  map(typeconv.simplifier, nw.haplotypes()),
            "facts": map(typeconv.simplifier, nw.facts()),
            "edges": map(typeconv.simplifier, nw.edges()),
            "version": self.version(),
        }
        json.dump(data, fp, *args, **kwargs)

    def load(self, nw, fp, *args, **kwargs):
        """Deserializes data from a json file and adds it to the yatel network
        
        Parameters
        ----------
        nw : yatel.db.YatelNetwork
            destination network for data
        fp: file like object
            source file
            
        """
        data = json.load(fp, *args, **kwargs)
        nw.add_elements(map(typeconv.parse, data["haplotypes"]))
        nw.add_elements(map(typeconv.parse, data["facts"]))
        nw.add_elements(map(typeconv.parse, data["edges"]))

    
# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(__doc__)
