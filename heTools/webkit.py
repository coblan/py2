import sys
import os
from heQt.qteven import *
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl,QObject,pyqtSlot, pyqtProperty
from PyQt4.QtWebKit import QWebView
import json

   
def main(url,obj=None):
    app = QApplication(sys.argv)
    win =QWebView()

    win.load( QUrl(url))
    # win.page().mainFrame().addToJavaScriptWindowObject('qt',obj)
    win.show()
    if obj:
        win.page().mainFrame().addToJavaScriptWindowObject('qt',obj)
        obj.frame = win.page().mainFrame()
    sys.exit(app.exec_())
    
if __name__=='__main__':
    main('sync/sync.html')