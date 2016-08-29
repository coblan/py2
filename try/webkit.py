import sys
import os
from heQt.qteven import *
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl,QObject,pyqtSlot, pyqtProperty
from PyQt4.QtWebKit import QWebView
import json

class Dog(QObject):
    def __init__(self, parent=None):
        super(Dog,self).__init__()
        self._name='dog'
    
    @pyqtProperty(str)
    def name(self):
        print('heere')
        return self._name
    
    @pyqtSlot(str)
    def set_name(self,name):
        self._name=name
    
    @pyqtSlot()
    def say(self):
        print(self._name)
        
    @pyqtSlot(str,result=str)
    def listdirs(self,path):
        ls = os.listdir(path)
        return json.dumps(ls)
    
    @pyqtSlot(str,result=str)
    def open(self,path):
        with open(path) as f:
            return f.read()
    
if __name__=='__main__':
    app = QApplication(sys.argv)
    win =QWebView()
    dog=Dog()
   
    win.load( QUrl('index.html'))
    
    win.page().mainFrame().addToJavaScriptWindowObject('dog',dog)
    win.show()
    win.page().mainFrame().addToJavaScriptWindowObject('dog',dog)
    sys.exit(app.exec_())