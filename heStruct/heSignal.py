# -*- encoding:utf-8 -*-

class Signal(object):
    def __init__(self,*args,**kw):
        """
        args: 位置参数的名字 如 ('name','age')
        kw : 关键字参数及其默认值： name='jone',age=18
        
        self.emit() 必须与 构造函数中的 参数一一对应
        """
        self.funcs=[]
        self.args=args
        self.kw=kw
        
    def connect(self,func,uniqu=True):
        if uniqu and func in self.funcs:
            return
        self.funcs.append(func)
        
    def disconnect(self,func):
        if func in self.funcs:
            self.funcs.remove(func)
            
    def emit(self,*args,**kw):
        try:
            for k,v in zip(self.args,args):
                kw[k]=v
            for k,v in self.kw:    # 把默认值 赋值给 实际的kw。 默认值是Signal的构造函数中获取到的
                if k not in kw:
                    kw[k]=v
        except Exception as e:
            print('emit args and kw not match with signal args and kw ')
            raise e
        
        for fun in self.funcs:
            fun(**kw)

dc={}
cnt=0
def reciver(signal_name,name=None):
    def _func(func):
        connect(signal_name, func,name)
        def _innfunc(*args,**kw):
            return func(*args,**kw)
        return _innfunc
    return _func
        

def connect(signal_name,func,name=None):
    global cnt
    if not name:
        name='name%s'%cnt
        cnt+=1
    if signal_name in dc:
        dc[signal_name][name]=func
    else:
        dc[signal_name]={name:func}
        
def fire(signal_name,*args,**kw):
    if signal_name not in dc:
        return
    for k ,v in dc[signal_name].items():
        v(*args,**kw)
    