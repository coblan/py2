# -*- encoding:utf8 -*-
from django.http import HttpResponse
import json
def get_or_none(model,**kw):
    """如果数据库有，则返回最新项，否则返回None
    """
    try:
        obj = model.objects.get(**kw)
        return obj
    except model.DoesNotExist: 
        return None
    
def get_or_new(model,**kw):
    """如果数据库有匹配，则返回最新的一项，如果没有匹配项，则返回一个新的对象
    """
    try:
        obj = model.objects.filter(**kw).order_by('-id')[0]
        return obj
    except (model.DoesNotExist,IndexError):
        obj = model(**kw)
        obj.save()
        return obj

_request_func = []
def jsonpost(request,scope):
    """
    from functools import partial
    new_jsonpost = partial(jsonpost,scope=global())
    """
    cmddc = json.loads(request.body)
    outdc = {}
    orderls = cmddc.pop('order',None)
    if orderls:
        for k in orderls:
            func = scope[k]
            if func in _request_func:
                outdc[k]=func(request=request,**cmddc.pop(k))
            else:
                outdc[k]=func(**cmddc.pop(k))
    for k,kw in cmddc.items():
        func = scope[k]
        if func in _request_func:
            outdc[k]=func(request=request,**kw)
        else:
            outdc[k]=func(**kw)
    return HttpResponse(json.dumps(outdc), content_type="application/json")


def require_request(func):
    def _func(*args,**kw):
        return func(*args,**kw)
    _request_func.append(_func)
    return _func

def my_context_proc(request):
    return {'IMG_DIR':'FUCK YOU'}