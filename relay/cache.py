cnt =0
def remenber(func):
    global cnt
    cnt+=1
    def _func(*args,**kw):
        if not hasattr(_func,'_remenber%s'%_func.index):
            rt = func(*args,**kw)
            setattr(_func,'_remenber%s'%_func.index,rt)
            setattr(_func,'_remenber_args%s'%_func.index,args)
            setattr(_func,'_remenber_kw%s'%_func.index,kw)
            return rt
        else:
            if args== getattr(_func,'_remenber_args%s'%_func.index) and \
               kw ==getattr(_func,'_remenber_kw%s'%_func.index):
                return getattr(_func,'_remenber%s'%_func.index)
            else:
                setattr(_func,'_remenber_args%s'%_func.index,args)
                setattr(_func,'_remenber_kw%s'%_func.index,kw)                
                return func(*args,**kw)
            
    _func.index =cnt
    return _func