# -*- encoding:utf-8 -*-

import scrapy

from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import LinkItem
#import wingdbstub

class GpSearch(CrawlSpider):
    name='gp'
    
    # allowed_domains =['mokitech.com']
    start_urls=['https://www.baidu.com/link?url=tBos-KTtchZEKrJGVCjo9f2-nQx6XA3v46756jD_cE3uXLI-O1IFEqA7hphMLd1r&amp;wd=&amp;eqid=e26a8254001fbf24000000035748f822']
    #start_urls = ['https://www.baidu.com/s?wd=%E6%9C%88%E4%BA%AE']
    #start_urls =['http://www.cocloud.net/2013/09/10/scrapy_img_spider.html',]
    # start_urls=[u'https://www.baidu.com/s?wd=%E6%9C%88%E4%BA%AE&rsv_spt=1&rsv_iqid=0xb86a98b10001667e&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=6&rsv_sug1=6&rsv_sug7=101&rsv_t=e705kmRTdHUVTphKETs67ydPfZOTdgSeF3S96ng0pKOI37STzr6pBcQDF7UncCaG0r6L&rsv_sug2=0&inputT=2154&rsv_sug4=4193']
    rules=(
        Rule(LinkExtractor(),callback='parse_item',follow=False),
        
    )
    custom_settings={
        'DEPTH_LIMIT':1,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        # 'IMAGES_STORE': 'D:/try/image',
        #'FILES_STORE' : 'D:/try/path',
        'ITEM_PIPELINES':{
            'tutorial.pipelines.MyPipeline':100
        },
        
    }
    def parse_item(self, response):
        yield LinkItem(link = response.url)
        # print(response.url)
    