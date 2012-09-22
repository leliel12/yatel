#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtCore

from yatel.gui import uis


#===============================================================================
# CLASS
#===============================================================================

class DoubleSlider(uis.UI("DoubleSlider.ui")):

    endValueChanged = QtCore.pyqtSignal(int)
    startValueChanged = QtCore.pyqtSignal(int)
    
    def __init__(self, parent, text, min_value, max_value):
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
        return self.minSlider.minimum(), self.maxSlider.maximum()
    
    def setStart(self, start):
        self.minSlider.setSliderPosition(start)
        
    def setEnd(self, end):
        self.maxSlider.setSliderPosition(end)
    
    def on_minSlider_valueChanged(self, v):
        if v > self.maxSlider.value():
            self.maxSlider.setSliderPosition(v)
        self.startValueChanged.emit(v)
            
    def on_maxSlider_valueChanged(self, v):
        if v < self.minSlider.value():
            self.minSlider.setSliderPosition(v)
        self.endValueChanged.emit(v)
        

#===============================================================================
# MAIN
#===============================================================================
        
if __name__ == "__main__":
    print(__doc__)
    
