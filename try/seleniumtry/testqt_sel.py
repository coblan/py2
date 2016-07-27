import sys
from PyQt4.QtGui import QApplication,QPushButton

from selenium import webdriver
#from PyQt4.QtCore import QUrl
#from PyQt4.QtWebKit import QWebView,QWebSettings


def get_content():
    print('here')
    print driver.title 

if __name__=='__main__':
    app = QApplication(sys.argv)
  
    driver = webdriver.Chrome()
    
    # go to the google home page
    driver.get("http://www.baidu.com")    
    
    btn= QPushButton('click')
    btn.clicked.connect(get_content)
    
    btn.show()
    sys.exit(app.exec_()) 

