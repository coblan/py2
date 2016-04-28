import requests
url='http://127.0.0.1:8000/lintool/hook_info/'
url2='http://linggo.sinaapp.com/lintool/hook_info/'
payload = {'key1': 'value1', 'key2': 'value2'}
rt=requests.post(url2,data=payload)
print(rt.text)