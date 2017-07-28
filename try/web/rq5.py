import requests
import os
url = 'http://localhost:8000/upload?node=node1'
os.chdir(r'D:\try')

files = {'file': open('data.tar.gz', 'rb')}

r = requests.post(url, files=files)
print(r.content)