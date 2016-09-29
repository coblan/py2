import requests
import json
from bs4 import BeautifulSoup
rq= requests.get('http://blog.wpjam.com/m/weixin-emotions/')

soup = BeautifulSoup(rq.text)
mp = {}
for tr in soup.select('tr'):
    try:
        # if tr.select('td')[1].text=="/::Z": #u"/::’(":
            # print(tr.select('img')[0]['src'])
        k=tr.select('td')[1].text.encode('utf8')
        v=tr.select('img')[0]['src'].encode('utf8')
        mp[k]=v
    except Exception as e:
        print(e)

# for k ,v in mp.items():
    # print(k,v)
with open ('weixinbiaoqin','wb') as f:
    json.dump(mp,f,ensure_ascii=False,indent=4)