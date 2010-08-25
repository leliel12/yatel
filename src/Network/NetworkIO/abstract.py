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

import abc

################################################################################
# CLASSES
################################################################################

class AbstractNetworkFileHandler(object):
    
    __metaclass__ = abc.ABCMeta

    def __init__(self, handle):
        self._file = handle

    @abc.abstractmethod
    def read(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def parse(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def write(self, sequences):
        raise NotImplementedError()
    
    @property
    def file(self):
        return self._file
    

################################################################################
# MAIN
################################################################################

if __name__ == "__main__":
    print __doc__

