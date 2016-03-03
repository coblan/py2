# -*- encoding:utf8 -*-
from heQt.qteven import *
import sys
import os
from subprocess import Popen
from string import Template
from PyQt4.QtGui import QTreeView, QStandardItemModel, QSplitter, QMessageBox, QApplication, QTextEdit, QStandardItem,\
     QAction,QMenu
from PyQt4.QtCore import QObject, Qt, QSettings, QModelIndex
from heQt.model.stdmodel import save_model,load_model,walk,childs
import pickle
import json

class CmdWin(QSplitter):
    
    def __init__(self, *args, **kwargs):
        super(CmdWin, self).__init__(*args, **kwargs)
        self.setWindowTitle(u'命令行界面版')
        self.tree = TreeView(self)
        self.info = QTextEdit()
        self.auOb = Logic(self.tree, self.info)
        self.addWidget(self.tree)
        self.addWidget(self.info)
        #self.setContextMenuPolicy(Qt.ActionsContextMenu)
        acs=['run',
            "add",
            'delete',
            'save' ]
        for k  in acs:
            ac=QAction(k,self)
            ac.triggered.connect(getattr(self.auOb,k))
            self.addAction(ac)  
        
        self.tree.index_changed.connect(self.on_tree_index_changed)
        
    def contextMenuEvent(self,event):
        globle_pos=self.mapToGlobal(event.pos())
        self.auOb.cursor_pos=self.tree.viewport().mapFromGlobal(globle_pos)
        menu=QMenu()
        menu.addActions(self.actions())
        menu.exec_(globle_pos)
    
    def on_tree_index_changed(self, cur, pre):
        """

        @type cur: QModelIndex
        @type pre: QModelIndex
        """
        if pre.isValid():
            self.tree.model().itemFromIndex(pre).setData(self.info.toPlainText(), Qt.UserRole + 1)
        self.info.setPlainText(cur.data(Qt.UserRole + 1))


    def load_settings(self):
        try:
            stns = QSettings('stns', QSettings.IniFormat)
            self.restoreGeometry(stns.value('win/geo'))
            self.restoreState(stns.value("win/split"))
        except TypeError:
            pass
        
        try:
            load_cmd(self.tree.model())
            load_expand(self.tree, self.tree.model())
        except IOError as e:
            print(e)        

    def closeEvent(self, evnt):
        stns = QSettings('stns', QSettings.IniFormat)
        stns.setValue('win/geo', self.saveGeometry())
        stns.setValue("win/split", self.saveState())
        save_cmd(self.tree.model())
        save_expand(self.tree,self.tree.model())
        super(CmdWin, self).closeEvent(evnt)
        

class TreeView(QTreeView):
    index_changed = pyqtSignal(QModelIndex, QModelIndex)

    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.setModel(QStandardItemModel())
        

    def currentChanged(self, cur, pre):
        self.index_changed.emit(cur, pre)
        return super(TreeView, self).currentChanged( cur, pre)


class Logic(QObject):
    def __init__(self, tree_, info_):
        super(Logic, self).__init__()
        # assert isinstance(self.info, QTextEdit)
        self.tree = tree_
        self.info = info_
        self.cursor_pos=None
    
    def under_mouse_index(self):
        return self.tree.indexAt(self.cursor_pos)
    
    def add(self):
        #idx = self.tree.ctxMenuIdx
        idx= self.under_mouse_index()
        model=self.tree.model()
        if idx.isValid():
            item=self.tree.model().itemFromIndex(idx)
            item.appendRow(QStandardItem('new item'))            
        else:
            self.tree.model().appendRow(QStandardItem('new item'))

    def delete(self):
        idx = self.under_mouse_index()
        if idx.isValid():
            if QMessageBox.information(None, 'warn', 'realy delete?%s' % idx.data()) == QMessageBox.Ok:
                self.tree.model().removeRow(idx.row(),idx.parent() )

    def run(self):
        scope = {}
        exec (self.info.toPlainText(), scope)
        cmd = scope.get("cmd", "can'g find cmd!")
        f = open('tmp.bat', 'w')
        if 'var' in scope:
            cmd = Template(cmd).substitute(scope["var"])

        f.write(cmd)
        f.close()
        Popen('cmd /k %s/tmp.bat' % os.getcwd(), universal_newlines=True)

    def save(self):
        idx = self.tree.currentIndex()
        self.tree.model().itemFromIndex(idx).setData(self.info.toPlainText(), Qt.UserRole + 1)
        self.tree.model()
        save_cmd(self.tree.model())

def load_cmd(model):
    with open('cmd') as f:
        items=json.load(f)
        _load_item_child(model,items)

def load_expand(tree,model):
    with open('expaned') as f:
        ls=pickle.load(f)
        cnt=0
        for p,c in walk(model):
            cnt+=1
            if cnt in ls:
                tree.expand(p.index())
        
        
def _load_item_child(p,childs):
    for child in childs:
        child_item=QStandardItem(child['name'])
        child_item.setData(child['data'],Qt.UserRole+1)
        _load_item_child(child_item,child['childs'])
        p.appendRow(child_item)


        
def save_cmd(model):
    s=_save_item_child(model)
    with open('cmd','w') as f:
        json.dump(s,f)  
        

def _save_item_child(item):
    out=[]
    for child in childs(item):
        dc={'name':child.data(Qt.DisplayRole),
            'childs':_save_item_child(child),
            'data':child.data(Qt.UserRole + 1)}
        out.append(dc)
    return out

def save_expand(tree,model):
    cnt=0
    expaned=[]
    for p,c in walk(model):
        cnt+=1
        if isinstance(p,QStandardItemModel):
            continue
        if tree.isExpanded(p.index()):
            expaned.append(cnt)
    with open('expaned','w') as f:
        pickle.dump(expaned,f)
        
if __name__ == '__main__':
    os.chdir('cmdgui')
    app = QApplication(sys.argv)
    mainWin = CmdWin()


    # lay=QSplitter()

    # tree = TreeView()
    # info = QTextEdit()
    # auOb = aux(tree, info)
    # tree.info = info
    # mode = treeModel(None)
    # mode.open('confing')
    #
    # tree.setModel(mode)
    #
    # tree.addAction('run').triggered.connect(auOb.run)
    # act = QAction(None)
    # act.setSeparator(True)
    # tree.addAction(act)
    # tree.addAction('add').triggered.connect(auOb.add)
    # tree.addAction('delete').triggered.connect(auOb.delete)
    #
    # tree.addAction('save').triggered.connect(auOb.save)
    #
    # mainWin.addWidget(tree)
    # mainWin.addWidget(info)

    # mainWin.setLayout(lay)
    mainWin.show()
    mainWin.load_settings()

    sys.exit(app.exec_())
