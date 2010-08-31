#!/usr/bin/env python
#-*-coding:utf-8-*-

# Copyright (C) 2010 Juan BC <jbc dot develop at gmail dot com>

# Biopython License Agreement

# Permission to use, copy, modify, and distribute this software and its
# documentation with or without modifications and for any purpose and
# without fee is hereby granted, provided that any copyright notices
# appear in all copies and that both those copyright notices and this
# permission notice appear in supporting documentation, and that the
# names of the contributors or copyright holders not be used in
# advertising or publicity pertaining to distribution of the software
# without specific prior permission.

# THE CONTRIBUTORS AND COPYRIGHT HOLDERS OF THIS SOFTWARE DISCLAIM ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL THE
# CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY SPECIAL, INDIRECT
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
# OR PERFORMANCE OF THIS SOFTWARE.


################################################################################
# DOCS
################################################################################

"""
    
    
"""


################################################################################
# META
################################################################################

__version__ = "0.1"
__license__ = "Biopython License"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2010-08-04"


################################################################################
# IMPORTS
################################################################################

import json

import base


################################################################################
# CLASSES
################################################################################

src = {
    
    "sequences":
        {
            "1":
                {"seq": "00001", "description": "lalalal"},
            "2":
                {"seq": "11110", "description": "lololol"}
        },
        
    "networks":
        [
            [(1, 2, 3), (2, 1, 2)],
            [(1, 2, 3), (2, 1, 2)]
        ]
}
import StringIO

src = StringIO.StringIO(json.dumps(src))

class NJDFileHandler(base.AbstractNetworkFileHandler):
    
    def read(self, handle):
        pass
    
    def parse(self, handle):
        data = json.load(handle)
        sequences = []
        if "sequences" in data:
            print data["sequences"]
    
    def write(self, sequences, handle):
        pass

NJDFileHandler().parse(src)

################################################################################
# MAIN
################################################################################

if __name__ == "__main__":
    print __doc__

