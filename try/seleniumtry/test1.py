# -*- encoding:utf8 -*-
import time

import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Create a new instance of the Firefox driver
# driver = webdriver.Firefox()
driver = webdriver.Chrome()

# go to the google home page
driver.get("http://www.google.com")

# the page is ajaxy so the title is originally this:
print driver.title
inputElement = driver.find_element_by_id("lst-ib")
inputElement.send_keys(u"月科技")
inputElement.submit()
time.sleep(3)
out = []
for ele in driver.find_elements_by_css_selector('h3 a'):
    out.append( ele.get_attribute('href'))
for ele in driver.find_elements_by_css_selector('#navcnt a'):
    out.append(ele.get_attribute('href'))
    # print(ele.get_attribute('href'))
# with open(u'd:/try/baidu','wb') as f:
    # f.write(driver.page_source.encode('utf8'))
# with open(u'd:/try/baidu_cookie','wb') as f:
    # json.dump(driver.get_cookies(),f)

with open(u'd:/try/google.html','wb') as f:
    json.dump(out,f)

