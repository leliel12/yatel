#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This module is used for construct yatel.dom object using yatel yaml format
files

"""

#===============================================================================
# IMPORTS
#===============================================================================

import yaml

from yatel import dom
from yatel.conv import coreconv


#===============================================================================
# IO FUNCTIONS
#===============================================================================

class YAMLConverter(coreconv.BaseConverter):

    def dump(self, nw, stream=None, **kwargs):
        data = super(JSONConversor, self).dump(nw)
        return yaml.safe_dump(data, stream=stream, **kwargs)

    def load(self, nw, stream):
        data = yaml.load(stream, **kwargs)
        return super(JSONConversor, self).load(nw, data)



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

