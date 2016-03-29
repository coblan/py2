# -*- encoding:utf8 -*-

import sys
import json
import time
#from django.conf import settings
import requests
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import auth
import urllib
from models import UserInfo

"""
AutoRegistBackEnd 是登陆的后台函数。
1.setting.py 里面设置变量
AUTHENTICATION_BACKENDS= ['django.contrib.auth.backends.ModelBackend',
                          'AutoRegistBackEnd']

这样设置后，调用 auth.authenticate(**kw)时，会触发该后台的authenticate函数，并返回user
然后再利用login(user)登陆该user，

2. 在model中建立一个staffInfo的model，来保存wx_id与user的对应关系

3.使用 Weixin.login 装饰需要登陆的views函数

注意：
Weixin的子类 Dingyue,Fuwu,Qiye 等才是具体的业务类。
"""




class Weixin(object):
    """
    """
    def __init__(self,appid,secret):
        self.appid=appid
        self.secret=secret
        self.access_token=None
        self.token_time=0
        
    def get_access_token(self):
        """获取token，如果没过期(1个小时)，就从缓存里面取，否则从服务器取。
        注意：
            尽管可能在分布式服务器上，全局变量不同，但是这里不要求sys.weixin同步，所以这里应该是没有问题的。
        """
        now = int(time.time())
        delta=now -self.token_time
        if not self.access_token or delta>3600:
            self.access_token = self.token_from_sever()
            self.token_time=now
        return self.access_token
     
        
    def token_from_sever(self):
        return None
    
    def get_code_url(self,redirect_url):
        redirect_url='http://'+redirect_url
        redirect_url=urllib.quote(redirect_url,safe='')
        url='https://open.weixin.qq.com/connect/oauth2/authorize?appid='+self.appid+'&redirect_uri='+\
            redirect_url+'&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect' 
        return url  
    
    def userid_from_code(self,code):
        """
        这个是服务号的
        """
        token=self.get_access_token()
        url='https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token='+token+'&code='+code
        rt=requests.get(url)
        dc=json.loads(rt.text)
        try:
            return dc['UserId']
        except KeyError as e:
            raise UserWarning,'not get userID from server ,server respons is :%s'%rt.text  
        
    def login(self,func):
        """decerator
        生成：request.session['wx_userid']
        """
        def _func(request,*args,**kw):
            if not request.user.is_authenticated():
                code = request.GET.get('code')
                if code:
                    self.proc_code(request,code)    
                    
                userid=request.session.get('wx_userid')
                if userid:
                    self.login_userid(request, userid)
                else:
                    return redirect(self.code_api(request))
            
            return func(request,*args,**kw)
        return _func
    
    def code_api(self,request):
        abspath = request.META.get('HTTP_HOST')+request.path
        url = self.get_code_url(abspath)
        return url

    def proc_code(self,request,code):
        userid =self.userid_from_code(code)
        request.session['wx_userid']=userid 
    
    def login_userid(self,request,userid):
        user= auth.authenticate(wx_userid=userid)
        auth.login(request,user)
        return user 



class Dingyue(Weixin):
    def token_from_sever(self):
        """从服务器取token
        """
        rq=requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+self.appid+'&secret='+self.secret)
        #rq = requests.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid='+self.appid+'&corpsecret='+self.secret)
        dc=json.loads(rq.text)
        access_token = dc.get("access_token")
        if access_token:
            return access_token
        else:
            raise UserWarning,'not get access_token form server ,in function Dingyue.token_from_sever(); rq = %s'%rq.text
        
    def userid_from_code(self,code):
        url='https://api.weixin.qq.com/sns/oauth2/access_token?appid='+self.appid+'&secret='+self.secret+\
            '&code='+code+'&grant_type=authorization_code'
        rt=requests.get(url)
        dc=json.loads(rt.text)
        try:
            return dc['openid']
        except KeyError as e:
            raise UserWarning,'not get userID from server ,server respons is :%s'%rt.text     



class AutoRegistBackend(object):
    def authenticate(self, wx_userid):
        if wx_userid:
            info,created =UserInfo.objects.get_or_create(wx_id=wx_userid)
            if created:
                user= User.objects.create(username=wx_userid+str(time.time()))
                info.owner=user
                info.save()
                return user
            else:
                return info.owner

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None   


def get_code_from_server():
    url='https://open.weixin.qq.com/connect/oauth2/authorize?appid='+appid+'&redirect_uri=\
        http%3a%2f%2fwechat.mokitech.com/attandanc/recieve_code%2f&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect' 

