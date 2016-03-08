# -*- encoding:utf8 -*-
from heQt.qteven import *
import sys
from PyQt4.QtGui import QApplication,QMainWindow,QWidget,QStatusBar,QLabel
from heQt.code_editor import CodeEditor
from heQt.dock import Dock,DockPanel
from ui.mainwin_ui import Ui_MainWindow
import pickle
from heStruct.heSignal import connect
from dockmanager import DockManager
from editormanager import EditorManager

class MainWin(QMainWindow,Ui_MainWindow):
    def __init__(self,p=None):
        super(MainWin,self).__init__(p)
        self.setupUi(self)
        
        self.dock=Dock()
        self.editors=EditorManager()
        self.setCentralWidget(self.dock)
        self.dock.setCentralWidget(self.editors)
        self.dockmanager=DockManager(self.dock,self)
        #status_bar=QStatusBar()
        #self.setStatusBar(status_bar)
        self.encode_labe=QLabel()
        self.encode_labe.setStyleSheet('margin-right: 20px;')
        self.statusBar().addPermanentWidget(self.encode_labe)
        self.actionTest.triggered.connect(self.test)
        # connect('code_encoding',self.show_encoding)
        self.actionSave.triggered.connect(self.editors.save_current_content)
        self.actionUndo.triggered.connect(self.editors.undo)
        self.actionRedo.triggered.connect(self.editors.redo)
        self.editors.undoStateChanged.connect(self.set_undo_state)
        self.editors.currentEncodeChanged.connect(self.show_encoding)
        
    def set_undo_state(self,undo,redo):
        self.actionUndo.setEnabled(undo)
        self.actionRedo.setEnabled(redo)
        
    def show_encoding(self,encode):
        self.encode_labe.setText(encode)
        
    def test(self):
        self.panel1=DockPanel()
        self.dock.addLeft(self.panel1)
        self.panel1.addTab(QWidget(),u'浮冰')
        self.editors.addTab(CodeEditor(),'ri')
    
    def load_settings(self):
        with open('auto/state') as f:
            dc=pickle.load(f)
            self.restoreGeometry(dc['geo'])
            self.dock.restore(dc['dock'])
            self.editors.restore(dc.get('editors'))
    
    def save_state(self):
        geo=self.saveGeometry()
        dock=self.dock.save()
        editors=self.editors.save()
        dc={'geo':geo,
            'dock':dock,
            'editors':editors
        }
        with open('auto/state','w') as f:
            pickle.dump(dc,f)
    
    def closeEvent(self,event):
        self.save_state()
        super(MainWin,self).closeEvent(event)
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    win=MainWin()
    try:
        win.load_settings()
    except IOError as e:
        print(e)
    win.show()
    sys.exit(app.exec_())