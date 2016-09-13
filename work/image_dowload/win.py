# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'win.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(768, 642)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.text_srce = QtGui.QLineEdit(self.groupBox)
        self.text_srce.setObjectName(_fromUtf8("text_srce"))
        self.gridLayout.addWidget(self.text_srce, 0, 1, 1, 1)
        self.brow_src = QtGui.QPushButton(self.groupBox)
        self.brow_src.setObjectName(_fromUtf8("brow_src"))
        self.gridLayout.addWidget(self.brow_src, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.dir_dst = QtGui.QLineEdit(self.groupBox)
        self.dir_dst.setObjectName(_fromUtf8("dir_dst"))
        self.gridLayout.addWidget(self.dir_dst, 1, 1, 1, 1)
        self.brow_dst = QtGui.QPushButton(self.groupBox)
        self.brow_dst.setObjectName(_fromUtf8("brow_dst"))
        self.gridLayout.addWidget(self.brow_dst, 1, 2, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout_2.addWidget(self.pushButton_3, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 100, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 1, 1, 1, 1)
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 2, 0, 1, 4)
        spacerItem2 = QtGui.QSpacerItem(20, 396, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 3, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "here", None))
        self.label.setText(_translate("Form", "source", None))
        self.brow_src.setText(_translate("Form", "browse", None))
        self.label_2.setText(_translate("Form", "destination", None))
        self.brow_dst.setText(_translate("Form", "browse", None))
        self.pushButton_3.setText(_translate("Form", "start", None))

