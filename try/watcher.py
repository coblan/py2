# -*- encoding:utf8 -*-
import sys
from heQt.qteven import *
from PyQt4.QtGui import *
from PyQt4.QtCore import QFileSystemWatcher
import os.path
from heOs.syndir import walk

class MyWatch(QFileSystemWatcher):
    def __init__(self, parent=None):
        super(MyWatch,self).__init__(parent)
        for b,d,f in walk(ur'D:\try\dirtry'):
            for dd in d:
                path =os.path.join(b,dd)
                self.addPath(path)
            for ff in f:
                path =os.path.join(b,ff)
                self.addPath(path)                
        self.directoryChanged.connect(self.dir_changed)
        self.fileChanged.connect(self.on_file_changed)
    
    def dir_changed(self,d):
        for f in os.listdir(d):
            self.addPath(os.path.join(d,f))
        print('dir changed')
    
    def on_file_changed(self,f):
        print('file changed :%s'%f)
        print(os.path.relpath(f,ur'D:\try\dirtry'))
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    wat=MyWatch()
    
    sys.exit(app.exec_())