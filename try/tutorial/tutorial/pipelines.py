# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
base_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(base_dir,'db'))

from interface import save_email

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class MyPipeline(object):
    def __init__(self):
        self.file=open('d:/try/fuckME.txt','w')
        
    def process_item(self, item, spider):
        self.file.write(unicode(item).encode('utf8')+'\n')
        return item
    
from items import EmailItem,HtmlBody
import os


class EmailPipline(object):
    def process_item(self, item, spider):
        #self.file.write(unicode(item).encode('utf8')+'\n')
        if isinstance(item,EmailItem):
            save_email(item['email'],item['title'])
        
        return item


class HtmlPipe(object):
    def process_item(self, item, spider):
        if isinstance(item,HtmlBody):
            with open(os.path.join(r'd:/try/html',str(hash(item['url'])))+'.html','w') as f:
                f.write(item['content'])
        else:
            return item
                
        