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
    'dirs':[(xxx,bbb),],
    'include_dir':lamda x : xxx,
    'include_file':lamda src,dst:xxx
    }
    """
    for src,dst in dc.get('dirs'):
        s=RepToApp(src,dst,dc)
        s.read_stamp()
        s.run()
        t = AppToRep(dst,src,dc)
        t.read_stamp()
        t.run()
        
        
        ls=[]
        for i in t.warn_files:
            if i in s.warn_files:
                ls.append(i)
        for x, y in ls:
            # if file was found bouth in target.warn_file and src.warn_file, then means stamp file left behind src and dst file.
            # this is a kind of conflict because the same file has been modified in two side without sync.
            
            print('[warning] %s----conflict-----%s'%( x,y))
        
        if not ls:
            t.update_stamp()
            print('no warning')



class RepToApp(SynCopy):
    def __init__(self, src,dst,dc):
        SynCopy.__init__(self,src,dst)
        self.dc = dc
        self.stamp_path = os.path.join(dst,'stmp.txt')
        self.warn_files=[]
  
    def include_dir(self,src_dir):
        if self.dc.get('include_dir'):
            return self.dc.get('include_dir')(src_dir)
        else:
            return True
    
    def include_file(self,src,dst):
        if src == self.stamp_path:
            return False
       
        elif self.dc.get('include_file'):
            if self.dc.get('include_file')(src,dst):
                if self.newer_than_stamp(dst):
                    if not self.content_eq(src,dst):  # when resolve conflict ,this express will make process skiping push_file
                        self.record_modified_file(os.path.normpath( src),os.path.normpath( dst) )      # so, make stamp update
                    return False

                if self.newer(src, dst):
                    return True   
        return False
                

    
    
    def record_modified_file(self,src,dst):
        self.warn_files.append((src,dst))
    
    def newer_than_stamp(self, path):
        if os.path.exists(path) and datetime.fromtimestamp( getmtime(path) )>self.stamp:
            return True
    
    def read_stamp(self):
        if os.path.exists(self.stamp_path):
            self.stamp=datetime.strptime( open(self.stamp_path,'r').read(),'%Y-%m-%d %H:%M:%S')
        else:
            self.stamp = datetime.fromtimestamp(0)    
            
    def update_stamp(self):
        with open(self.stamp_path,'w') as f:
            f.write(datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'))   

class AppToRep(RepToApp):
    def __init__(self, src, dst, dc):
        super(AppToRep,self).__init__(src, dst, dc)
        self.stamp_path = os.path.join(src,'stmp.txt')
    
    def record_modified_file(self,src,dst):
        self.warn_files.append((dst,src))
        
def main():
    print(datetime.now())
    if args.conf:
        sync_with_config(args.conf)
         

if __name__=='__main__':
    main()