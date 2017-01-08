# -*- coding:utf-8 -*-

"""
syn_copy(_from,_to,except_=None,except_name=func_copy) :
      见函数docstring
"""
from __future__ import unicode_literals
import sys,os
from os.path import *
import os
import shutil
from heStruct.heSignal import Signal
from shutil import rmtree

class SynCopy(object):
    def __init__(self,src,dst):
        self.success_update=Signal('src','dst')
        self.src=src
        self.dst=dst
    
    def process(self,src,dst):
        self._copy_file(src, dst)   
        
    def include_dir(self,src_dir):
        """
        @src_dir:
        overwrite  to  指定需要包含的 目录
        """
        return True
    
    def include_file(self,src,dst):
        """
        overwrite to 指定需要包含的名字
        """
        return self.is_modify(src, dst) 
    
    def run(self):
        print('开始同步目录{src}==={dst}'.format(src=self.src,dst=self.dst))
        if not os.path.exists(self.src):
            return
        if isfile(self.src):
            return self._syn_file(self.src, self.dst)
        else:
            for root,dirs,files in os.walk(self.src):
                dirs[:]=filter(self.include_dir,dirs)
                
                rel = os.path.relpath(root,self.src)
                dst_root = os.path.join(self.dst,rel)
                
                dst_dir_paths = [os.path.join(dst_root,dir) for dir in dirs]
                for path in dst_dir_paths:
                    self._mkdir_if_not(path)
                
                src_files_paths = [os.path.join(root,file) for file in files]
                dst_files_paths = [os.path.join(dst_root,file) for file in files]
                
                should_update_files = [(src,dst) for src,dst in zip(src_files_paths,dst_files_paths) if self.include_file(src,dst)]
                
                for src,dst in should_update_files:
                    self.process(src, dst)
                    
  
    def _mkdir_if_not(self,path):
        if not exists(path):
            os.makedirs(path)
    
    
        
    def _copy_file(self,src,dst):
        #if not self.should_incude_name(src,dst):
            #return
        try:
            shutil.copy2(src,dst)
            self.success_update.emit(src,dst)
            print(u"复制文件 :从"+src+u"到---->>>"+dst)     
        except Exception as e:
            print(u"复制文件  %s错误, 错误为:%s"%(src,e))            
    
      
    
    def is_modify(self,src,dst):
        return self.newer(src, dst)
    
    def newer(self,src,dst):
        if not os.path.exists(dst):
            return True
        else:
            return  int(getmtime(src))-1 >int(getmtime(dst))
        
    def content_eq(self,src,dst):
        if os.path.exists(src) and os.path.exists(dst):
            return open(src).read() == open(dst).read()
        return False
    

class SynDel(object):
    def __init__(self,src,dst):
        self.src=src
        self.dst=dst
        self.del_files=[]
        self.del_dirs=[]
        
    def aware_dir_name(self,root,dst_dir_name):
        return True
    def aware_file_name(self,src_file_path,dst_file_path):
        return True
        
    def run(self):
        print(u"开始清理目录"+" %s..X..%s"%(self.src,self.dst))
        if isfile(self.src) or isfile(self.dst):
            self.append_del_file_list(self.src,self.dst)
        else:
            for root,dirs,files in walk(self.dst,self.aware_dir_name):
                crt_src_root=normpath(join(self.src,relpath(root,self.dst)))
                for ii in dirs:
                    src_child_dir=os.path.join(crt_src_root,ii)
                    dst_child_dir=join(root,ii)
                    if not os.path.exists(src_child_dir):
                        self.del_dirs.append(dst_child_dir)
        
                for jj in files:
                    src_child_file=join(crt_src_root,jj)
                    dst_child_file=join(root,jj)
                    self.append_del_file_list(src_child_file,dst_child_file)

        self.exec_del()
            
    def append_del_file_list(self,src_file_path,dst_file_path):
        if self.aware_file_name(src_file_path,dst_file_path) \
           and not os.path.exists(src_file_path):
            self.del_files.append(dst_file_path) 
            
    def exec_del(self):
        try:
            for ff in self.del_files:
                os.remove(ff)
                print(u"[delete] 已经删除文件:"+ff)
                
            for dd in self.del_dirs:
                rmtree(dd)
                #os.rmdir(dd)
                print(u"[delete]已经删除文件夹:"+dd)
            print(u'sync del  over...')
        except Exception as e:
            print(u"删除  %s  出错 ,原因:%s"%(ff,e))        
            
