import requests
url = 'http://cd.58.com/chuzu/?key=%E7%A7%9F%E6%88%BF&cmcskey=%E7%A7%9F%E6%88%BF&final=1&jump=1&specialtype=gls'
url = 'http://cd.58.com/xiaoqu/meizhouhuayuanzongluwan/chuzu/'
rt = requests.get(url)
print(rt)
