#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# DOCS
#===============================================================================

"""http server for queriying using qbj or yql

"""

#===============================================================================
# IMPORTS
#===============================================================================

import flask

from yatel import db, qbj


#===============================================================================
# BASE CLASS
#===============================================================================

class YatelHTTPServer(flask.Flask):

    def __init__(self, **config):
        super(YatelHTTPServer, self).__init__()
        self.config.from_object(config)

        self._nws = {}

        self.route("/")(self._its_works)
        self.route("/qbj/<nw>")(self._qbj)

    def add_nw(self, nwname, nw, qbj):
        if not isinstance(nw, db.YatelNetwork):
            raise TypeError("nw must be db.YatelNetwork subclass")
        self._nws[nwname] = {"nwname": nwname, "nw": nw}
        if qbj:
            self._nws[nwname]["qbj"] = qbj.QBJEngine(nw)

    def _its_works(self):
        return "{} works!".format(type(self).__name__)

    def _qbj(self, nw):
        pass



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




