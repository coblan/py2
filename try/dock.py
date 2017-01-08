# -*- encoding:utf8 -*-
from heQt.qteven import *
from PyQt4.QtGui import QApplication,QMainWindow,QWidget
from heQt.dock import Dock,DockPanel
import sys
import json
import pickle

class Win(QMainWindow):
    def __init__(self,p=None):
        super(Win,self).__init__(p)
        self.dock=Dock()
        self.setCentralWidget(self.dock)
        self.dock.setCentralWidget(QWidget())
    def closeEvent(self,event):
        dc={'dock':self.dock.save(),
            'geo':pickle.dumps(self.saveGeometry())}
        with open('d:/try/docktest','w') as f:
            json.dump(dc,f)
        super(Win,self).closeEvent(event)
    

class ToolWin(QWidget):
    def __reduce__(self):
        return self.__class__,tuple(),self.windowTitle()
    def __setstate__(self,state):
        self.setWindowTitle(state)

def test():
    print('it is null')
    panel1=DockPanel()
    panel1.addTab(ToolWin(),u'中文')
    # win.setCentralWidget(dock)
    # dock.setCentralWidget(QWidget())
    win.dock.addLeft(panel1)
    win.show()    
if __name__=='__main__':
    app=QApplication(sys.argv)
    win=Win()
    try:
        with open('d:/try/docktest') as f:
            dc=json.load(f)
            if dc:
                win.restoreGeometry(pickle.loads(dc['geo']))
                win.dock.restore(dc['dock'])
                win.show()
            else:
                test()
    except:
        test()
    
    # test()
    
    
    sys.exit(app.exec_())