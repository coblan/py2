# -*- encoding:utf8 -*-
import threading
from django.db import models
import time
from struct import get_or_none
from django.db import transaction
import pickle
from django.utils import timezone
import json

funcs={}
def loopFunc(name):
    def _func(func):
        funcs[name]=func
        def __func(**kw):
            return func(**kw)
        return __func
    return _func

class OneTimeCmd(object):
    def process(self,work):
        if work.kw:
            kw=json.loads(work.kw)
        else:
            kw={}
        rt=funcs[work.func](**kw)
        work.rt=rt
        work.done=True
        work.save() 
        return rt

class AlwaysCmd(object):
    def process(self,work):
        if work.kw:
            kw=json.loads(work.kw)
        else:
            kw={}
        rt=funcs[work.func](**kw)
        work.rt=rt
        work.fetched=False
        #work.done=True
        work.save() 
        return rt    

def work_proc(funcs):
    while True:
        time.sleep(60*5)
        while True:
            work=None
            with transaction.atomic():
                work=get_or_none(WorksModel,fetched=False,done=False,sud_time__lte=timezone.now())
                if work:
                    work.fetched=True
                    work.save()
            if work:
                if globals().get(work.category):
                    obj=globals().get(work.category)()
                    obj.process(work)
                
                break
            else:
                break
            
dog = []
@loopFunc('test')
def test():
    dog.append('hash')

def test_view():
    return str(dog)

class WorksModel(models.Model):
    func=models.CharField('函数名',max_length=300,blank=True)
    kw=models.TextField('关键字参数',blank=True)
    rt=models.TextField('返回结果',blank=True)
    sud_time=models.DateTimeField('应该处理时刻',auto_now=True,blank=True,null=True)
    fetched=models.BooleanField('是否被认领',default=False)
    done=models.BooleanField('是否已处理',default=False)
    category=models.CharField('类型',max_length=100,blank=True)        

#worker=threading.Thread(target=work_proc,args=(funcs,))
#worker.start()




