from selenium import webdriver

#browser = webdriver.Chrome()
browser = webdriver.Firefox()
browser.get('http://www.google.com/')

print(browser.get_cookies())
input('ss')