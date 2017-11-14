# import requests
# url = 'http://imagedb.stm.com/userupload'
# # url = 'http://localhost:8000/userupload'
# # files = {'userfile': open(r'D:\try\image\full\2a6eba0af9d5035323fd5224ede875d9bde8a4ae.jpg', 'rb')}
# files = {'userfile': open(r'D:\try\image\koala3.jpg', 'rb')}


# r = requests.post(url, files=files)
# print(r.text)

import requests
url = 'http://suntabu.com/console.html'
datas = {'n': 'jwc',
         'p': 'jwc',
         }
headers = {'Referer': 'http://www.suntabu.com/console.html',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
           '(KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
                         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           }
sessions = requests.session()
response = sessions.post(url, headers=headers, data=datas)
print(response.status_code)