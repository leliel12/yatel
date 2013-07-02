#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOC
#===============================================================================

"""Wrapper for use jqplot inside qtapp

"""

if __name__ == "__main__":
    import sys, os
    sys.path.insert(1, os.path.join("..", ".."))
    import yatel.gui


#===============================================================================
# IMPORTS
#===============================================================================

import random
import json

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtWebKit

from yatel import dom

from yatel.gui import html


#===============================================================================
# NETWORK WIDGET
#===============================================================================

class Plot(QtWebKit.QWebView):
    """Singleton instance for use Pilas widget as QtWidget ofr draw networks

    """

    def __init__(self, parent=None):
        """Init the instance of ``NetworkProxy`` singleton."""
        super(Plot, self).__init__(parent=parent)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.loop = QtCore.QEventLoop()
        self.page().mainFrame().addToJavaScriptWindowObject("python", self)

        self._frame = self.page().currentFrame()

        self.loadFinished.connect(self.on_ready)

        self.load(QtCore.QUrl.fromLocalFile(html.get("plot.html")))
        self.loop.exec_()

    def doCapture(self, filename):
        """Save the view of the network as image

        Based on: https://github.com/ralsina/nikola/blob/master/scripts/capty

        """
        wb = self.page()
        wb.setViewportSize(wb.mainFrame().contentsSize())
        img = QtGui.QImage(wb.viewportSize(), QtGui.QImage.Format_ARGB32)
        painter = QtGui.QPainter(img)
        wb.mainFrame().render(painter)
        painter.end()
        img.save(filename)



    @QtCore.pyqtSlot()
    def on_ready(self):
        """Called when the html is ready"""
        self.loop.exit()
        self.loadFinished.disconnect(self.on_ready)

    def py2js(self, obj):
        """Convert the python object to javascript object"""
        if isinstance(obj, (list, tuple, dict)):
            if isinstance(obj, tuple):
                obj = list(obj)
            return json.dumps(obj)
        elif isinstance(obj, bool):
            return unicode(obj).lower()
        elif obj is None:
            return u"null"
        elif not isinstance(obj, (int, float)):
            return u"'{}'".format(obj)
        return unicode(obj)

    def js_function(self, func, *args):
        """This method call the subjacent javascript widget.

        Example:

        .. code-block:: python

            n = Network()
            n.js_function("add_node", 1, 2, 3, 4)

        is equivalent in javascript to

        .. code-block:: javascript

            add_node(1, 2, 3, 4);

        """
        prepared_args = map(self.py2js, args)
        jsfunc = "{}({})".format(func, ", ".join(prepared_args))
        return self._frame.evaluateJavaScript(jsfunc)

    def clear(self):
        """Remove all nodes and edges of the graph"""
        self.js_function("clear")

    def draw_serie(self, serie):
        self.js_function("drawSerie", serie)



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

    import sys, os
    sys.path.insert(1, os.path.join("..", ".."))

    settings = QtWebKit.QWebSettings.globalSettings()
    settings.setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)

    n = Plot()
    n.draw_serie([1,2,3])
    n.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
    win = QtGui.QMainWindow()
    win.setCentralWidget(n)
    win.show()
    n.draw_serie([1,2,3,4])

    sys.exit(yatel.gui.APP.exec_())
# ~
