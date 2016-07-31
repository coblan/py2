from selenium import webdriver

class Engin(object):
    
    def drive_pool(self,number=5):
        self.pool=[]
        for i in range(5):
            self.pool.append(webdriver.Chrome())
            