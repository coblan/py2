# -*- encoding:utf8 -*-
from heQt.qteven import *
import sys
from PyQt4.QtGui import QApplication,QMainWindow,QTabWidget,QWidget
from heQt.code_editor import CodeEditor
from heQt.dock import Dock,DockPanel
class MainWin(QMainWindow):
    def __init__(self,p=None):
        super(MainWin,self).__init__(p)
        self.dock=Dock()
        self.tabwin=QTabWidget()
        self.setCentralWidget(self.dock)
        self.dock.setCentralWidget(self.tabwin)
        
        self.panel1=DockPanel()
        self.dock.addLeft(self.panel1)
        self.panel1.addTab(QWidget(),u'浮冰')
        self.tabwin.addTab(CodeEditor(),'ri')

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=MainWin()
    win.show()
    sys.exit(app.exec_())