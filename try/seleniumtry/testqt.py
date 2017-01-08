import sys
from PyQt4.QtGui import QApplication,QPushButton
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView,QWebSettings


def get_content():
    print('here')
    # ss=r"""
    # var ga = document.createElement('script');   
    # ga.type = 'text/javascript';   
    # ga.async = true;  
    # ga.src= "http://apps.bdimg.com/libs/jquery/1.11.1/jquery.min.js"
    # document.body.appendChild(ga);
    # """
    # web.page().mainFrame().evaluateJavaScript("alert($('h3'))")
    fram =  web.page().mainFrame()
    ls = fram.findAllElements('h3 a').toList()
    for a in ls:
        print(a.attribute('href'))
    ls= fram.findAllElements('#navcnt a').toList()
    print('='*30)
    for a in ls:
        print(a.attribute('href'))    

if __name__=='__main__':
    app = QApplication(sys.argv)
    web = QWebView()
    # settings= web.settings()
    # settings.setAttribute(QWebSettings.JavascriptEnabled, True)
    # settings.setAttribute(QWebSettings.JavascriptCanOpenWindows, True)   
    web.show()
    web.load(QUrl('http://www.google.com'))
    
    # web.load(QUrl('http://pts.mokitech.com'))
    
    btn= QPushButton('click')
    btn.clicked.connect(get_content)
    
    btn.show()
    sys.exit(app.exec_())

