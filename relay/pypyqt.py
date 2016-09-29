import sys
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView
from PyQt4.QtGui import QApplication
import time

def func():
    view.page().mainFrame().evaluateJavaScript('alert($("[name=metadata1]").attr("type"))')

if __name__=='__main__':
    app=QApplication(sys.argv)
    view = QWebView()
    view.load(QUrl("https://developer.amazon.com/home.html") )
    # view.show()
    view.loadFinished.connect(func)
    
    
    
    sys.exit(app.exec_() )