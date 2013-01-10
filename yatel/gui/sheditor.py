#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.

# The original code:
#     Copyright (C) 2008 Christophe Kibleur <kib2@free.fr>
#     This file is part of WikiParser (http://thewikiblog.appspot.com/).


#===============================================================================
# DOCS
#===============================================================================

"""widgets an utilities for use syntax highlight"""


#===============================================================================
# IMPORTS
#===============================================================================

import time
import re

from PyQt4 import QtGui
from PyQt4 import QtCore

from pygments import highlight
from pygments.lexers import *
from pygments.formatter import Formatter

#===============================================================================
# FORMATER
#===============================================================================

class QFormatter(Formatter):

    def __init__(self):

        def hex2QColor(c):
            r=int(c[0:2],16)
            g=int(c[2:4],16)
            b=int(c[4:6],16)
            return QtGui.QColor(r,g,b)

        super(QFormatter, self).__init__()
        self.data=[]

        # Create a dictionary of text styles, indexed
        # by pygments token names, containing QTextCharFormat
        # instances according to pygments' description
        # of each style

        self.styles={}
        for token, style in self.style:
            qtf=QtGui.QTextCharFormat()

            if style['color']:
                qtf.setForeground(hex2QColor(style['color']))
            if style['bgcolor']:
                qtf.setBackground(hex2QColor(style['bgcolor']))
            if style['bold']:
                qtf.setFontWeight(QtGui.QFont.Bold)
            if style['italic']:
                qtf.setFontItalic(True)
            if style['underline']:
                qtf.setFontUnderline(True)
            self.styles[str(token)]=qtf

    def format(self, tokensource, outfile):
        global styles
        # We ignore outfile, keep output in a buffer
        self.data=[]

        # Just store a list of styles, one for each character
        # in the input. Obviously a smarter thing with
        # offsets and lengths is a good idea!

        for ttype, value in tokensource:
            l=len(value)
            t=str(ttype)
            self.data.extend([self.styles[t],]*l)


#===============================================================================
# HIGHLIGHTER
#===============================================================================

class Highlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, parent, mode):
        super(Highlighter, self).__init__(parent)
        self.tstamp=time.time()

        # Keep the formatter and lexer, initializing them
        # may be costly.
        self.formatter=QFormatter()
        self.lexer=get_lexer_by_name(mode)

    def highlightBlock(self, text):
        """Takes a block, applies format to the document.
        according to what's in it.
        """

        # I need to know where in the document we are,
        # because our formatting info is global to
        # the document
        cb = self.currentBlock()
        p = cb.position()

        # The \n is not really needed, but sometimes
        # you are in an empty last block, so your position is
        # **after** the end of the document.
        text=unicode(self.document().toPlainText())+'\n'

        # Yes, re-highlight the whole document.
        # There **must** be some optimizacion possibilities
        # but it seems fast enough.
        highlight(text,self.lexer,self.formatter)

        # Just apply the formatting to this block.
        # For titles, it may be necessary to backtrack
        # and format a couple of blocks **earlier**.
        for i in range(len(unicode(text))):
            try:
                self.setFormat(i,1,self.formatter.data[p+i])
            except IndexError:
                pass

        # I may need to do something about this being called
        # too quickly.
        self.tstamp=time.time()


#===============================================================================
# EDITOR
#===============================================================================

class HiglightedEditor(QtGui.QPlainTextEdit):
    """Editor with syntax highligt"""

    def __init__(self, syntax, parent=None):
        """Creates a new instance of ``HiglightedEditor``.

        **Params**
            :syntax: A name of existing lexer.
            :parent: The parent widget.

        """
        super(HiglightedEditor, self).__init__(parent)
        self.highlighter = Highlighter(self.document(),syntax)

    def text(self):
        return self.toPlainText()

    def setText(self, text):
        return self.setPlainText(text)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
    import sys
    app = QtGui.QApplication(sys.argv)
    rst = QtGui.QPlainTextEdit()
    rst.setWindowTitle('SQL')
    hl=Highlighter(rst.document(),"sql")
    rst.show()
    sys.exit(app.exec_())

