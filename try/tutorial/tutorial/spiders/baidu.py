# -*- encoding:utf-8 -*-

import scrapy

from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import LinkItem,EmailItem,HtmlBody
from bs4 import BeautifulSoup
# import wingdbstub

urls = []
with open(u'd:/try/baidu.html','r') as f:
    soup= BeautifulSoup( f.read() )
    #for a in soup.select('tr a'):
            #urls.append("https://www.baidu.com"+ a['href'] )    
    for a in soup.select('h3 a'):
        urls.append( a['href'] )
    for a in soup.select('#page a'):
        urls.append( "https://www.baidu.com"+a['href'] )

class GpSearch(CrawlSpider):
    name='baidu'
    
    # allowed_domains =['mokitech.com']
    # start_urls=[r'https://www.baidu.com/s?wd=%E6%9C%88%E7%A7%91%E6%8A%80&rsv_spt=1&rsv_iqid=0xb3ed79f0001525c1&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=9&rsv_sug1=9&rsv_sug7=101&rsv_t=4793C5NsAf5aHgVjwst9Rb7oT5zfBEPnCr3r82r9F%2Bgv0PDCPugh%2BeBtI0kyp9lcuxGn&rsv_sug2=0&inputT=3717&rsv_sug4=8000']
    start_urls = urls
    #start_urls = [r'https://www.baidu.com/s?wd=月科技']
    #start_urls =['http://www.cocloud.net/2013/09/10/scrapy_img_spider.html',]
    
    # start_urls=[r'https://www.google.com.hk/search?hl=en&q=月科技']
    
    rules=(
        # Rule(LinkExtractor(restrict_css='#navcnt'),follow=True),
        #Rule(LinkExtractor(restrict_css='#page'),follow=True),
        Rule(LinkExtractor(restrict_css='h3'),callback='parse_item',follow=True),
        #Rule(LinkExtractor(deny_domains=('baidu.com')),callback='parse_item',follow=True)
        
    )
    #self.settings
    custom_settings={
        'CONCURRENT_REQUESTS' : 100,
        'REACTOR_THREADPOOL_MAXSIZE' : 20,
        'COOKIES_ENABLED' : False,
        'RETRY_ENABLED' : False,
        'DOWNLOAD_TIMEOUT' : 15,
        
        'DEPTH_LIMIT':3,
        # 'USER_AGENT': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        # 'IMAGES_STORE': 'D:/try/image',
        #'FILES_STORE' : 'D:/try/path',
        'ITEM_PIPELINES':{
            'tutorial.pipelines.EmailPipline':100,
            #'tutorial.pipelines.HtmlPipe':110,
        },

        'DOWNLOADER_MIDDLEWARES':{
            # 'tutorial.middle.Goagent':80,
            # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100,
            'tutorial.middle.SaveAll':70,
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware':100,
            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,  
            # 'tutorial.middle.RotateUserAgentMiddleware' :100              
        },        
        
    }
    #def parse_start_url(self,response):
        #for i in self.func(response):
            #yield i
    
    #def func(self,response):
        #for i in response.css('h3 a::attr(href)'):
            #l=LinkItem(link = i.extract())
            #yield l
    
    #def parse_page(self,response):
        #for i in self.func(response):
            #yield i      
            
    #def parse(self,response):
        #l=HtmlBody()
        #l['url']=response.url
        #l['content']=response.body
        #yield l
        #for i in super(GpSearch,self).parse(response):
            #yield i
            
    def parse_item(self, response):
        #l=LinkItem(link = response.url)
        #for i in response.css('title'):
            #l['title']=i.extract()
        #yield l
        
               
        for email in response.selector.re('\w+@\w+.\w+'):
            l = EmailItem()
            for i in response.css('title::text'):
                l['title']=i.extract()             
            l['email']=email
            
            yield l
        # print(response.url)
    