import scrapy

from scrapy.spiders import Spider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import LinkItem
#import wingdbstub

class LocalTest(Spider):
    name='cuslocal'
    # allowed_domains =['mokitech.com']
    #start_urls =['http://www.cocloud.net/2013/09/10/scrapy_img_spider.html',]
    start_urls=['http://localhost:3456/']
    # rules=(
        # Rule(LinkExtractor(),callback='parse_item',follow=True),
    # )
    custom_settings={
        'DEPTH_LIMIT':1,
        # 'IMAGES_STORE': 'D:/try/image',
        #'FILES_STORE' : 'D:/try/path',
        'ITEM_PIPELINES':{
            'tutorial.pipelines.MyPipeline':100
        },
        
    }
    def parse(self, response):
        for i in self.parse_item(response):
            yield i
        for href in response.css('a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url)        
        
    def parse_item(self, response):
        yield LinkItem(link = response.url)
        # print(response.url)
    