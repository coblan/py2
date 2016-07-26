# -*- encoding:utf8 -*-
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()
#driver = webdriver.Chrome()

# go to the google home page
driver.get("http://www.baidu.com")

# the page is ajaxy so the title is originally this:
print driver.title
inputElement = driver.find_element_by_id("kw")
inputElement.send_keys(u"月科技")
inputElement.submit()

with open(u'd:/try/baidu','wb') as f:
    f.write(driver.page_source.encode('utf8'))
with open(u'd:/try/baidu_cookie','wb') as f:
    json.dump(driver.get_cookies(),f)



