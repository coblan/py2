# -*- encoding:utf8 -*-
from PyQt4.QtCore import QObject
from heQt.dock import DockPanel
#from dir_tool_tab import DirToolTab
from heQt.dock.toolTabs.fastDir import FastDirTab
from heQt.dock.toolTabs.outline import Outline
from heStruct.heSignal import fire
import os
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
        self.mainwin.actionNew_dir.triggered.connect(self.newdir)
        self.mainwin.actionOpen_outline.triggered.connect(self.open_outline)
    
    def newdir(self):
        fire("new_dir",os.getcwd())
    def open_outline(self):
        outline=Outline()
        self.dock.add_tab(outline,u'大纲')
        
    def addDirTab(self):
        self.panel1=DockPanel()
        self.dock.addLeft(self.panel1)  
        self.panel1.addTab(FastDirTab(),u'快捷目录')    