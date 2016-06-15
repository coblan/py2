# -*- encoding:utf-8 -*-

import scrapy

from scrapy.spiders import Spider, CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import LinkItem
#import wingdbstub

class GpSearch(CrawlSpider):
    name='broad'
    #rules=(
        #Rule(LinkExtractor(),follow=False),
    
    #)
    custom_settings={
        'DEPTH_LIMIT':2,
        'ITEM_PIPELINES':{
            'tutorial.pipelines.MyPipeline':100
        },
        
    }
    
    def start_requests(self):
        #yield self.make_requests_from_url('http://www.luoyuekeji.com/')
        with open('d:/try/fuck.txt') as f:
            for i in f.readlines():
                c=i.rstrip('\n')
                yield self.make_requests_from_url(c)
        
    def parse(self, response):
        l=LinkItem(link = response.url)
        for i in response.css('title'):
            l['title']=i.css('::text')[0].extract()
        yield l
        # print(response.url)
    