import sys
import time
import pickle
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4.QtGui import QApplication,QPushButton,QWidget,QPlainTextEdit,QVBoxLayout

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
#from PyQt4.QtCore import QUrl
#from PyQt4.QtWebKit import QWebView,QWebSettings


#def get_content():
    #print('here')
    #print driver.title 

class Win(QWidget):
    def __init__(self, parent=None, flags=0):
        super(Win,self).__init__()
        self.btn = QPushButton('run',self)
        self.save_btn = QPushButton('save cookies',self)
        self.add_btn = QPushButton('add cookies', self)
        self.plain=QPlainTextEdit(self)
        lay = QVBoxLayout(self)
        lay.addWidget(self.btn)
        lay.addWidget(self.save_btn)
        lay.addWidget(self.add_btn)
        lay.addWidget(self.plain)
        
        self.btn.clicked.connect(self.run)
        self.save_btn.clicked.connect(self.save_cookies)
        self.add_btn.clicked.connect(self.add_cookies)
    
    def run(self):
        print('here')
        
        code = self.plain.toPlainText()
        try:
            exec(code)
        except Exception as e:
            print(e)
      
    
    def save_cookies(self):
        cookies = driver.get_cookies()
        with open(u'd:/try/cook','wb') as f:
            pickle.dump(cookies,f)
    
    def add_cookies(self):
        with open(u'd:/try/cook','rb') as f:
            cookies = pickle.load(f)
            for c in cookies:
                driver.add_cookie(c)



def click(ele):
    #webdriver.web
    driver.execute_script("window.scrollTo({x}, {y})".format(**ele.location)) 
    ele.click()
    #actions = ActionChains(driver)
    #actions.move_to_element(ele).click().perform()
    #actions.click(ele)
    #actions.perform()

def wait(second):
    time.sleep(second)
    #driver.implicitly_wait(second)
    #web
    #WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))
    
def input(ele,string):
    ele.send_keys(string)
    
def sel(css):
    return driver.find_elements_by_css_selector(css)

def attr(ele,name):
    return ele.get_attribute(name)

if __name__=='__main__':
    app = QApplication(sys.argv)
    
    driver = webdriver.Chrome()
    
    #ls=[]
    #for i in range(3):
        #ls.append( webdriver.Chrome())
    
    #for driver in ls:
        #driver.get("http://www.baidu.com") 
    
    
    # go to the google home page
    #driver.get("http://www.baidu.com")    
    
    win = Win()
    win.show()    
    
    #btn= QPushButton('click')
    #btn.clicked.connect(get_content)
    
    #btn.show()
    sys.exit(app.exec_()) 

