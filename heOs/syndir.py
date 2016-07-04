# -*- coding:utf-8 -*-

"""
syn_copy(_from,_to,except_=None,except_name=func_copy) :
      见函数docstring
"""

import sys,os
from os.path import *
import shutil
from heStruct.heSignal import Signal

class SynCopy(object):
    def __init__(self,src,dst):
        self.success_update=Signal('src','dst')
        self.src=src
        self.dst=dst
        
    def should_include_dir(self,src_dir):
        """
        @src_dir:
        overwrite  to  指定需要包含的 目录
        """
        return True
    
    def should_incude_name(self,src,dst):
        """
        overwrite to 指定需要包含的名字
        """
        return self.is_modify(src, dst) 
    
    def run(self):
        if not os.path.exists(self.src):
            return
        if isfile(self.src):
            return self._syn_file(self.src, self.dst)
        else:
            for root,dirs,files in walk(self.src,self.should_include_dir):
                rel=relpath(root,self.src)
                root_to=normpath(join(self.dst,rel))
                if self.should_incude_name(root,root_to):
                    self._mkdir_ifnot(root_to)
  
                for ii in dirs:
                    drnm=normpath(join(root_to,ii))
                    if self.should_incude_name(join(root,ii),drnm):
                        self._mkdir_ifnot(drnm)
         
                for jj in files:
                    flnm=normpath(join(root_to,jj))
                    #if self.should_incude_name(join(root,jj),flnm):
                    self._syn_file(join(root,jj), flnm)
        
    def _mkdir_ifnot(self,path):
        if not exists(path):
            os.mkdir(path)
            
    def _syn_file(self,src,dst):
        if not self.should_incude_name(src,dst):
            return
        try:
            shutil.copyfile(src,dst)
            self.success_update.emit(src,dst)
            print(u"复制文件 :从"+src+u"到---->>>"+dst)     
        except Exception as e:
            print(u"复制文件  %s错误, 错误为:%s"%(src,e))            
    
      
    
    def is_modify(self,src,dst):
        return not exists(dst) or int(getmtime(src))>int(getmtime(dst))
    
   
    
            
#def syn_copy(_from,_to,except_=None,except_name=sud_exclude):
    #"""同步拷贝。_from:样板目录；_to:修正目录；
    #Args:
    #@except:func(from_dir_name),传入_from中的目录名，return True时改目录不被处理，也就不会同步；
    #@except_name:func(from_name,to_name),传入的from_name文件名或目录是肯定存在的，to_name是目标路径(当前不一定存在)
                #return True 时，文件/目录不被拷贝，注意:如果是目录，其子孙文件同样会被处理,如果想不处理其子孙文件，
                #可以在except参数指定的func中过滤掉改文件夹."""
    #if not exists(_from):
        #return
    #elif isfile(_from):
        #return syn_file(_from,_to)
    
    ##except_name=filter_not_modify(except_name)
    
    #for root,dirs,files in walk(_from,except_):
        #rel=relpath(root,_from)
        #root_to=normpath(join(_to,rel))
        #if not except_name(root,root_to):
            #try:
                #os.mkdir(root_to)
            #except:
                #pass
        #for ii in dirs:
            #drnm=normpath(join(root_to,ii))
            #if not except_name(join(root,ii),drnm):
                #try:
                    #os.mkdir(drnm)
                    #print(u"创建文件夹:"+drnm)
                #except:
                    #pass
        #for jj in files:
            #flnm=normpath(join(root_to,jj))
            #if not except_name(join(root,jj),flnm):
                #try:
                    #if exists(flnm):
                        #os.remove(flnm)
                    #shutil.copyfile(join(root,jj),flnm)
                    #print(u"复制文件 :从"+join(root,jj)+u"到---->>>"+flnm)
                #except Exception as e:
                    #print(u"复制文件  %s错误, 错误为:%s"%(flnm,e))
                    
                    
