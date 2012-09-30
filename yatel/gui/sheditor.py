#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice 
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""widgets an utilities for use syntax highligt of QScintilla

"""


#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qsci


#===============================================================================
# EDITOR
#===============================================================================

class HiglightedEditor(Qsci.QsciScintilla):
    """Editor with syntax highligt"""
    
    def __init__(self, syntax, parent=None):
        """Creates a new instance of ``HiglightedEditor``.
        
        **Params**
            :syntax: A name of existing lexer.
            :parent: The parent widget.
            
        """
        super(HiglightedEditor, self).__init__(parent)
        self.setLexer(lexer(syntax)())
        self.setAutoIndent(True)
        self.setIndentationWidth(4)
        self.setIndentationGuides(1)
        self.setIndentationsUseTabs(0)
        self.setAutoCompletionThreshold(2)


#===============================================================================
# FUNCTIONS
#===============================================================================

def lexer(syntax):
    """Return the lexer for the given language
    
    **Params**
        :syntax: A name of existing lexer.
    
    """
    if syntax == "java":
        return Qsci.QsciLexerJava
    if syntax == "pascal":
        return Qsci.QsciLexerPascal
    if syntax == "spice":
        return Qsci.QsciLexerSpice
    if syntax == "bash":
        return Qsci.QsciLexerBash
    if syntax == "d":
        return Qsci.QsciLexerD
    if syntax == "javascript":
        return Qsci.QsciLexerJavaScript
    if syntax == "perl":
        return Qsci.QsciLexerPerl
    if syntax == "tcl":
        return Qsci.QsciLexerTCL
    if syntax == "batch":
        return Qsci.QsciLexerBatch
    if syntax == "diff":
        return Qsci.QsciLexerDiff
    if syntax == "lua":
        return Qsci.QsciLexerLua
    if syntax == "postscript":
        return Qsci.QsciLexerPostScript
    if syntax == "tex":
        return Qsci.QsciLexerTeX
    if syntax == "cmake":
        return Qsci.QsciLexerCMake
    if syntax == "fortran":
        return Qsci.QsciLexerFortran
    if syntax == "makefile":
        return Qsci.QsciLexerMakefile
    if syntax == "properties":
        return Qsci.QsciLexerProperties
    if syntax == "vhdl":
        return Qsci.QsciLexerVHDL
    if syntax == "cpp":
        return Qsci.QsciLexerCPP
    if syntax == "fortran77":
        return Qsci.QsciLexerFortran77
    if syntax == "matlab":
        return Qsci.QsciLexerMatlab
    if syntax == "python":
        return Qsci.QsciLexerPython
    if syntax == "verilog":
        return Qsci.QsciLexerVerilog
    if syntax == "css":
        return Qsci.QsciLexerCSS
    if syntax == "html":
        return Qsci.QsciLexerHTML
    if syntax == "octave":
        return Qsci.QsciLexerOctave
    if syntax == "ruby":
        return Qsci.QsciLexerRuby
    if syntax == "xml":
        return Qsci.QsciLexerXML
    if syntax == "csharp":
        return Qsci.QsciLexerCSharp
    if syntax == "idl":
        return Qsci.QsciLexerIDL
    if syntax == "pov":
        return Qsci.QsciLexerPOV
    if syntax == "sql":
        return Qsci.QsciLexerSQL
    if syntax == "yaml":
        return Qsci.QsciLexerYAML
    raise ValueError("Invalid syntax: " + syntax)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

