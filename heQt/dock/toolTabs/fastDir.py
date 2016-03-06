# -*- encoding:utf8 -*-
from heQt.qteven import *
from PyQt4.QtGui import *
from PyQt4.QtCore import QDir,QFileInfo,Qt,QModelIndex
from os.path import join
from heStruct.heSignal import reciver,connect,fire
from heQt.model.stdmodel import childs,walk

class FastDirTab(QTreeView):
    def __init__(self, parent=None):
        super(FastDirTab,self).__init__(parent)
        self._model=QStandardItemModel()
        self.setModel(self._model)
        self.PATH_DATA=Qt.UserRole+1
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setContextMenuPolicy(Qt.DefaultContextMenu)
        connect('new_dir', self.add_path)
        self.setEditTriggers(QTreeView.NoEditTriggers)
        self.expanded.connect(self.expand_index)
        self.doubleClicked.connect(self.on_db_clicked)
        
    def on_db_clicked(self,index):    
        fire('open_file',index.data(self.PATH_DATA) )
    
    def get_context_actions(self,dc):
        if not hasattr(self,'_actions'):
            act_data=[{'label':'rename'},
                      {'label':u'移出快捷目录','show':'under_cursor_is_root_dir','func':self.exclude_current_root_dir}]
            self._actions=self._create_actions(act_data)
        actions =self._filter_action_show(self._actions,dc)
        return actions
        
    def _create_actions(self,datas):
        acts=[]
        for data in datas:
            if data.get('label'):
                act=QAction(data.get('label'),self)
                act.org_dc=data
                if data.get('func'):
                    act.triggered.connect(data.get('func'))
                acts.append(act)
        return acts
    
    def _filter_action_show(self,actions,dc):
        acts=[]
        for act in actions:
            condition=act.org_dc.get('show')
            if not condition or dc.get(condition):
                acts.append(act)
        return acts
    
    def exclude_current_root_dir(self):
        index=self.currentIndex()
        if index.parent()==QModelIndex():
            self.model().removeRow(index.row())
        
    def contextMenuEvent(self,event):
        globle_pos=self.viewport().mapToGlobal(event.pos())
        dc={}
        index=self.indexAt(event.pos())
        if index.isValid() and index.parent()==QModelIndex():
            dc['under_cursor_is_root_dir']=True
        actions=self.get_context_actions(dc)
        menu=QMenu()
        menu.addActions(actions)
        menu.exec_(globle_pos)        
    
    def add_path(self,dir_path):
        f=QFileInfo(dir_path)
        parent=QStandardItem(QFileIconProvider().icon(f),dir_path)
        parent.setData(dir_path,self.PATH_DATA)
        self.model().appendRow(parent)
        self.fake_expand_arrow(parent)
    
    def expand_index(self,index):
        item=self.model().itemFromIndex(index)
        c0=item.child(0)
        if c0.data(Qt.DisplayRole)=='for_fack_arrow':
            item.removeRow(0)
            self.build_child_dir_item(item)
            row_cnt=item.rowCount()
            for c in range(row_cnt):
                self.fake_expand_arrow(item.child(c) )
            
    def fake_expand_arrow(self,parent):
        path=parent.data(self.PATH_DATA)
        if QDir(path).count()>2:  # 2 是因为有 . 和 .. 目录
            parent.appendRow(QStandardItem('for_fack_arrow'))
            
    def build_child_dir_item(self,parent):
        p_path=parent.data(self.PATH_DATA)
        for f in QDir(p_path).entryInfoList(QDir.AllEntries|QDir.NoDotAndDotDot,sort=QDir.DirsFirst):
            item=QStandardItem(QFileIconProvider().icon(f),f.fileName())
            item.setData(join(p_path,f.fileName()))
            parent.appendRow(item)
            QApplication.processEvents()
            
    def dropEvent(self,event):
        mim = event.mimeData()
        if mim.hasUrls():
            for url in mim.urls ():
                self.add_path(url.toLocalFile())
        
    def dragEnterEvent(self, event):
        mim = event.mimeData()
        if mim.hasUrls():
            event.acceptProposedAction() 
        
    def tabbarAction(self):
        return []
    
    def __reduce__(self):
        
        dc={'title':self.windowTitle(),
            'paths':self._get_all_paths(),
            'expaned':self._get_expaned_paths()}
        return self.__class__,tuple(),dc
    
    def _get_all_paths(self):
        paths=[]
        for item in childs(self.model()):
            paths.append(item.data(self.PATH_DATA ))        
        return paths
    def _get_expaned_paths(self):
        expaned=[]
        for p,item in walk(self.model()):
            if self.isExpanded(item.index() ):
                expaned.append(item.data(self.PATH_DATA) )
        return expaned
    
    def __setstate__(self,state):
        self.setWindowTitle(state['title'])
        paths=state.get('paths',[])
        for path in paths:
            self.add_path(path)
        expaned=state.get('expaned',[])
        self._expaned_from_saved_path(expaned)
        
    def _expaned_from_saved_path(self,pathes):
        for p,item in walk(self.model()):
            if item.data(self.PATH_DATA) in pathes:
                self.expand(item.index())



if __name__=='__main__':
    from PyQt4.QtGui import QApplication
    app=QApplication([])
    win=FastDirTab()
    win.show()
    app.exec_()