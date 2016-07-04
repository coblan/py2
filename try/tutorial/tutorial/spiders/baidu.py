# -*- encoding:utf-8 -*-

import scrapy

from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import LinkItem,EmailItem
import wingdbstub

class GpSearch(CrawlSpider):
    name='baidu'
    
    # allowed_domains =['mokitech.com']
    start_urls=[r'https://www.baidu.com/s?wd=月科技&rsv_spt=1&rsv_iqid=0xee4521c20021ac50&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=3&rsv_sug1=2&rsv_sug7=101&rsv_t=f8bbDuxD7RErED6qK8OR8RzuZO09E7E5yq6KbWSHhz4Ru6lJ99sH9DOKbsrUIraR3MIu&rsv_sug2=0&inputT=8383&rsv_sug4=10856']
    #start_urls = ['https://www.baidu.com/s?wd=%E6%9C%88%E4%BA%AE']
    #start_urls =['http://www.cocloud.net/2013/09/10/scrapy_img_spider.html',]
    # start_urls=[u'https://www.baidu.com/s?wd=%E6%9C%88%E4%BA%AE&rsv_spt=1&rsv_iqid=0xb86a98b10001667e&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=6&rsv_sug1=6&rsv_sug7=101&rsv_t=e705kmRTdHUVTphKETs67ydPfZOTdgSeF3S96ng0pKOI37STzr6pBcQDF7UncCaG0r6L&rsv_sug2=0&inputT=2154&rsv_sug4=4193']
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
            'tutorial.pipelines.EmailPipline':100
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
    
    def parse_item(self, response):
        #l=LinkItem(link = response.url)
        #for i in response.css('title'):
            #l['title']=i.extract()
        #yield l
        
               
        for email in response.selector.re('\w+@\w+.\w+'):
            l = EmailItem()
            for i in response.css('title'):
                l['title']=i.extract()             
            l['email']=email
            
            yield l
        # print(response.url)
    