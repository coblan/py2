# -*- encoding:utf8 -*-
import requests

url = 'http://127.0.0.1:8000/try/file/'
files = {'file': open(r'C:\Users\zhangrong\Desktop\2015-11-07\mytest.txt', 'rb')}
#files = {'file': ('report.jpg', open('/home/lyb/sjzl.mpg', 'rb'))}     #显式的设置文件名

r = requests.post(url, files=files)
print(r.text)