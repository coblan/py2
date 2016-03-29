# -*- encoding:utf-8 -*-
from django.db import models
import json

def to_dict(instance,filt_attr=None):
    """
    filt_attr(instance)是可调用对象，返回一个字典，包含已经处理过的属性。这些属性不会再被to_jd操作。
    
    注意，返回的字典，一定是可以json化的才行。
    """
    
    fields=instance._meta.fields
    if filt_attr:
        out=filt_attr(instance)
    else:
        out={}
    for field in fields:
        if field.name in out:
            continue
        else:
            if isinstance(field,models.ForeignKey):
                out[field.name]=getattr(instance,field.name).pk
            else:
                out[field.name]=field.get_prep_value( getattr(instance,field.name) )
    out['pk']=instance.pk
    return out


def from_dict(dc,model,pre_proc=None):
    """

    1. 半自动：
    processed_attr=pre_proc(dc,model) ; 返回处理过的字典processed，该processed用于剔除传入的dc参数
    
    """
    processed={}
    if pre_proc:
        processed=pre_proc(dc,model)
    for k in processed:
        dc.pop(k)         # 去除被pre_proc处理过的值， (因为处理过的值，不应再被 _convert_foreign处理)
    _convert_foreign(dc,model)
    dc.update(processed)   # 把pre_proc的值合并回去 ，(因为下面要给 instance赋值)
    pk=dc.get('pk')
    if pk:
        instance=model.objects.get(pk=pk) 
        for k,v in dc.items():
            setattr(instance,k,v)       
        return instance            
    else:
        instance=model.objects.create(**dc)
        return instance
    
def _convert_foreign(dc,model):
    fields=model._meta.fields
    for field in fields:
        if field.name in dc and isinstance(field,models.ForeignKey):
            dc[field.name]=_deserilize_foreignkey(field, dc[field.name])    

def _deserilize_foreignkey(field,pk):
    model=field.rel.to
    return model.objects.get(pk=pk)
    
    
                
            
            
    