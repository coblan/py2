# -*- encoding:utf8 -*-

import re
class Goagent(object):
    """Custom ProxyMiddleware."""
    #def __init__(self, settings):
        #self.proxy_list = settings.get('PROXY_LIST')
        #with open(self.proxy_list) as f:
            #self.proxies = [ip.strip() for ip in f]

    def process_request(self, request, spider):
        url = request.url
        if re.match(r'^http(s)*://www.google.',url):
            request.meta['proxy'] ='http://127.0.0.1:8087'
        #request.meta['proxy'] = 'http://{}'.format(random.choice(self.proxies))
        
import os


user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "  
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",  
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "  
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",  
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "  
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",  
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "  
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",  
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "  
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",  
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "  
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",  
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "  
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",  
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",  
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "  
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",  
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "  
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"  
]  

class SaveAll(object):
    def process_request(self, request, spider):
        url = request.url
        print(url)
    
    def process_response(self, request, response, spider):
        url = response.url
        with open(os.path.join(r'd:/try/html',str(hash(url)))+'.html','wb') as f:
            f.write(response.body)   
        return response

from scrapy import log  

"""避免被ban策略之一：使用useragent池。 

使用注意：需在settings.py中进行相应的设置。 
"""  

import random  
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware  

class RotateUserAgentMiddleware(UserAgentMiddleware):  

    def __init__(self, user_agent=''):  
        self.user_agent = user_agent  

    def process_request(self, request, spider):  
        ua = random.choice(user_agent_list)  
        if ua:  
            #显示当前使用的useragent  
            print "********Current UserAgent:%s************" %ua  

            #记录  
            # log.msg('Current UserAgent: '+ua, level='INFO')  
            request.headers.setdefault('User-Agent', ua)  
   