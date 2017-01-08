import requests
url = 'http://imagedb.stm.com/userupload'
# url = 'http://localhost:8000/userupload'
# files = {'userfile': open(r'D:\try\image\full\2a6eba0af9d5035323fd5224ede875d9bde8a4ae.jpg', 'rb')}
files = {'userfile': open(r'D:\try\image\koala3.jpg', 'rb')}


r = requests.post(url, files=files)
print(r.text)