def embed_url(url):
    return 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+appid+'&redirect_uri='+url\
        +'&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'
    

def userid_from_code(code):
    token=get_access_token()
    if not token:
        return 'token is none'
    url='https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token='+token+'&code='+code
    rt=requests.get(url)
    dc=json.loads(rt.text)
    return dc.get('UserId')

# def recieve_code(request):
    # """测试用的，测试微信auth2.0,将连接嵌入第三方，是否能够获取用户信息。
    # """
    # code = request.GET.get('code')
    # if code:
        # openid = get_openid(code)
        # if not openid:
            # return HttpResponse('not openid')
        # else:
            # items = get_user_with_openids([openid,])
            # if not items:
                # return HttpResponse('not items')
            # else:
                # item= items[0]
                # return HttpResponse("<div>nickname:%s,,,<img src='%s'></div>"%(item.get('nickname'),item.get('headimgurl')))   
    # else:
        # return HttpResponse('not code')
    

def _token_from_sever():
    
    """从服务器取token
    """
   
    rq = requests.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid='+appid+'&corpsecret='+secret)
    dc=json.loads(rq.text)
    access_token = dc.get("access_token")
    token_time=int(time.time())
    sys.weixin['access_token']=access_token
    sys.weixin['token_time']=token_time  
    return access_token


def send_text(userid,content):
    """
    微信中发送【文字】消息
    
    @type userid:str ,员工号，如AE1856
    @type content:str ,发送的内容
    """
    token=get_access_token()
    url='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+token
    data={
        "touser": "%s"%userid,
        # "toparty": " PartyID1 | PartyID2 ",
        # "totag": " TagID1 | TagID2 ",
        "msgtype": "text",
        "agentid": "3",
        "text": {
            "content": content.decode('utf8')
            },
        "safe":"0",
    }  
    data=json.dumps(data,ensure_ascii=False)
    rt = requests.post(url,data=data.encode('utf8'))
    return json.loads(rt.text)
    
def weixin_view(request):
    """现在没用
    """
    if request.method == 'GET':
        s1 = request.GET.get('echostr','')
        if s1:
            return  HttpResponse(s1)
        else:    # 管理抢答界面
            return HttpResponse('weixin get ok')
    elif request.method == 'POST':
        if request.META.get('CONTENT_TYPE','').lower().strip() == 'text/xml':
            come_str = request.body 
            handle = paser(come_str)
            if handle.msgType=='text':
                #can_qd= state.can_qd #mystate.get_qd_state()
                if  gd.can_qd :
                    openid= handle.fromUserName
                    msg = get_or_none(QiangDaModel,openid=openid)
                    # msg =None
                    if msg:
                        content = '每个问题只能抢答一次'
                    else:
                        try:
                            content ='回答成功!' 
                            now=timezone.localtime(timezone.now()).time().strftime('%H:%M:%S')
                            user= get_or_none(UserModel,openid=openid)
                            if user:
                                nickname,headimg = user.nickname(),user.img()
                            else:
                                nickname,headimg = '',''
                            
                           # //--memecatched
                            # index = gd.incr('q_cnt')
                            # def func(ls):
                                # ls.append({'id':index, #gd.q_cnt,
                                        # 'openid':openid,
                                        # 'content':handle.content,
                                        # 'time':now,
                                        # 'nickname':nickname,
                                        # 'head':headimg})
                                # return ls
                            # gd.sync('qiangda_msgs',func)
                            
                            # cont = base64.b64encode(handle.content)
                            # nick = base64.b64encode(nickname.encode('utf8'))
                            # QiangDaModel(openid=openid,content=cont,time=now,submited='false',nickname=nick,head=headimg).save()
                            
                            cont = base64.b64encode(handle.content)
                            # cont=handle.content
                            nick = nickname.encode('utf8')
                            QiangDaModel(openid=openid,content=cont,time=now,submited='false',nickname=nick,head=headimg).save()                        
                            # gd.has_qd_msg=True     # 标记有数据，减少读取数据库次数
                        except Exception as e:
                            ExceptionModel(place='weixin',detail=str(e)).save()
                else:
                    content ='抢答还没有开始'
                    
                text_msg= """
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
                """%(handle.fromUserName, handle.toUserName,int(time.time()),content)  
                return HttpResponse(text_msg, content_type='text/html; charset=utf-8')
        return HttpResponse('success')