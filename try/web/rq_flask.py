import requests
import json


#s = requests.Session()
#s.verify = '/path/to/certfile'

rt = requests.get('https://localhost:8100/',verify=r'D:\cygwin64\home\coblan\myca\server.crt')
print(rt.text)