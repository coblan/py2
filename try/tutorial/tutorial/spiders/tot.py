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
    name='baidu'
    allowed_domains =['mokitech.com']
    start_urls =['http://www.mokitech.com/']
    rules=(
        Rule(LinkExtractor(),callback='parse_item'),
        
    )
    
    def parse_item(self, response):
        print('here')
        print(response.url)
        for i in response.xpath('//img/@src'):
            print(i)
            yield TutorialItem(link=i)
        # for i in response.xpath('//a/@href'):
            # print(i.extract())