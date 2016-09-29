# -*- encoding:utf8 -*-

import sys
import json
import time

import requests
appid = 'wx7080c32bd10defb0'
secret = 'd4624c36b6795d1d99dcf0547af5443d'
sys.weixin={}

def get_access_token():
    """获取token，如果没过期(1个小时)，就从缓存里面取，否则从服务器取。
    注意：
        尽管可能在分布式服务器上，全局变量不同，但是这里不要求sys.weixin同步，所以这里应该是没有问题的。
    """
    access_token= sys.weixin.get('access_token')
    if not access_token:
        access_token = fetch_access_token()
    else:
        token_time =sys.weixin['token_time']
        now = int(time.time())
        if now -token_time >3600:
            access_token=fetch_access_token()
    return access_token


def get_userinfo_switch(code,userinfo,msg=[]):
    """当同一台手机切换账号时，就可能是cookies有userinfo信息，
    但是openid却不是原来的人了。
    ----TOdo 每次切换用户，或者退出登录，都会清空cookie，所以这个函数无用了。
    """
    access_token = get_access_token()
    open_dict = get_openid(code, msg)
    openid = open_dict.get('openid')
    openid_local = userinfo.get('openid')
    ACCESS_TOKEN=open_dict.get('access_token')
    if openid == openid_local:
        oldtime=int( userinfo.get('time') )
        now = int(time.time())
        if now-oldtime >3600*24*2:
            dc = get_userinfo(ACCESS_TOKEN, openid, msg)
            dc['time']=now
            msg.append('openid 的时间超过2天，更新')
            return dc
        else:
            msg.append('userinfo没过期，openid也没变，不需要更新')
            return userinfo
    else:
        msg.append('openid不同，肯定是切换用户了')
        dc = get_userinfo(ACCESS_TOKEN, openid, msg)
        dc['time']=int(time.time())
        return dc

def get_user_from_server(code,msg=[]):
    """从code到openid再到userinfo
    """
    msg.append('从code->openid->userinfo')
    dc = get_openid(code)
    msg.append(dc)
    ACCESS_TOKEN=dc.get('access_token')
    openid=dc.get('openid') 
    userinfo = get_userinfo(ACCESS_TOKEN, openid)
    msg.append(userinfo)
    userinfo['time'] = int(time.time())
    return userinfo

def get_openid(code):
    """返回：
    {
   "access_token":"ACCESS_TOKEN",
   "expires_in":7200,
   "refresh_token":"REFRESH_TOKEN",
   "openid":"OPENID",
   "scope":"SCOPE",
   "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
}
    """
    url='https://api.weixin.qq.com/sns/oauth2/access_token?appid='+appid+'&secret='+secret+'&code='+code+'&grant_type=authorization_code'
    rq = requests.get(url)
    dc = json.loads(rq.text)
    return dc.get('openid')

def get_userinfo(ACCESS_TOKEN,openid):
    """返回字典格式为：
    {
   "openid":" OPENID",
   " nickname": NICKNAME,
   "sex":"1",
   "province":"PROVINCE"
   "city":"CITY",
   "country":"COUNTRY",
    "headimgurl":    "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/46", 
	"privilege":[
	"PRIVILEGE1"
	"PRIVILEGE2"
    ],
    "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
}
更具体的见微信帮助：http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html  的第四步
    """
    url='https://api.weixin.qq.com/sns/userinfo?access_token='+ACCESS_TOKEN+'&openid='+openid+'&lang=zh_CN'
    rq=requests.get(url)
    rq.encoding='utf8'
    dc=json.loads(rq.text)
    return dc
    
def fetch_access_token():
    """从服务器取token
    """
    rq = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appid+'&secret='+secret)
    dc=json.loads(rq.text)
    access_token = dc.get("access_token")
    token_time=int(time.time())
    sys.weixin['access_token']=access_token
    sys.weixin['token_time']=token_time  
    return access_token

def get_user_with_openids(openids):
    """向服务器查询不完整信息用户，并将其保存数据库
    """
    access_token= get_access_token()
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