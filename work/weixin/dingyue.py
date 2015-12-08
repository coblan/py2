# -*- encoding:utf8 -*-
import pickle
import time
import requests
import json
APPID='wx7080c32bd10defb0'
SECRET='d4624c36b6795d1d99dcf0547af5443d'
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

class AccessToken(object):
    APPID = APPID
    SECRET = SECRET
    def __init__(self,path='database'):
        try:
            self.read(path)
        except:
            self.update()
        
    def update(self):
        """从服务器取token
        """
        print('from server')
        rq = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+self.APPID+'&secret='+self.SECRET)
        dc=json.loads(rq.text)
        self.access_token = dc.get("access_token")
        self.time=int(time.time())  
        
    def save(self,path):
        with open(path,'wb') as f:
            pickle.dump((self.access_token,self.time),f)
        
    def read(self,path):
        with open(path,'rb') as f:
            self.access_token,self.time = pickle.load(f)
    
    def get(self):
        now = int(time.time())
        if now - self.time >3600:
            self.update()
        self.save('database')
        return self.access_token
        
def add_menu():
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+AccessToken().get()
    data="""{
     "button":[
      {
           "name":"菜单",
           "sub_button":[
           {	
               "type":"view",
               "name":"年会节目主界面测试1",
               "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7080c32bd10defb0&redirect_uri=http%3a%2f%2fcoblan.sinaapp.com%2fnianhui%2fjiemu%2f&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
            },
            ]
       }]
 }"""


    rq = requests.post(url,data=data)
    print(rq.text)

def get_user_with_openids(openids):
    """向服务器查询不完整信息用户，并将其保存数据库
    """
    access_token= AccessToken().get()
    url= 'https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token='+access_token
    dc = {"user_list":[]}
    for openid in openids:
        dc['user_list'].append({
            "openid":openid,
            'lang':'zh-CN'
        })
    
    data = json.dumps(dc)
    rq = requests.post(url,data=data)
    rq.encoding='utf8'
    dc= json.loads(rq.text)
    items = dc.get( "user_info_list")   
    return items

if __name__=='__main__':
    #print(AccessToken().get())
    add_menu()
    # openids=['o6hHBv6HoSpoA8RphJ1sP7zgOlIk','o6hHBv1AfKq8rH5LAY6AY_gHbQrc','sdfsgweggsd']
    # print( get_user_with_openids(openids) )
    