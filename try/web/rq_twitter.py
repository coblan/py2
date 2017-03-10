from __future__ import unicode_literals
import requests
import json
import time
import urllib

from hashlib import sha1
import hmac
import base64

YOU_Access_Token_Secret='3jMLmhzyuSL9wt2YvT19LMGdtM4Oyi5GtHqt8r1qIL9JA'

def hmac_sha1(key,msg):
    my_sign = hmac.new(key, msg, sha1).digest()
    my_sign = base64.b64encode(my_sign)
    return my_sign

# url='https://api.twitter.com/oauth2/token'
url = 'https://api.twitter.com/oauth/request_token'
stamp= str(int(time.time()))
data={
   'oauth_consumer_key':'rkGfOADVkeOUxiylvU5CpBVU1',
   'oauth_signature_method':'HMAC-SHA1',
   # 'oauth_signature':'',
   'oauth_timestamp':stamp,
   'oauth_nonce':'bbaimajkuihFabxSWbWovY3uYSQ2pTgmZeNuBBBAAA',
   'oauth_callback': urllib.quote('http://moki-local.enjoyst.com',safe='~()*!.\'')
}
param_str = urllib.quote('&'.join( ['='.join(kv) for kv in sorted(data.items(),key=lambda x:x[0]) ]))

base_str='POST&'+urllib.quote(url,safe='~()*!.\'')+'&'+param_str
base_str=base_str
# %YOU_Access_Token_Secret
data['oauth_signature']=hmac_sha1(key='Tttwjj4X2JNCk6sPOQIPjyndMczObFbyQC6OsgcfwLhz2Eug21',msg=base_str)
# data ='mobile=17138080650&vcode=4566&nosign=1'
# data='car_no=%E4%BA%ACW34567&nick=%E8%8B%B1%E9%9B%84%E4%B8%8A%E5%BA%A7&car_brand=&car_model=&passwd=e10adc3949ba59abbe56e057f20f883e&nosign=1'

# url = 'http://localhost:8000/user/updateuserhead'
# data = 'uid=2&usersession=18&head=http%3A%2F%2Fwx.qlogo.cn%2Fmmopen%2FQ3auHgzwzM5ib2aEwMZu68rRlbWEr4j3FciaQyb8WTdX9PK4iaruybtzO8zc7xjTXnUueIp6rwka5opqPXibjYwOZg%2F0&nosign=1'

rt = requests.post(url,data=data)
print(rt.text)