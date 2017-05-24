import requests

header={
    'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)',  
    'Referer':'https://wx2.qq.com'
}
url = 'https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxgeticon?seq=670441231&username=@5ed5930eac4aef94c19d06feac454d7f&skey=@crypt_8105ceef_48da5e30b6fc629cb4bdd0154ed66322'
resp = requests.get(url,headers=header)
print(resp.content)

