# -*- encoding:utf-8 -*-

import scrapy
# from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spiders import CrawlSpider,Rule
# from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.linkextractors import LinkExtractor
from ..items import TutorialItem
# class Baidu(scrapy.Spider):
    # name='baidu'
    # allowed_domains =['baidu.com']
    # start_urls =['http://stackoverflow.com/questions/21788939/how-to-use-pycharm-to-debug-scrapy-projects']
    
    # def parse(self, response):
        # for i in response.xpath('//a/@href'):
            # print(i.extract())
            
        # filename = response.url.split("/")[-2]
        # if not filename:
            # return
        # with open(filename, 'wb') as f:
            # f.write(response.body)    

class Baidu(CrawlSpider):
    name='baiduss'
    #allowed_domains =['mokitech.com']
    #start_urls =['http://www.mokitech.com/']
    start_urls=[r'http://book.douban.com/subject/1626306/','https://www.aliyun.com/']
    rules=(
        Rule(LinkExtractor(deny_domains=['baidu.com']),callback='parse_item'),
        
    )
    custom_settings={
        'ITEM_PIPELINES':{'tutorial.pipelines.MyPipeline':100}
    }
    def parse_item(self, response):
        print('here')
        print(response.url)
        for i in response.xpath('//img/@src'):
            print(i)
            yield TutorialItem(link=i.extract())
        # for i in response.xpath('//a/@href'):
            # print(i.extract())