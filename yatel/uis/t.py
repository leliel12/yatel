# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'charge_frame.ui'
#
# Created: Tue Sep 13 19:01:47 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.resize(716, 499)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Frame.sizePolicy().hasHeightForWidth())
        Frame.setSizePolicy(sizePolicy)
        Frame.setFrameShape(QtGui.QFrame.NoFrame)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout = QtGui.QVBoxLayout(Frame)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tableCool = QtGui.QTableWidget(Frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableCool.sizePolicy().hasHeightForWidth())
        self.tableCool.setSizePolicy(sizePolicy)
        self.tableCool.setObjectName(_fromUtf8("tableCool"))
        self.tableCool.setColumnCount(0)
        self.tableCool.setRowCount(0)
        self.tableCool.horizontalHeader().setVisible(True)
        self.tableCool.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.tableCool)
        self.tableTypes = QtGui.QTableWidget(Frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableTypes.sizePolicy().hasHeightForWidth())
        self.tableTypes.setSizePolicy(sizePolicy)
        self.tableTypes.setMaximumSize(QtCore.QSize(250, 16777215))
        self.tableTypes.setGridStyle(QtCore.Qt.NoPen)
        self.tableTypes.setObjectName(_fromUtf8("tableTypes"))
        self.tableTypes.setColumnCount(2)
        self.tableTypes.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableTypes.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableTypes.setHorizontalHeaderItem(1, item)
        self.tableTypes.horizontalHeader().setStretchLastSection(True)
        self.tableTypes.verticalHeader().setVisible(True)
        self.tableTypes.verticalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.tableTypes)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.selectHapIdLabel = QtGui.QLabel(Frame)
        self.selectHapIdLabel.setEnabled(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 131, 131))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.selectHapIdLabel.setPalette(palette)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.selectHapIdLabel.setFont(font)
        self.selectHapIdLabel.setToolTip(_fromUtf8(""))
        self.selectHapIdLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.selectHapIdLabel.setObjectName(_fromUtf8("selectHapIdLabel"))
        self.verticalLayout.addWidget(self.selectHapIdLabel)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.tableTypes.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Frame", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.tableTypes.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Frame", "<ID OF WHAT>", None, QtGui.QApplication.UnicodeUTF8))
        self.selectHapIdLabel.setText(QtGui.QApplication.translate("Frame", "<PLEASE SELECT>", None, QtGui.QApplication.UnicodeUTF8))

