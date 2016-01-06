# -*- encoding:utf8 -*-

import sys,os
from heQt.qteven import *
from PyQt4.QtGui import QTreeView,QStandardItemModel

from qt_.widget.itemView import TreeView
from qt_.model_.itemModel import treeModel
from subprocess import Popen
from string import Template

class aux(QObject):
    def __init__(self, tree_,info_):
        super(aux,self).__init__()
        self.tree=tree_
        self.info=info_
    def add(self):
        idx=self.tree.ctxMenuIdx
        self.tree.model().append(QStandardItem('new item'),idx if idx else None)
    
    def delete(self):
        idx=self.tree.ctxMenuIdx
        if idx.isValid():
            if QMessageBox.information(None,'warn','realy delete?%s'%idx.data())==QMessageBox.Ok:
                self.tree.model().remove(idx)
    
    def run(self):
        scope={}
        exec(self.info.toPlainText(),scope)
        cmd=scope.get("cmd","can'g find cmd!")
        f=open('tmp.bat','w')
        if 'var' in scope:
            cmd=Template(cmd).substitute(scope["var"])
            
        f.write(cmd)
        f.close()
        pop=Popen('cmd /k %s/tmp.bat'%os.getcwd(),universal_newlines=True)
    
    def save(self):
        idx=self.tree.currentIndex()
        self.tree.model().itemFromIndex(idx).setData(self.info.toPlainText(),Qt.UserRole+1)
        self.tree.model().save('confing')

class TreeView(QTreeView):
    def __init__(self,parent=None):
        super(TreeView,self).__init__(parent)
        self.setModel(QStandardItemModel())
        
        
def indexChanged(self,cur,pre):
    if pre.isValid():
        self.model().itemFromIndex(pre).setData(self.info.toPlainText(),Qt.UserRole+1)
    self.info.setPlainText(cur.data(Qt.UserRole+1))
    return QAbstractItemView.currentChanged(self,cur,pre)

TreeView.currentChanged=indexChanged

class win(QSplitter):
    #def __init__(self, *args, **kwargs):
        #super(win,self).__init__(*args, **kwargs)
        
    def closeEvent(self,evnt):
        stns=QSettings('stns',QSettings.IniFormat)
        stns.setValue('win/geo',self.saveGeometry())
        stns.setValue("win/split",self.saveState())
        QWidget.closeEvent(self,evnt)
    

if __name__=='__main__':
    os.chdir('cmdgui')
    app=QApplication(sys.argv)
    mainWin=win(None)
    mainWin.setWindowTitle(u'命令行界面版')
    #lay=QSplitter()
    
    tree=TreeView()
    info=QTextEdit()
    auOb=aux(tree,info)
    tree.info=info
    mode=treeModel(None)
    mode.open('confing')
    
    tree.setModel(mode)

    tree.addAction('run').triggered.connect(auOb.run)
    act=QAction(None)
    act.setSeparator(True)
    tree.addAction(act)
    tree.addAction('add').triggered.connect(auOb.add)
    tree.addAction('delete').triggered.connect(auOb.delete)
    
    tree.addAction('save').triggered.connect(auOb.save)
    
    mainWin.addWidget(tree)
    mainWin.addWidget(info)
    
    #mainWin.setLayout(lay)
    mainWin.show()
    stns=QSettings('stns',QSettings.IniFormat)
    mainWin.restoreGeometry(stns.value('win/geo'))
    mainWin.restoreState(stns.value("win/split"))
    
    sys.exit(app.exec_())