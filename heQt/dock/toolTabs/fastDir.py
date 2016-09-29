# -*- encoding:utf8 -*-
from heQt.qteven import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from os.path import join
from heStruct.heSignal import reciver,connect,fire
from heQt.model.stdmodel import childs,walk
from heOs.heio import open_with_os
from heOs.windows.fileope import recycle_path
import os.path

class FastDirTab(QTreeView):
    """
    SIGNAL:　fastDir_doubleClicked
    """
    def __init__(self, parent=None):
        super(FastDirTab,self).__init__(parent)
        self._model=QStandardItemModel()
        self.setModel(self._model)
        self.PATH_DATA=Qt.UserRole+1
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setContextMenuPolicy(Qt.DefaultContextMenu)
        
        acts=[(u'新建文件',self.new_file),
              (u'新建文件夹',self.new_dir),
              ('rename',self.rename),
              ('refresh',self.refresh),
              ('seperator',''),
              (u'使用系统打开',self.open_with_os),
              (u'删除到回收站',self.recycle)]
        
        for label,fun in acts:
            act=QAction(label,self)
            if not fun:
                act.setSeparator(True)
            else:
                act.triggered.connect(fun)
            self.addAction(act)

        self.setEditTriggers(QTreeView.NoEditTriggers)
        self.expanded.connect(self.expand_index)
        self.doubleClicked.connect(self.on_db_clicked)
        
    def new_dir(self):
        try:
            item=self._current_valid_item()
            path=item.data(self.PATH_DATA)
            if not QFileInfo(path).isDir():
                item=item.parent()
                path=item.data(self.PATH_DATA)
            name,valid=QInputDialog.getText(self,u'新建文件夹',u'文件夹名')
            if valid and name:
                abs_path=os.path.join(path,name)
                os.mkdir(abs_path)
                child= self._creae_item_from_path(abs_path)
                item.appendRow(child)
        except UserWarning as e:
            print(e)
        except IOError as e:
            print(e)
    
    def refresh(self):
        paths=self.get_root_paths()
        self.model().clear()
        for p in paths:
            self.add_path(p)
    
    def rename(self):
        try:
            item=self._current_valid_item()
            old_name=item.data(Qt.DisplayRole)
            parent=item.parent()
            if not parent:
                return
            path=parent.data(self.PATH_DATA)
            name,yes=QInputDialog.getText(self,u'改名',u'文件名',text=old_name)
            if yes and name:
                self._rename(path,old_name,name)
                item.setData(name,Qt.DisplayRole)
                item.setData(os.path.join(path,name),self.PATH_DATA)
                
        except UserWarning as e:
            print(e)
                
    def _rename(self,path,old,new):
        p_path=os.path.join(path,new)
        if os.path.exists(p_path):
            raise UserWarning,'file already exist, file name is %s'%new
        elif not QDir(path).rename(old,new):
            raise UserWarning,'QDir rename error'
    
    def new_file(self):
        try:
            item = self._get_current_dir_item()
            path=item.data(self.PATH_DATA)
            name,valid=QInputDialog.getText(self,u'新建文件',u'文件名')
            if valid and name:
                file_path=join(path,name)
                with open(file_path,'w') as f:
                    pass
                child= self._creae_item_from_path(file_path)
                item.appendRow(child)
        except UserWarning as e:
            print(e)
        except IOError as e:
            print(e)
            
    def _get_current_dir_item(self):
        """
        如果当前item不是文件夹，则返回它的parent
        """
        item=self._current_valid_item()
        path=item.data(self.PATH_DATA)
        if not QFileInfo(path).isDir():
            item=item.parent()
        return item    
    
    def _creae_item_from_path(self,abs_path):
        f=QFileInfo(abs_path)
        name=f.fileName()
        child=QStandardItem(QFileIconProvider().icon(f),name)
        child.setData(abs_path,self.PATH_DATA) 
        return child        
    
    def _new_dir_under_dir(self,abs_path):
        #QDir(abs_path).
        try:
            os.mkdir(abs_path)
        except IOError as e:
            raise UserWarning,'mkdir has error ,when create %s '%(abs_path)
        #if not QDir(path).mkdir(name):
            #raise UserWarning,'mkdir has error when use QDir create %s / %s'%(path,name)
        
    #def _create_file_and_item(self,path,name):
        #file_path=join(path,name)
        #self._new_file_under_dir(file_path)
        #child=QStandardItem(name)
        #child.setData(file_path,self.PATH_DATA) 
        #return child
    
    def _current_valid_item(self):
        index=self._current_valid_index()
        return self.model().itemFromIndex(index)
    
    def _current_valid_index(self):
        index=self.currentIndex()
        if index.isValid(): 
            return index
        else:
            raise UserWarning,'no invalide index'
        
    def _new_file_under_dir(self,file_path):
        if not os.path.exists(file_path):
            with open(file_path,'w') as f:
                pass
        else:
            raise UserWarning,'file has been exist When creat new file. file name is %s'%file_path
        
    def recycle(self):
        try:
            index=self._current_valid_index()
            path=index.data(self.PATH_DATA)
            if QMessageBox.warning(None,u'警告',u'是否要删除 %s'%path,QMessageBox.Yes|QMessageBox.No)==QMessageBox.No:
                return
            code=recycle_path(path)
            if code==0:    
                self.model().removeRow(index.row(),index.parent())
            else:
                raise UserWarning,'recycel error ,error code is %s'%code
        except UserWarning as e:
            print(e)
    
    def open_with_os(self):
        try:
            index=self._current_valid_index()
            path=index.data(self.PATH_DATA)
            open_with_os(path)
        except UserWarning as e:
            print(e)
    
    def on_db_clicked(self,index):    
        fire('fastDir_doubleClicked',index.data(self.PATH_DATA) )
    
    def get_context_actions(self,dc):
        """
        ToDo:改进 action的过滤方式。
        """
        if not hasattr(self,'_actions'):
            act_data=[# {'label':'rename'},  
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
        menu.addActions(self.actions())
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
            'paths':self.get_root_paths(),
            'expaned':self._get_expaned_paths()}
        return self.__class__,tuple(),dc
    
    def get_root_paths(self):
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