#def syn_file(_from,_to):
    #if not sud_exclude(_from, _to):
        #shutil.copyfile(_from,_to)
        #print(u"复制文件 :从"+_from+u"到---->>>"+_to)


#def delDir(dir_,except_=None,except_name=None):
    #"""该函数用于删除某个目录
    
    #Args:
    #@dir_:需要被删除的目录名
    #@except_:func(dir_name)一个函数，接受目录名,return True，该目录名中所有文件都不会在删除列表中
    #@except_name:fun(name)，函数，接受文件名或目录名,return True，该文件或目录确定不会被删除
    
    #用法，使用except_函数控制整个文件夹的删除与否。使用except_name控制单个文件的删除与否
#"""
    #del_dirs=[]
    #del_files=[]
    #for root,dirs,files in walk(dir_,except_):
        #for ii in dirs:
            #if not except_name or not except_name(join(root,ii)):
                #del_dirs.append(join(root,ii))
        #for jj in files:
            #if not except_name or not except_name(join(root,jj)):
                #del_files.append(join(root,jj))
    #for ii in del_files:
        #try:
            #os.remove(ii)
            #print(u"已经删除文件:"+ii)
        #except Exception as e:
            #print(u"删除文件 %s 错误,原因:%s"%(ii,e))
    #del_dirs.sort(reverse=True)
    #for jj in del_dirs:
        #try:
            #os.rmdir(jj)
            #print(u"已经 删除文件夹:"+jj)
        #except :
            #pass
    #try:
        #os.rmdir(dir_)
        #print(u"成功删除了文件夹: "+dir_)
    #except:
        #pass
        ##print("删除文件夹 %s 错误 :%s"%(dir_,e))

class SynDel(object):
    def __init__(self,src,dst):
        self.src=src
        self.dst=dst
        self.del_files=[]
        self.del_dirs=[]
        
    def should_include_dir(self,dst_dir):
        return True
    def should_include_name(self,src,dst):
        return True
        
    def run(self):
        #del_dirs=[]
        #del_files=[]
        
        print(u"正在整理目录"+" %s..X..%s"%(self.src,self.dst))
        if isfile(self.src) or isfile(self.dst):
            self.sync_del_file(self.src,self.dst)
        else:
            for root,dirs,files in walk(self.dst,self.should_include_dir):
                root_from=normpath(join(self.src,relpath(root,self.dst)))
                for ii in dirs:
                    from_now=os.path.join(root_from,ii)
                    to_now=join(root,ii)
                    if self.should_include_name(from_now,to_now)\
                       and not os.path.exists(from_now):
                        self.del_dirs.append(to_now)
        
                for jj in files:
                    from_now=join(root_from,jj)
                    to_now=join(root,jj)
                    self.sync_del_file(from_now,to_now)
                #if self.should_include_name(from_now,to_now) \
                   #and not os.path.exists(from_now):
                    #del_files.append(to_now)
        #for ff in del_files:
            #try:
                #os.remove(ff)
                #print(u"已经删除文件:"+ff)
            #except Exception as e:
                #print(u"删除  %s  出错 ,原因:%s"%(ff,e))
    
        #for dd in del_dirs:
            #try:
                #os.rmdir(dd)
                #print(u"经常删除文件夹:"+dd)
            #except:
                #pass
        self.exec_del()
            
    def sync_del_file(self,src,dst):
        if self.should_include_name(src,dst) \
           and not os.path.exists(src):
            self.del_files.append(dst) 
            
    def exec_del(self):
        for ff in self.del_files:
            try:
                os.remove(ff)
                print(u"[delete] 已经删除文件:"+ff)
            except Exception as e:
                print(u"删除  %s  出错 ,原因:%s"%(ff,e))
    
        for dd in self.del_dirs:
            try:
                os.rmdir(dd)
                print(u"经常删除文件夹:"+dd)
            except:
                pass 
        print(u'sync del  over...')
            
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


def walk(dir_,include=None):
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