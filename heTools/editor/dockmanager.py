# -*- encoding:utf8 -*-
from PyQt4.QtCore import QObject
from heQt.dock import DockPanel
from dir_tool_tab import DirToolTab

if 0:
    from main import MainWin,Dock
    
class DockManager(QObject):
    def __init__(self, dock,mainwin):
        super(DockManager,self).__init__(mainwin)
        if 0:
            assert isinstance(mainwin,MainWin)
            assert isinstance(dock,Dock)
            
        self.mainwin=mainwin
        self.dock=dock
        
        self.mainwin.actionAddDirTab.triggered.connect(self.addDirTab)
        
    def addDirTab(self):
        self.panel1=DockPanel()
        self.dock.addLeft(self.panel1)  
        self.panel1.addTab(DirToolTab(),u'快捷目录')    