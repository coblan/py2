# -*- encoding:utf-8 -*-

import scrapy

from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import LinkItem,EmailItem,HtmlBody
import wingdbstub

class GpSearch(CrawlSpider):
    name='baidu'
    
    # allowed_domains =['mokitech.com']
    #start_urls=[r'https://www.baidu.com/s?wd=月科技&rsv_spt=1&rsv_iqid=0xee4521c20021ac50&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=3&rsv_sug1=2&rsv_sug7=101&rsv_t=f8bbDuxD7RErED6qK8OR8RzuZO09E7E5yq6KbWSHhz4Ru6lJ99sH9DOKbsrUIraR3MIu&rsv_sug2=0&inputT=8383&rsv_sug4=10856']
    
    #start_urls = [r'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E6%9C%88%E7%A7%91%E6%8A%80&rsv_pq=a81514370000ec70&rsv_t=1cc4H7YnCOtNC5%2FEjW7%2BKT%2FZAMENQDbd8GyeahsogLxG%2FNGzUAtnMdGTFoM&rqlang=cn&rsv_enter=1&rsv_n=2&rsv_sug3=1']
    #start_urls =['http://www.cocloud.net/2013/09/10/scrapy_img_spider.html',]
    start_urls=[r'https://www.google.com.hk/?gws_rd=cr#newwindow=1&safe=strict&q=%E6%9C%88%E7%A7%91%E6%8A%80&btnK=Google+%E6%90%9C%E7%B4%A2']
    #start_urls=[u'https://www.google.com.hk/?q=scrapy+proxy#newwindow=1&safe=strict&q=scrapy+proxy']
    rules=(
        Rule(LinkExtractor(restrict_css='#page'),follow=True),
        Rule(LinkExtractor(restrict_css='h3'),callback='parse_item',follow=False)
        
    )
    custom_settings={
        'CONCURRENT_REQUESTS' : 100,
        'DEPTH_LIMIT':2,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        # 'IMAGES_STORE': 'D:/try/image',
        #'FILES_STORE' : 'D:/try/path',
        'ITEM_PIPELINES':{
            'tutorial.pipelines.EmailPipline':100,
            #'tutorial.pipelines.HtmlPipe':110,
        },
        
        'DOWNLOADER_MIDDLEWARES':{
            'tutorial.middle.Goagent':80,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100,
            'tutorial.middle.SaveAll':70,
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware':100,
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
    