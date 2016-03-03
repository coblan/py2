
class HeSignal(object):
    def __init__(self,name):
        pass
    
    def regist():
        pass
    def fire(signal_name):
        pass

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
    