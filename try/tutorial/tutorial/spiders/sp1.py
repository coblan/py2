# -*- encoding:utf-8 -*-

import scrapy

from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ImgItem
#import wingdbstub

class Google(CrawlSpider):
    name='google'
    # allowed_domains =['mokitech.com']
    #start_urls =['http://www.cocloud.net/2013/09/10/scrapy_img_spider.html',]
    # start_urls=['http://wow.178.com/201605/257793690793.html']
    # start_urls=['https://www.baidu.com/s?wd=%E6%9C%88%E4%BA%AE']
    start_urls=['https://www.google.com.sg/?gfe_rd=cr&ei=zLRHV4nZNrDY8geQ3aCABw#q=月亮']
    rules=(
        Rule(LinkExtractor(),callback='parse_item'),
        
    )
    custom_settings={
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        'DEPTH_LIMIT':1,
        'IMAGES_STORE': 'D:/try/image/google',
        #'FILES_STORE' : 'D:/try/path',
        'ITEM_PIPELINES':{
            #'tutorial.tmppip.Tmp':100,
            #'scrapy.pipelines.files.FilesPipeline': 1,
            'scrapy.pipelines.images.ImagesPipeline': 100
            #'scrapy.contrib.pipeline.images.ImagesPipeline':200,
        },
        
    }
    def parse_item(self, response):
        # print('here')
        # print(response.url)
        #for i in response.xpath('//img/@src'):
            #l=ImgItem()
            #l['image_urls']=[response.urljoin(i.extract())]
            #l['file_urls'] =[response.urljoin(i.extract()),]
            #yield l
        ls=[response.urljoin(i.extract()) for i in response.xpath('//img/@src')]
        yield ImgItem(image_urls=ls)