
from PyQt4.QtGui import QTreeView,QStandardItem,QStandardItemModel,QFileIconProvider
from PyQt4.QtCore import QDir,QFileInfo
from os import walk
from heStruct.heSignal import reciver,connect


class FastDirTab(QTreeView):
    def __init__(self, parent=None):
        super(FastDirTab,self).__init__(parent)
        self._model=QStandardItemModel()
        self.setModel(self._model)
        connect('new_dir', self.addDir)
        
    def addDir(self,dir_path):
        for f in QDir(dir_path).entryInfoList(QDir.AllEntries|QDir.NoDotAndDotDot,sort=QDir.DirsFirst):
            item=QStandardItem(QFileIconProvider().icon(f),f.baseName())
            if f.isDir():
                child_dir=f.dir()
                child_dir.cd(f.baseName())
                self.update_child_dir(item,child_dir.absolutePath() )
            self.model().appendRow(item)
    
    def update_child_dir(self,parent,path):
        for f in QDir(path).entryInfoList(QDir.AllEntries|QDir.NoDotAndDotDot,sort=QDir.DirsFirst):
            child=QStandardItem(QFileIconProvider().icon(f),f.baseName())
            parent.appendRow(child)
    
    def __reduce__(self):
        dc={'title':self.windowTitle()}
        return self.__class__,tuple(),dc
    
    def __setstate__(self,state):
        self.setWindowTitle(state['title'])