# -*- encoding:Utf-8 -*-
#import wingdbstub
from heOs.syndir import SynCopy,SynDel
import sys
import json
import re
import argparse
from datetime import datetime
import time
#from peewee import *
from os.path import getmtime
import os.path
from heTools.webkit import main
from js_logic import Dog

parser = argparse.ArgumentParser() 
parser.add_argument("-s", help="source dir") 
parser.add_argument("-d", help="dest dir") 
parser.add_argument('-c',"--conf", help="input config file ,json formate") 
args = parser.parse_args()


def sync_with_config_file(conf):
    #with open(conf) as f:
    dc={}
    execfile(conf, globals(), dc)
    sync_with_config(dc)
    
def sync_with_config(dc):
    for src,dst in dc.get('dirs'):
        s=CustomSync(src,dst,dc.get('ignore_files'))
        s.run()
        dog=Dog()
        dog.files=s.result
        print(repr(dog.get_files()))
        main('sync.html',dog)
      
class CustomSync(SynCopy):
    def __init__(self, src,dst,ignore):
        SynCopy.__init__(self,src,dst)
        self.ignore = ignore
        self.result=[]
        
    def include_dir(self,src_dir):
        if re.search(self.ignore,src_dir):
            return False
        else:
            return True
    
    def include_file(self,src,dst):
        if not self.is_modify(src, dst):
            return False
        if re.search(self.ignore,src):
            return False
        else:
            return True
    
    def process(self, src, dst):
        self.result.append((src,dst))
        print(src,dst)
    

# def main():
    # print(datetime.now())
    # if args.conf:
        # sync_with_config_file(args.conf)
         

# if __name__=='__main__':
    # main()