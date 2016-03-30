# -*- encoding:utf-8 -*-
"""
考虑到，可追溯性，所以Signal设计为一个类的形式，在使用时都会生成一个对象，从而达到可追溯的目的。最初的字符串的形式，是不能达到这种目的的。

Example: 
A类发送信号，B类接受
class A:
    def __init__(self):
        self.edited=Signal('text',edtor='heyulin')    # 关键字参数，起到了赋值default的作用
    
    def setText(self,text):
        dosome_edit_work(text)
        self.edited.emit(text)    # recived function= func(text=text,editor='heyulin')
        
        #self.edited.emit(text,editor='zhangrong')    # recived function= func(text=text,editor='zhangrong')

# Client
class B:
    def __init__(self):
        editor=A()
        editor.edited.connect(self.dosomething)   # 链接信号
        
    def dosomething(self,**kw):   # 有些handler参数较signal.emit少，所以需要加上**kw关键字参数，否则python会报错。
        ...

"""

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


##########################
#下面的代码不再使用
##########################

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
    