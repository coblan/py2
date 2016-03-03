# -*- encoding:utf8 -*-
from heQt.qteven import *
import sys
from PyQt4.QtGui import QApplication,QMainWindow,QTabWidget,QWidget
from heQt.code_editor import CodeEditor
from heQt.dock import Dock,DockPanel
from ui.mainwin_ui import Ui_MainWindow
import pickle

from dockmanager import DockManager

class MainWin(QMainWindow,Ui_MainWindow):
    def __init__(self,p=None):
        super(MainWin,self).__init__(p)
        self.setupUi(self)
        
        self.dock=Dock()
        self.tabwin=QTabWidget()
        self.setCentralWidget(self.dock)
        self.dock.setCentralWidget(self.tabwin)
        self.dockmanager=DockManager(self.dock,self)
        
        self.actionTest.triggered.connect(self.test)

    def test(self):
        self.panel1=DockPanel()
        self.dock.addLeft(self.panel1)
        self.panel1.addTab(QWidget(),u'浮冰')
        self.tabwin.addTab(CodeEditor(),'ri')
    
    def load_settings(self):
        with open('auto/state') as f:
            dc=pickle.load(f)
            self.restoreGeometry(dc['geo'])
            self.dock.restore(dc['dock'])
    
    def save_state(self):
        geo=self.saveGeometry()
        dock=self.dock.save()
        dc={'geo':geo,
            'dock':dock
        }
        with open('auto/state','w') as f:
            pickle.dump(dc,f)
    
    def closeEvent(self,event):
        self.save_state()
        super(MainWin,self).closeEvent(event)
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    win=MainWin()
    win.show()
    try:
        win.load_settings()
    except IOError as e:
        print(e)
    
    sys.exit(app.exec_())