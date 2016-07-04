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


class EmailPipline(object):
    def process_item(self, item, spider):
        #self.file.write(unicode(item).encode('utf8')+'\n')
        save_email(item.email,item.title)
        return item