#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOC
#===============================================================================

"""Wrapper for use actors and pilas widget inside a qt app as a interactive
network.

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

from yatel.gui import resources


#===============================================================================
# NETWORK WIDGET
#===============================================================================

class Network(QtWebKit.QWebView):
    """Singleton instance for use Pilas widget as QtWidget ofr draw networks

    """
    node_clicked = QtCore.pyqtSignal(dom.Haplotype)

    def __init__(self, parent=None):
        """Init the instance of ``NetworkProxy`` singleton."""
        super(Network, self).__init__(parent=parent)
        self.loop = QtCore.QEventLoop()
        self.page().mainFrame().addToJavaScriptWindowObject("python", self)

        self._haps = {}
        self._highlighted = ()
        self._selected = None
        self._haps_names_showed = True
        self._weights_showed = True
        self._frame = self.page().currentFrame()

        self.loadFinished.connect(self.on_ready)

        self.load(QtCore.QUrl.fromLocalFile(resources.get("network.html")))
        self.loop.exec_()

    @QtCore.pyqtSlot(str)
    def on_nodeclicked(self, hap_id):
        hap = self._haps[hap_id]
        self.node_clicked.emit(hap)

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
        self._haps = {}
        self._highlighted = ()
        self._selected = None
        self._haps_names_showed = True
        self.js_function("clear")

    def get_unused_coord(self, max_iteration=100):
        """Return a probably *free of node* coordinate"""

        xy = self.js_function("getUnusedCoord",
                              self.height(), self.width(), max_iteration)
        return map(int, xy)

    def select_node(self, hap):
        """Select a node asociated to the given ``yatel.dom.Haplotype``"""
        self._selected = hap
        self.js_function("selectNode", hap.hap_id)

    def show_haps_names(self, show):
        """Show the name of the haplotype over all the nodes.

        **Params**
            :show: ``bool`` flag to show or hide the haplotype name

        """
        self.js_function("showHapsNames", show)
        self._haps_names_showed = show

    def show_weights(self, show):
        """Show the weights over all the edges.

        **Params**
            :show: ``bool`` flag to show or hide the edge's weight.

        """
        self.js_function("showWeights", show)
        self._weights_showed = show

    def highlight_nodes(self, *haps):
        """Highlight all the nodes given in a tuple ``*haps``."""
        ids = [hap.hap_id for hap in haps]
        self.js_function("highlightNodes", ids)
        self._highlighted = haps

    def unhighlightall(self):
        """Unhighlight all the nodes."""
        self.js_function("unhighlightall")
        self._highlighted = ()

    def add_node(self, hap, x=0, y=0):
        """Add a new node.

        **Params**
            :hap: The ``dom.Haplotype`` instance for extract data to
                  create the node.
            :x: ``int`` of the relative position from center of the widget where
                the node will be drawed.
            :y: ``int`` of the relative position from center of the widget where
                the node will be drawed.

        """
        if hap.hap_id not in self._haps:
            self._haps[hap.hap_id] = hap
            self.js_function("addNode", hap.hap_id, hap.hap_id, x, y)

    def del_node(self, hap):
        """Delete the node asociated to the given ``yatel.dom.Haplotype`` *hap*.

        """
        self._haps.pop(hap.hap_id)
        self.js_function("delNode", hap.hap_id)

    def add_edge(self, edge):
        """Add a new edge between the nodes asociated to the *haplotypes* of
        the ``yatel.dom.Edge`` instance.

        """
        self.js_function("addEdge", edge.weight, *edge.haps_id)

    def add_edges(self, *edges):
        """Add a multiple new edge between the nodes asociated to the
        *haplotypes* of the tuple ``yatel.dom.Edge`` instances.

        """
        map(self.add_edge, edges)

    def filter_edges(self, *edges):
        """Show only the listed ``*edges``"""
        eids = []
        for e in edges:
            eids.append("_".join(e.haps_id))
        self.js_function("filterEdges", eids)

    def del_edge(self, edge):
        """Delete the given edge"""
        self.js_function("delEdge", *edge.haps_id)

    def del_edges_with_node(self, hap):
        """Deletes all edges containing the node asociated with haplotype
        ``hap``.

        """
        self.js_function("delEdgesWithNode", hap.hap_id)

    def topology(self):
        """Gets a ``dict`` qith keys as ``yatel.dom.Haplotype`` and value a
        ``tuple`` with the position of the asociated node.

        """
        top = {}
        for k, v in self.js_function("topology").items():
            top[self._haps[k]] = tuple(v)
        return top

    def move_node(self, hap, x, y):
        """Move node asociated to the given *haplotype* to ``x, y``"""
        self.js_function("moveNode", hap.hap_id, x, y)

    def center(self):
        self.js_function("center")

    @property
    def haps_names_showed(self):
        """Return if the haplotypes names are actually showed."""
        return self._haps_names_showed;

    @property
    def weights_showed(self):
        """Return if the weight edges are actually showed."""
        pass

    @property
    def bounds(self):
        """The size os the drawable area."""
        return self.width(), self.height()

    @property
    def selected_node(self):
        """The selected node."""
        return self._selected

    @property
    def highlighted_nodes(self):
        """The list of higlighted nodes."""
        return self._highlighted


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

    import sys, os
    sys.path.insert(1, os.path.join("..", ".."))

    settings = QtWebKit.QWebSettings.globalSettings()
    settings.setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)

    n = Network()

    a0 = dom.Haplotype("hap0")
    a1 = dom.Haplotype("hap1")
    a2 = dom.Haplotype("hap2")
    a3 = dom.Haplotype("hap3")
    n.add_node(a0, 0, 0)
    n.add_node(a1, -100, 100)
    n.add_node(a2, 200, 200)
    n.add_node(a3, 0, -100)

    n.select_node(a3)
    n.show()

    edges = [dom.Edge(555, a0.hap_id, a1.hap_id),
             dom.Edge(777, a3.hap_id, a2.hap_id),
             dom.Edge(666, a2.hap_id, a0.hap_id)]
    n.add_edges(*edges)
    n.haps_names_showed
    n.move_node(a3, 0, 50)
    n.get_unused_coord()

    n.highlight_nodes(a2, a3)

    # n.unhighlightall()

    n.topology()
    n.center()

    # n.del_edges_with_node(a2)
    # ~ n.filter_edges(edges[0], edges[1])
    # ~ n.del_node(a0)
    # ~ n.del_edge(edges[1])
# ~
    # ~ f = dom.Fact(a1.hap_id, a=1)
    # ~ n.highlight_nodes(a1, a2)
    # ~ n.node_clicked.conectar(printer)
    # ~ n.node_clicked.conectar(selector)
# ~
    sys.exit(yatel.gui.APP.exec_())
    # ~ pilas.ejecutar()
# ~
