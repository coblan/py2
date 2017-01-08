import requests

rt = requests.get('http://s.click.taobao.com/zjPPWVx')
with open(r'd:/try/jjj.html','wb') as f:
    f.write(rt.content)