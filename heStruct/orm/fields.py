# -*- encoding:utf8 -*-
from datetime import datetime,date

class Field(object):
    cnt = 0
    def __init__(self,default =None, NULL=False):
        self.cnt=Field.cnt
        Field.cnt+=1
        self.default=default
        self.NULL = NULL
        self.name = '' # Model中会设置
        self.model=''
    def createstr(self):
        pass
    
    @staticmethod
    def todb(obj):
        pass
    def __set__(self,obj,val):
        pass
    def __get__(self,obj,tp =None):
        fobj =  getattr(obj,"_field%s"%self.cnt,None)    
        if fobj is None:
            if self.default is not None:
                return self.default
            elif self.NULL:
                return None
            else:
                raise AttributeError("%s.%s Has No default Value AND not NULL,so must set the value"%(self.model,self.name))
        else:
            return fobj

class CharField(Field):
    def createstr(self):
        outstr =  self.name+" text" 
        if not self.NULL:
            outstr+= " NOT NULL"
        return outstr
    
    def todb(self,obj):
        if obj is None:
            return "NULL"
        assert isinstance(obj,str)
        obj = obj.replace("'","''")
        return "'%s'"%obj
    
    def __set__(self,obj,val):
        if val is None or isinstance(val,(str,unicode)):  
            setattr(obj,"_field%s"%self.cnt,str(val))
        else:
            raise ValueError("charfield need @str or @unicode")

    
class IntField(Field):
    def todb(self,obj):
        if obj is None:
            return "NULL"
        assert isinstance(obj,int)
        return "%s"%obj
    def createstr(self):
        outstr =  self.name +" INT"
        if not self.NULL:
            outstr+= " NOT NULL"
        return outstr   
    
    def __set__(self,obj,val):
        if val is None:
            setattr(obj,"_field%s"%self.cnt,val)
        elif isinstance(val,int):
            setattr(obj,"_field%s"%self.cnt,val)
        else:
            raise ValueError("IntField need @int")
      

    
class AutoIncrement(IntField):
    def createstr(self):
        return  self.name+ " INTEGER PRIMARY KEY"
    
    def __set__(self,obj,val):
        raise ValueError('AutoIncrement shouldent manul set')
    
    def setvalue(self,obj,val):
        setattr(obj,"_field%s"%self.cnt,val)


class DateField(CharField):
    
    def todb(self,obj):
        if obj is None:
            return 'NULL'
        assert isinstance(obj,date)
        return obj.strftime("'%Y/%m/%d'")
    
    def __set__(self, obj, val):
        if val is None:
            setattr(obj,"_field%s"%self.cnt,val)
        elif isinstance(val,(str,unicode)):
            val=datetime.strptime(val,"%Y/%m/%d").date()
            setattr(obj,"_field%s"%self.cnt,val)
        elif isinstance(val,date):
            setattr(obj,"_field%s"%self.cnt,val)
        else:
            raise ValueError("DateField need assign @date or @date_string or @None")

