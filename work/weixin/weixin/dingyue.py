#! -*- encoding:utf8 -*-
import requests

def main():
    crt_token = '920XNa9MArHcj6VIqGq-8yTNraig-Oj8iwlcEQLFLuq1BZ1Ex5igZRDTf_fxp4df8hchxXYYwXEqT7zVG8JL-T48Q-FBFp5PVi9mifJ5DjwNHPjACAJDL'
    # access_token()
    # 发送文件到服务器
    #send_media(crt_token,'image',r'D:\try\imgproc\test1.jpg')
    
    # 上传news文件
    #send_txt_media(crt_token)
    #send_group(crt_token)
    
    # add_menu(crt_token)
    
    # for i in range(50):
        # test_local()
    #抢答
    # test_local()
    
    send(crt_token)


def access_token():
    '''获取accses_token,
    appid=wx7080c32bd10defb0&secret=d4624c36b6795d1d99dcf0547af5443d

    曾经获得的一个：
    "type":"image","media_id":"ZWx3LgGb3jRu79rGlnVKW9SDE-hRjCrBh5IJ91nCiX9VcYA4N-8FYfq24opF6A05"
    '''
    myappid='wx7080c32bd10defb'
    mysecret= 'd4624c36b6795d1d99dcf0547af5443d'
    mokiappid='wx4caa217911a92dbd'
    mokisecret='257666d2ee35c47df38f4f6dd759813e'
    appid = mokiappid
    secret=mokisecret
    #moki
    # appid = 'wx4caa217911a92dbd'
    # secret = '257666d2ee35c47df38f4f6dd759813e'
    rq = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appid+'&secret='+secret)
    print(rq.text) 
    
def send_media(token,type_,file_):
    url = r'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s'%(token,type_)
    media ={'media':open(file_,'rb')}
    rq = requests.post(url, files= media)
    print(rq.text)


def send_txt_media(token):
    """在群发里面找到的方法：
    曾经成功的一个：
    {"type":"news","media_id":"jwKykANlGxl2ueVfCFu1STTSaa9_W4YMKZNGJnzydUUNZAwep7wGfFvVfmGT9znO","created_at":1446436254}
    """
    url = r'https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token=%s'%token
    data="""
    {
   "articles": [
		 {
                        "thumb_media_id":"ZWx3LgGb3jRu79rGlnVKW9SDE-hRjCrBh5IJ91nCiX9VcYA4N-8FYfq24opF6A05",
                        "author":"xxx",
			 "title":"Happy Day",
			 "content_source_url":"www.qq.com",
			 "content":"content",
			 "digest":"digest",
                        "show_cover_pic":"1"
		 },
		 {
                        "thumb_media_id":"ZWx3LgGb3jRu79rGlnVKW9SDE-hRjCrBh5IJ91nCiX9VcYA4N-8FYfq24opF6A05",
                        "author":"xxx",
			 "title":"Happy222 Day",
			 "content_source_url":"www.qq.com",
			 "content":"content",
			 "digest":"digest",
                        "show_cover_pic":"0"
		 }
   ]
}
"""
    rq = requests.post(url,data=data)
    print(rq.text)


def send_group(token):
    url = r'https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token=%s'%token
    news="""
    {
   "filter":{
      "is_to_all":true
   },
   "mpnews":{
      "media_id":"jwKykANlGxl2ueVfCFu1STTSaa9_W4YMKZNGJnzydUUNZAwep7wGfFvVfmGT9znO"
   },
    "msgtype":"mpnews"
}"""
    text_msg = """
    {
   "filter":{
      "is_to_all":true
   },
   "text":{
      "content":"CONTENT"
   },
    "msgtype":"text"
}"""

    rq = requests.post(url, data=news)
    print(rq.text)


def send(token):
    #"content": "点击我(https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7080c32bd10defb0&redirect_uri=http%3a%2f%2fcoblan.sinaapp.com%2fnianhui%2fgetuser%2f&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect)"
    url = r'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='+token
    #post数据格式
    data= """
    {
        "touser": "olEWajpji6FqC5twaXFV7S929AnQ", 
        "text": {
            "content": "点击我(https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx4caa217911a92dbd&redirect_uri=http%3a%2f%2fwechat.mokitech.com%2fnianhui%2fjiemu%2f&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect)"
        }, 
        "msgtype": "text"
    }
    """
    rq = requests.post(url,data)
    print(rq.text)
    

def add_menu(token):
    '添加菜单'
    url = r"https://api.weixin.qq.com/cgi-bin/menu/create?access_token="+token
    data ="""
    {
         "button":[
         {	
              "type":"view",
              "name":"moki",
              "url":"http://coblan.sinaapp.com/jdk/"
          },
          {
               "name":"菜单",
               "sub_button":[
               {	
                   "type":"view",
                   "name":"测试网页跳转n",
                   "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7080c32bd10defb0&redirect_uri=http%3a%2f%2fcoblan.sinaapp.com%2fnianhui%2f&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
                },
               {	
                   "type":"view",
                   "name":"测试H",
                   "url":"http://coblan.sinaapp.com/hello/"
                },
                {
                   "type":"view",
                   "name":"请假",
                   "url":"http://coblan.sinaapp.com/journey/"
                },
                {
                   "type":"click",
                   "name":"赞一下我们",
                   "key":"V1001_GOOD"
                }]
           }]
     }
    """
    rq = requests.post(url, data=data)
    print(rq.text)


def test_local():
    '测试本地服务器的post XML的功能'
    # data ="""<xml><ToUserName><![CDATA[gh_7b76db9b0422]]></ToUserName>
# <FromUserName><![CDATA[o6hHBv1AfKq8rH5LAY6AY_gHbQrc]]></FromUserName>
# <CreateTime>1446453151</CreateTime>
# <MsgType><![CDATA[event]]></MsgType>
# <Event><![CDATA[CLICK]]></Event>
# <EventKey><![CDATA[V1001_GOOD]]></EventKey>
# </xml>
    # """
    # moki某人:olEWajiSzMCHUkqNue5zMg43gvKM
    data ="""<xml><ToUserName><![CDATA[gh_7b76db9b0422]]></ToUserName>
<FromUserName><![CDATA[olEWajiSzMCHUkqNue5zMg43gvKM]]></FromUserName>
<CreateTime>1446453151</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[这里是内容]]></Content>
</xml>
    """    
    headers = {'content-type': 'text/xml'}
    local="http://127.0.0.1:8000/nianhui/weixin/"
    web = "http://coblan.sinaapp.com/nianhui/weixin/"
    rq= requests.post(local, data=data, headers=headers)
    print(rq.text)


def test_get_user():
    from wxcom import get_openid
    print(get_openid('031de0724b2d7b880277cfc494cd2dec'))

def test_mokiUrl():
    url = 'http://216.12.198.102:8181/nianhui/weixin/'
    dc = {'echostr':'i m echostr'}
    rq = requests.get(url,params=dc)
    print(rq.text)

if __name__ =='__main__':
    main()
    # test_mokiUrl()
    # test_get_user()

