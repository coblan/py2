# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class MyPipeline(object):
    def __init__(self):
        self.file=open('d:/try/fuck.txt','w')
        
    def process_item(self, item, spider):
        print('wa haha')
        print(item)
        self.file.write(item.get('link')+'\n')
        return item

