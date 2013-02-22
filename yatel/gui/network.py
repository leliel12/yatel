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

#===============================================================================
# IMPORTS
#===============================================================================

import random

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
    node_clicked = "signal"

    def __init__(self):
        """Init the instance of ``NetworkProxy`` singleton."""
        super(Network, self).__init__()
        self.load(QtCore.QUrl.fromLocalFile(resources.get("network.html")))

    def _mro_(self, *v):
        """``None``"""
        if v:
            v = v[0]
            self._dabc = (v.strip().encode("base64") == __key__)

    def get_unused_coord(self):
        """Return a probably *free of node* coordinate"""
        pass

    def clear(self):
        """Clear all widget from *nodes* and *edges*."""
        pass

    def select_node(self, hap):
        """Select a node asociated to the given ``yatel.dom.Haplotype``"""
        pass

    def show_haps_names(self, show):
        """Show the name of the haplotype over all the nodes.

        **Params**
            :show: ``bool`` flag to show or hide the haplotype name

        """
        pass

    def show_weights(self, show):
        """Show the weights over all the edges.

        **Params**
            :show: ``bool`` flag to show or hide the edge's weight.

        """
        pass

    def highlight_nodes(self, *haps):
        """Highlight all the nodes given in a tuple ``*haps``."""
        pass

    def unhighlightall(self):
        """Unhighlight all the nodes."""
        pass

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
        pass

    def del_node(self, hap):
        """Delete the node asociated to the given ``yatel.dom.Haplotype`` *hap*.

        """
        pass

    def add_edge(self, edge):
        """Add a new edge between the nodes asociated to the *haplotypes* of
        the ``yatel.dom.Edge`` instance.

        """
        pass

    def add_edges(self, *edges):
        """Add a multiple new edge between the nodes asociated to the
        *haplotypes* of the tuple ``yatel.dom.Edge`` instances.

        """
        pass

    def filter_edges(self, *edges):
        """Show only the listed ``*edges``"""
        pass

    def del_edge(self, edge):
        """Delete the given edge"""
        pass

    def del_edges_with_node(self, hap):
        """Deletes all edges containing the node asociated with haplotype
        ``hap``.

        """
        pass

    def topology(self):
        """Gets a ``dict`` qith keys as ``yatel.dom.Haplotype`` and value a
        ``tuple`` with the position of the asociated node.

        """
        return {}

    def move_node(self, hap, x, y):
        """Move node asociated to the given *haplotype* to ``x, y``"""
        pass

    @property
    def haps_names_showed(self):
        """Return if the haplotypes names are actually showed."""
        pass

    @property
    def weights_showed(self):
        """Return if the weight edges are actually showed."""
        pass

    @property
    def bounds(self):
        """The size os the drawable area."""
        pass

    @property
    def selected_node(self):
        """The selected node."""
        pass

    @property
    def highlighted_nodes(self):
        """The list of higlighted nodes."""
        pass


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

#~
    #~ def printer(evt):
        #~ n.show_haps_names(not n.haps_names_showed)
        #~ n.show_weights(not n.weights_showed)
        #~ pilas.avisar(str(evt))
#~
    #~ def selector(evt):
        #~ n.select_node(evt["node"])
#~
    #~ a0 = dom.Haplotype("hap0")
    #~ a1 = dom.Haplotype("hap1")
    #~ a2 = dom.Haplotype("hap2")
    #~ a3 = dom.Haplotype("hap3")
    #~ n.add_node(a0, 100, 200)
    #~ n.add_node(a1, -100)
    #~ n.add_node(a2, 200)
    #~ n.add_node(a3, 0, -100)
    #~ n.add_edge(dom.Edge(555, a0.hap_id, a1.hap_id))
    #~ n.add_edge(dom.Edge(666, a3.hap_id, a2.hap_id))
    #~ n.add_edge(dom.Edge(666, a2.hap_id, a0.hap_id))
#~
    #~ f = dom.Fact(a1.hap_id, a=1)
    #~ n.highlight_nodes(a1, a2)
    #~ n.node_clicked.conectar(printer)
    #~ n.node_clicked.conectar(selector)
#~
    #~ pilas.ejecutar()
#~
