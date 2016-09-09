# -*- encoding:Utf-8 -*-
#import wingdbstub
from heOs.syndir import SynCopy,SynDel
import sys
import json

import argparse
from datetime import datetime
import time
from os.path import getmtime
import os.path

parser = argparse.ArgumentParser() 
parser.add_argument("-s", help="source dir") 
parser.add_argument("-d", help="dest dir") 
parser.add_argument('-c',"--conf", help="input config file ,json formate") 
args = parser.parse_args()


def sync_with_config_file(conf):
    dc={}
    execfile(conf, globals(), dc)
    sync(dc)
        

def sync(dc):
    """
    dc={
    'dirs':[(xxx,bbb),]
    }
    """
    for src,dst in dc.get('dirs'):
        s=CustomSync(src,dst)
        s.run()    

class CustomSync(SynCopy):
    def __init__(self, dc):
        SynCopy.__init__(self,src,dst)
        self.dc = dc
        
    def include_dir(self,src_dir):
        if self.dc.get('include_dir'):
            return self.dc.get('include_dir')(src_dir)
        else:
            return True
    
    def include_file(self,src,dst):
        if not self.is_modify(src, dst):
            return False
        if self.dc.get('include_file'):
            return self.dc.get('include_file')(src,dst)
        else:
            return True

def main():
    print(datetime.now())
    if args.conf:
        sync_with_config(args.conf)
         

if __name__=='__main__':
    main()