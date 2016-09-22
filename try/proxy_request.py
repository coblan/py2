import requests
proxies = {
    'http': 'http://127.0.0.1:8087',
    'https': 'http://127.0.0.1:8087',
}
rt = requests.get('https://www.google.com.hk/?gws_rd=cr#newwindow=1&safe=strict&q=%E6%9C%88%E7%A7%91%E6%8A%80&btnK=Google+%E6%90%9C%E7%B4%A2',\
                  proxies=proxies,verify=False)
with open('d:/try/hh.html','w') as f:
    f.write(rt.content)