def syn_del(src,dst,except_=None,except_name=None):
    """该函数用于同步src与dst目录，如果dst中的某些文件或文件夹在src不存在，就删除。
    
    Args:
    @src:样本目录;dst:修正目录
    @except:func(dir_name),函数，接受_to中的文件目录名,return True，改文件夹不会被修正
    @except_name:func(from_name,to_name),函数，接受文件或目录名，return True，该文件或裸目录不会被修正。
                 由于遍历的是_to目录，所以to_name是肯定存在的，from_name是组合出来的，
                 可以判断from_name文件是否存在从而判断是否删除to_name
"""
    del_dirs=[]
    del_files=[]
    print(u"正在整理目录"+"...")
    for root,dirs,files in walk(dst,except_):
        root_from=normpath(join(src,relpath(root,dst)))

        for ii in dirs:
            from_now=os.path.join(root_from,ii)
            to_now=join(root,ii)
            if (not except_name or not except_name(from_now,to_now)) \
               and not QFileInfo(from_now).exists():
                del_dirs.append(to_now)

        for jj in files:
            from_now=join(root_from,jj)
            to_now=join(root,jj)
            if (not except_name or not except_name(from_now,to_now)) \
               and not QFileInfo(from_now).exists():
                del_files.append(to_now)
    for ff in del_files:
        try:
            os.remove(ff)
            print(u"已经删除文件:"+ff)
        except Exception as e:
            print(u"删除  %s  出错 ,原因:%s"%(ff,e))

    for dd in del_dirs:
        try:
            os.rmdir(dd)
            print(u"经常删除文件夹:"+dd)
        except:
            pass

def walk(idir,is_dir_include = None):
    for i in os.walk(idir):
        if is_dir_include:
            left_dirs=[]
            for d in i[1]:
                if is_dir_include(i[0],d):
                    left_dirs.append(d)
                    
            i[1][:]= left_dirs #filter(is_dir_include,abs_dirs)
        #left_dirs=filter(is_dir_include,abs_dirs)
        yield i

def walk_old(dir_,include=None):
    """
    模拟python的标准walk函数，但是增加了过滤文件夹功能，如果不需要过滤文件夹，最好还是使用python的标准库吧
    
    @ dir_: best unicode
    @except_: func(dir):return True ,when wan't show dir
    
    yield:
    basedir,[dirs],[files]
    """

    if not include or include(dir_):
        out=__req(dir_)
        if out:
            yield out
            dirs=out[1]
            for ii in dirs:
                for jj in  walk(join(out[0],ii),include):
                    yield jj          


def __req(dir_):
    if not dir_:
        return
    ls=os.listdir(dir_)
    root=dir_
    dirs=[]
    files=[]
    for ii in ls:
        if isdir(join(root,ii)):
            dirs.append(ii)
        else:
            files.append(ii)
    return (root,dirs,files)


if __name__=='__main__':
    #for b,d,fs in walk(r'D:\try\django'):
        #for f in fs:
            #if (f .endswith('.html') ):
                #print(f)
    #def func(from_):
        #if from_.endswith('.pyc'):
            #return False
        #else:
            #return True
        
    ##syn_copy(r'D:\try\django', r'D:\try\dirtry')
    #delDir(r'D:\try\dirtry',except_name=func)
    
    s=SynCopy(ur'D:\try\中文测试', ur'D:\try\pig')
    def func(src,dst):
        pass
    s.success_update.connect(func)
    s.run()