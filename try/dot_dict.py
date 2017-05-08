class DotDict(dict):
    def __init__(self,*args,**kws):
        super(DotDict,self).__init__(*args,**kws)
        self.__dict__=self
        
    def __setattr__(self,name,value):
        if name=='__dict__':
            super(DotDict,self).__setattr__(name,value)
        else:
            self[name]=value

class DotObj(object):
    def __init__(self,dc):
        for k,v in dc.items():
            setattr(self,k,v)
    def __getattr__(self,name):
        try:
            return object.__getattr__(self,name)
        except AttributeError:
            return None


if __name__=='__main__':
    dc={'name':'dog'}
    ss=DotDict(dc)
    print(ss.name)
    
    er= DotObj(dc)
    print(er.name)