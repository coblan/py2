#! -*- encoding:utf8 -*-
import requests

corpID= 'wxdf69422291cbc41e'
secret = 'sfNvVpGYh0KkAka1YWHZplnV5W5NPAufqD9e-x5PAnH3XGZ-Kx5DiOTAFhnj-HK0'
agentID = '3'

def main():
    crt_token = 'nYT48BZvZb_CpO7nwA23GhiurkH-kAreyL3jZIZujg-Aw_LHFX7ALg-HtxUxEc1lk9oEzrL_8i4H3v9PyO0pcQ'
    #access_token()
    # 发送文件到服务器
    #send_media(crt_token,'image',r'D:\try\imgproc\test1.jpg')

    # 上传news文件
    #send_txt_media(crt_token)
    #send_group(crt_token)

    #add_menu(crt_token)

    #test_local()

    #send(crt_token)
    #test_post_msg()
    #get_qiye_user(crt_token,'ec9925fed0a5bbe3fe852731e98e50e4')
    #fork_get_user()
    get_img_ls(crt_token)

def access_token():
    '''获取accses_token,

    '''
    rq = requests.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid='+corpID+'&corpsecret='+secret)
    print(rq.text) 

def send_media(token,type_,file_):
    """type_:类型 
       file_:媒体文件"""
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
    url = r'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='+token
    #post数据格式
    data= """
    {
        "touser": "o6hHBv1AfKq8rH5LAY6AY_gHbQrc", 
        "text": {
            "content": "HELLO"
        }, 
        "msgtype": "text"
    }
    """
    rq = requests.post(url,data)
    print(rq.text)

def send_img(token):
    url = r'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='+token
    #post数据格式
    data= """
    {
        "touser": "o6hHBv1AfKq8rH5LAY6AY_gHbQrc", 
        "image": {
              "media_id": "$MEDIA_ID"
              }, 
        "msgtype": "image"
    }
    """
    rq = requests.post(url,data)
    print(rq.text)
    

def add_menu(token):
    '添加菜单'
    url = r"https://qyapi.weixin.qq.com/cgi-bin/menu/create?access_token="+token+"&agentid="+agentID
    data ="""
    {
         "button":[
         {	
              "type":"view",
              "name":"JS-JDK",
              "url":"http://coblan.sinaapp.com/jdk/"
          },
          {
               "name":"菜单",
               "sub_button":[
               
               {	
                   "type":"view",
                   "name":"测试跳转页1",
                   "url":"http://coblan.sinaapp.com/static/APP/pages/index.html"
                },
                { 
                   "type":"view",
                   "name":"获取用户code1",
                   "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxdf69422291cbc41e&redirect_uri=\
                   http%3a%2f%2fcoblan.sinaapp.com%2fgetuser%2f&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
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
    data ="""<xml><ToUserName><![CDATA[gh_7b76db9b0422]]></ToUserName>
<FromUserName><![CDATA[o6hHBv1AfKq8rH5LAY6AY_gHbQrc]]></FromUserName>
<CreateTime>1446453151</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[CLICK]]></Event>
<EventKey><![CDATA[V1001_GOOD]]></EventKey>
</xml>
    """
    headers = {'content-type': 'text/xml'}
    rq= requests.post("http://127.0.0.1:8000/wei/", data=data, headers=headers)
    print(rq.text)

def test_post_msg():
    headers ={#'QUERY_STRING': r'msg_signature=998eab19ff2a5af4350554adb8e67d8e0bdd80d8&timestamp=1446615507&nonce=760585220',
              #'QUERY_STRING':'dddd',
              'content-type': 'text/xml'}
    data ="""
    <xml><ToUserName><![CDATA[wxdf69422291cbc41e]]></ToUserName>
<Encrypt><![CDATA[PUSVPdfsUV0Mr1OYFt7nXzYm4rSCUIVMfb1SO9/qNmmWK6Mlm18X8caVS4C1wOsFS6eVxYHm/D7OawgaX4z//JGGv9skpwnlnmklNIA5mGihDJPc8Bq5FUq6fImDTGw4bmW9TTIODAD8KxMZAL7tuyX7ISCYPjhcq8cW0gVC5ev2aM7hTOOzui5uwfIQKPRAe1JaV8TkSwtFlAA33VeaGxsaHB5EIlvO8TnS5kmaJcdP5Yl19LB6AvGfq9J3uhy5nBKs9vcB2nKvuSVhQJI3If/GzYGayFTpzu55dp3s7WgfXKNxPLr0PlhCuH6D66b/JYHnwbAnYM1Xo1B3WtRa/GDQy/9ARqrpoX7Fo4i6au0rmL+Ym/5QqfWlZhCjYD8FGqPl3yaLTInXhOIo+2aGGCMIbBZamUJOgO1xdZVkigg=]]></Encrypt>
<AgentID><![CDATA[3]]></AgentID>
</xml>
       """
    dataURL= "http://127.0.0.1:8000/mokie/?msg_signature=998eab19ff2a5af4350554adb8e67d8e0bdd80d8&timestamp=1446615507&nonce=760585220"
    
    ZHAN= """
    <xml><ToUserName><![CDATA[wxdf69422291cbc41e]]></ToUserName>
<Encrypt><![CDATA[Kpu/hbvVJD+Y8pOB9xtIm7hfNBLezKbiTGitf06aiOx+CObgiacsJKN9KdYh0TmudCDBR+EyuBgp4Plbve02qJpTJXCOL51S1EWDBaZNyOaj5CncFOppV2ZjOIy8dmGN2TTdH0TvtvGKzdJ7F0WvE0tpoHRo0gXk5DuH5r5hKs4SSApKyeIjMpV2f4mvD+29W/d+8E5fqlZYxRJNUneXI2hDJ3JYHDXSMjXsmM/or1ZVclYQq19ie082xQ3wT16qyntgevM18NFrpqbAeLEtJUZgXUkoBGPSWBumGQzQlM6rK8dg+PJ1Dfz2mYW2b8HFkTXOt8WAxlTumw9qXwe/YMTs0sJOqSDSHQ/aQVnFBO6JYXIhHFuT6Vxq46xZGnSit2ZGs0WIoxABViBdH2J/1adZxofszdpMBoNinqqhPTNdEiYk4AAgU62RpCv+JnZi2sTJXAzWdINunt9B+H/wAw==]]></Encrypt>
<AgentID><![CDATA[3]]></AgentID>
</xml>"""
    ZHANURL='http://127.0.0.1:8000/mokie/?msg_signature=a7cbf401bac7401fe95a88efdd058715f74b1ca6&timestamp=1446627240&nonce=1677872891'
    rq= requests.post(ZHANURL, data=ZHAN, headers=headers)
    print(rq.text)    
        
def get_qiye_user(token,code):
    url= 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token='+token+'&code='+code
    rq = requests.get(url)
    print(rq.text)

def fork_get_user():
    url = 'http://127.0.0.1:8000/getuser/?code=c66bb67c858a51464a67c342df24d7eb'
    rq = requests.get(url)
    print(rq.text)

def get_img_ls(token):
    url = r'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token='+token
    data = {
    "type":'image',
    "offset":0,
    "count":20
    }
    rq = requests.post(url,data=data)
    print(rq.text)
    
if __name__ =='__main__':
    main()
    

