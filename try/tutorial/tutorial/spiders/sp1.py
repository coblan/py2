import scrapy

from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ImgItem
import wingdbstub

class Google(CrawlSpider):
    name='google'
    # allowed_domains =['mokitech.com']
    start_urls =['https://www.google.com/']
    rules=(
        Rule(LinkExtractor(),callback='parse_item'),
        
    )
    custom_settings={
        'DEPTH_LIMIT':1,
        'IMAGES_STORE': 'D:/try/image',
        'ITEM_PIPELINES':{
            # 'tutorial.tmppip.Tmp':100,
            'scrapy.pipelines.images.ImagesPipeline': 100
        },
        
    }
    def parse_item(self, response):
        # print('here')
        # print(response.url)
        for i in response.xpath('//img/@src'):
            l=ImgItem()
            l['image_urls']=response.urljoin(i.extract())

            yield l