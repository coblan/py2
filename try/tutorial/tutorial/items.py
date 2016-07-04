# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class LinkItem(scrapy.Item):
    title=scrapy.Field()
    link=scrapy.Field()
    
    def __unicode__(self):
        return self.get('title') + '\t' + self.get('link')

class EmailItem(scrapy.Item):
    email = scrapy.Field()
    title = scrapy.Field()


class ImgItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()  
    file_urls = scrapy.Field()
    file= scrapy.Field()