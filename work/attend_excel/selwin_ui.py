# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selwin.ui'
#
# Created: Fri Nov 20 09:04:42 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1160, 763)
        self.gridLayout_3 = QtGui.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.text_src = QtGui.QLineEdit(self.groupBox)
        self.text_src.setObjectName("text_src")
        self.gridLayout.addWidget(self.text_src, 0, 1, 1, 1)
        self.btn_src = QtGui.QPushButton(self.groupBox)
        self.btn_src.setObjectName("btn_src")
        self.gridLayout.addWidget(self.btn_src, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.text_dst = QtGui.QLineEdit(self.groupBox)
        self.text_dst.setObjectName("text_dst")
        self.gridLayout.addWidget(self.text_dst, 1, 1, 1, 1)
        self.btn_dst = QtGui.QPushButton(self.groupBox)
        self.btn_dst.setObjectName("btn_dst")
        self.gridLayout.addWidget(self.btn_dst, 1, 2, 1, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtGui.QSpacerItem(588, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btn_preprocess = QtGui.QPushButton(self.groupBox)
        self.btn_preprocess.setObjectName("btn_preprocess")
        self.horizontalLayout_3.addWidget(self.btn_preprocess)
        self.horizontalLayout_3.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem1 = QtGui.QSpacerItem(88, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.setStretch(0, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter = QtGui.QSplitter(self.groupBox_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.text_manul = QtGui.QPlainTextEdit(self.splitter)
        self.text_manul.setObjectName("text_manul")
        self.text_explain = QtGui.QTextBrowser(self.splitter)
        self.text_explain.setObjectName("text_explain")
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtGui.QSpacerItem(568, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btn_process = QtGui.QPushButton(Form)
        self.btn_process.setObjectName("btn_process")
        self.horizontalLayout.addWidget(self.btn_process)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.horizontalLayout.setStretch(0, 1)
        self.gridLayout_3.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.gridLayout_3.setRowStretch(1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "文件", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "源Excel", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_src.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "目标Excel", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_dst.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_preprocess.setText(QtGui.QApplication.translate("Form", "预处理", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Form", "手工处理", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_process.setText(QtGui.QApplication.translate("Form", "处理", None, QtGui.QApplication.UnicodeUTF8))
