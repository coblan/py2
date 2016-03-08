# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwin.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(932, 769)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 932, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.stat_bar = QtGui.QStatusBar(MainWindow)
        self.stat_bar.setObjectName(_fromUtf8("stat_bar"))
        MainWindow.setStatusBar(self.stat_bar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionTest = QtGui.QAction(MainWindow)
        self.actionTest.setObjectName(_fromUtf8("actionTest"))
        self.actionAddDirTab = QtGui.QAction(MainWindow)
        self.actionAddDirTab.setObjectName(_fromUtf8("actionAddDirTab"))
        self.actionNew_dir = QtGui.QAction(MainWindow)
        self.actionNew_dir.setObjectName(_fromUtf8("actionNew_dir"))
        self.actionOpen_outline = QtGui.QAction(MainWindow)
        self.actionOpen_outline.setObjectName(_fromUtf8("actionOpen_outline"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_all = QtGui.QAction(MainWindow)
        self.actionSave_all.setObjectName(_fromUtf8("actionSave_all"))
        self.actionUndo = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/image/image/undo_64px_1188189_easyicon.net.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUndo.setIcon(icon)
        self.actionUndo.setObjectName(_fromUtf8("actionUndo"))
        self.actionRedo = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/image/image/redo_64px_1188145_easyicon.net.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRedo.setIcon(icon1)
        self.actionRedo.setObjectName(_fromUtf8("actionRedo"))
        self.menuFile.addAction(self.actionTest)
        self.menuFile.addAction(self.actionAddDirTab)
        self.menuFile.addAction(self.actionNew_dir)
        self.menuFile.addAction(self.actionOpen_outline)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_all)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSave_all)
        self.toolBar.addAction(self.actionUndo)
        self.toolBar.addAction(self.actionRedo)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuFile.setTitle(_translate("MainWindow", "file", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionTest.setText(_translate("MainWindow", "here", None))
        self.actionAddDirTab.setText(_translate("MainWindow", "addDirTab", None))
        self.actionNew_dir.setText(_translate("MainWindow", "new_dir", None))
        self.actionOpen_outline.setText(_translate("MainWindow", "open_outline", None))
        self.actionSave.setText(_translate("MainWindow", "save", None))
        self.actionSave_all.setText(_translate("MainWindow", "save_all", None))
        self.actionUndo.setText(_translate("MainWindow", "undo", None))
        self.actionRedo.setText(_translate("MainWindow", "redo", None))

import mainwin_rc
