#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This module is used for construct yatel.dom object using yatel json format
files

"""

#===============================================================================
# IMPORTS
#===============================================================================

import json

from yatel import dom
from yatel.conv import coreconv


#===============================================================================
# IO FUNCTIONS
#===============================================================================

class JSONConverter(coreconv.BaseConverter):

    def dump(self, nw, stream=None, **kwargs):
        kwargs["indent"] = kwargs.get("indent", 2)
        kwargs["ensure_ascii"] = kwargs.get("ensure_ascii", True)
        data = super(JSONConversor, self).dump(nw)
        if stream:
            return json.dump(data, stream, **kwargs)
        return json.dumps(data, **kwargs)

    def load(self, nw, stream, **kwargs):
        loader = json.loads if isinstance(stream, basestring) else json.load
        data = loader(stream, **kwargs)
        return super(JSONConversor, self).load(nw, data)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

