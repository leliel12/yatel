#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice 
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Implementation of a double slider.

"""


#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtCore

from yatel.gui import uis


#===============================================================================
# CLASS
#===============================================================================

class DoubleSlider(uis.UI("DoubleSlider.ui")):
    """DoubleSlider implementation as widget
    
    """
    
    #: Signal emited when the slider representing the lower limit is changed.
    endValueChanged = QtCore.pyqtSignal(int)
    
    #: Signal emited when the slider representing the upper limit is changed.
    startValueChanged = QtCore.pyqtSignal(int)
    
    def __init__(self, parent, text, min_value, max_value):
        """Create a new instance of ``DoubleSlider``
        
        **Params**
            :parent: A gui parent of this widget.
            :text: Text of label of the component
            :min_value: the minimum value of the slider.
            :max_value: the maximum value of the slider.
        
        """
        super(DoubleSlider, self).__init__(parent)
        if min_value > max_value:
            raise ValueError("min_value must be <= max_value")
        self.label.setText(text)
        self.minSlider.setMinimum(min_value)
        self.minSlider.setMaximum(max_value)
        self.minSlider.setSliderPosition(min_value)
        self.minValueLabel.setNum(min_value)
        self.maxSlider.setMinimum(min_value)
        self.maxSlider.setMaximum(max_value)
        self.maxSlider.setSliderPosition(max_value)
        self.maxValueLabel.setNum(max_value)
    
    def tops(self):
        """Return a tuple with minimun and maximum value of the slider.
        
        **Returns**
            A tuple ``(min_value, max_value)``.
        
        """
        return self.minSlider.minimum(), self.maxSlider.maximum()
    
    def setStart(self, start):
        """Set the position of the slider representing the lower limit.
        
        **Params**
            :start: ``int``.
            
        """
        self.minSlider.setSliderPosition(start)
        
    def setEnd(self, end):
        """Set the position of the slider representing the upper limit.
        
        **Params**
            :end: ``int``.
            
        """
        self.maxSlider.setSliderPosition(end)
    
    def on_minSlider_valueChanged(self, v):
        """Slot executed when slider representing the lower limit change.
        
        This method keeps ``minSlider <= maxSlider``.
        
        **Params**
            :v: New value of the slider as ``int``.
        
        """
        if v > self.maxSlider.value():
            self.maxSlider.setSliderPosition(v)
        self.startValueChanged.emit(v)
            
    def on_maxSlider_valueChanged(self, v):
        """Slot executed when slider representing the uper limit change
        
        This method keeps ``minSlider <= maxSlider``.
        
        **Params**
            :v: New value of the slider as ``int``.
        
        """
        if v < self.minSlider.value():
            self.minSlider.setSliderPosition(v)
        self.endValueChanged.emit(v)
        

#===============================================================================
# MAIN
#===============================================================================
        
if __name__ == "__main__":
    print(__doc__)
    
