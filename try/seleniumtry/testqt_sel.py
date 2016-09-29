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
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException

import os
import sys
base_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(base_dir,'db'))

from interface import save_model
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
        
        pub_lukou()
        
        #code = self.plain.toPlainText()
        ##do(code)
        #try:
            #exec(code)
        #except Exception as e:
            #print(e)
      
    
    def save_cookies(self):
        cookies = driver.get_cookies()
        with open(u'd:/try/cook','wb') as f:
            pickle.dump(cookies,f)
    
    def add_cookies(self):
        driver.delete_all_cookies()
        
        with open(u'd:/try/cook','rb') as f:
            cookies = pickle.load(f)
            for c in cookies:
                driver.add_cookie(c)

from interface import TuiModel
def pub_lukou():
    cnt = 0
    for row in TuiModel.objects.all():
        try:
            if row.lukou =='no':
                kw=row.url
                #visible('.publish.option')
                wait(1)
                hover(sel('.publish.option')[0])
                click(sel('li [href="/post/commodity"]')[0])
                visible('div.link .cmd-link')
                js('$("div.link .cmd-link").val("%s")'%kw)
                click(sel('#fetchCommodity')[0])
                or_visible('button.active.publish','.err-txt')
                if sel('.err-txt[style="display: block;"]'):
                    row.lukou='error_url'
                    row.save()
                else:
                    click(sel('button.active.publish')[0]) 
                    row.lukou = 'yes'
                    row.save()
                #if cnt >10:
                        #break
        except UnexpectedAlertPresentException as e:
            print(repr(e))
            time.sleep(1)
            continue
        

def do(kw):
    click(sel('#q')[0])
    sel('#q')[0].clear()
    input(sel('#q')[0],kw)
    sel('[mx-click="searchChannel()"]')[0].click()
    wait(3)
    sel('[mx-click="itemSort(1)"]')[0].click()
    wait(1)
    visible('.tag-wrap .box-btn-group a')
    for ele in sel('.tag-wrap')[0:3]:
        t_e = ele.find_element_by_css_selector('.content-title')
        title = attr(t_e,'title')
    
        ljtg = ele.find_element_by_css_selector('.box-btn-group a')
        click(ljtg)
        wait(1)
        visible('.dialog-ft [mx-click="submit"]')
        click(sel('.dialog-ft [mx-click="submit"]')[0])
        wait(1)
        visible('#clipboard-target')
        url= attr(sel('#clipboard-target')[0],'value') 
        click(sel('[mx-click="close"]')[0])
    
        img = attr(ele.find_element_by_css_selector('.search-box-img img'),'src')
        price = ele.find_element_by_css_selector('.color-d.number-16 .integer').text
        dc = {'title':title,'url':url,'img':img,'price':price,'tag':kw}
        print(dc)
        save_model(dc)    


def js(script):
    driver.execute_script(script)

def hover(ele):
    builder = ActionChains(driver)
    builder.move_to_element(ele).perform()

def select(ele,value):
    select = Select(ele)
    #select.select_by_index(index)
    #select.select_by_visible_text("text")
    select.select_by_value(value)    

def visible(selector):
    element = WebDriverWait(driver, 20).until(
        #EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
        
    )    

def or_visible(sel1,sel2):
    def fun1(self):
        first = EC.visibility_of_element_located((By.CSS_SELECTOR, sel1))(self)
        second = EC.visibility_of_element_located((By.CSS_SELECTOR, sel2))(self)
        return  first if first else second
               
    element = WebDriverWait(driver, 20).until(
        fun1
    )     


def my_run():
    sel('#q')[0].clear()
    input(sel('#q')[0],u'手机')
    sel('[mx-click="searchChannel()"]')[0].click()
    wait(3)
    sel('[mx-click="itemSort(1)"]')[0].click()
    wait(1)
    click( sel('.tag-wrap .box-btn-group a')[0]) #.click()
    wait(1)
    click(sel('.dialog-ft button')[0]) #.click()
    wait(1)    

def mk_visible(ele):
    driver.execute_script("window.scrollTo({x}, {y})".format(**ele.location)) 
    
def click(ele):
    driver.execute_script("window.scrollTo({x}, {y})".format(**ele.location)) 
    ele.click()


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
    win = Win()
    win.show() 
    
    driver = webdriver.Chrome()
    driver.get('http://www.lukou.com')
 
    #driver.get(r'http://pub.alimama.com/promo/item/channel/index.htm?spm=a219t.7900221.1998910419.39.efad5W&channel=qqhd')
    #driver.delete_all_cookies()
    with open(u'd:/try/cook','rb') as f:
        cookies = pickle.load(f)
        for c in cookies:
            driver.add_cookie(c)   
    
    
    #ls=[]
    #for i in range(3):
        #ls.append( webdriver.Chrome())
    
    #for driver in ls:
        #driver.get("http://www.baidu.com") 
    
    
    # go to the google home page
    #driver.get("http://www.baidu.com")    
    
      
    
    #btn= QPushButton('click')
    #btn.clicked.connect(get_content)
    
    #btn.show()
    sys.exit(app.exec_()) 

