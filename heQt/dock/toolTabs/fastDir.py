
from PyQt4.QtGui import QTreeView,QStandardItem,QStandardItemModel,QFileIconProvider
from PyQt4.QtCore import QDir,QFileInfo,Qt
from os import walk
from os.path import join
from heStruct.heSignal import reciver,connect


class FastDirTab(QTreeView):
    def __init__(self, parent=None):
        super(FastDirTab,self).__init__(parent)
        self._model=QStandardItemModel()
        self.setModel(self._model)
        
        self.PATH_DATA=Qt.UserRole+1
        
        connect('new_dir', self.addDir)
        
        self.expanded.connect(self)
        
    def addDir(self,dir_path):
        f=QFileInfo(dir_path)
        parent=QStandardItem(QFileIconProvider().icon(f),dir_path)
        parent.setData(dir_path,self.PATH_DATA)
        self.model().appendRow(parent)
        self.build_child_dir_item(parent)
        # for f in QDir(dir_path).entryInfoList(QDir.AllEntries|QDir.NoDotAndDotDot,sort=QDir.DirsFirst):
            # item=QStandardItem(QFileIconProvider().icon(f),f.baseName())
            # if f.isDir():
                # child_dir=f.dir()
                # child_dir.cd(f.baseName())
                # self.update_child_dir(item,child_dir.absolutePath() )
            # parent.appendRow(item)
    
    def build_child_dir_item(self,parent):
        p_path=parent.data(self.PATH_DATA)
        for f in QDir(p_path).entryInfoList(QDir.AllEntries|QDir.NoDotAndDotDot,sort=QDir.DirsFirst):
            item=QStandardItem(QFileIconProvider().icon(f),f.baseName())
            item.setData(join(p_path,f.baseName()))
            parent.appendRow(item)
            
    
    def tabbarAction(self):
        pass
    
    def update_child_dir(self,parent,path):
        for f in QDir(path).entryInfoList(QDir.AllEntries|QDir.NoDotAndDotDot,sort=QDir.DirsFirst):
            child=QStandardItem(QFileIconProvider().icon(f),f.baseName())
            parent.appendRow(child)
    
    def __reduce__(self):
        dc={'title':self.windowTitle()}
        return self.__class__,tuple(),dc
    
    def __setstate__(self,state):
        self.setWindowTitle(state['title'])