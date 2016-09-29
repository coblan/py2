# -*- encoding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8') 
from sqlite import Sqlite
from fields import *

  
class Meta(type):
    def __init__(cls,cls_name,parents,attr):
        fields =[]
        if hasattr(parents[0],'fields'):
            fields.extend( parents[0].fields)

        for k , v in attr.items():
            if isinstance(v,Field):
                fields.append((k,v))
                v.name=k
                v.model=cls_name
        fields.sort(cmp=lambda x,y: cmp(x[1].cnt , y[1].cnt))
        cls.fields = fields

class Model(object):
    __metaclass__=Meta
    db=Sqlite
    # 添加一个自增
    autoId = AutoIncrement()
    currentid=None
    def __init__(self,**kw):
        for k ,v in kw.items():
            setattr(self,k,v)
        #self.__dict__.update(kw)
    
    @classmethod
    def getField(cls,key):
        for k,v in cls.fields:
            if k == key:
                return v
        return None
    
    @classmethod
    def create(cls):
        querystr = cls.db.create(cls)
        cls.cursor.execute(querystr)  
        
    @classmethod
    def connection(cls,conn):
        cls.conn = conn
        cls.cursor = cls.conn.cursor()
        
    @classmethod
    def commit(cls):
        cls.conn.commit()
        
    @classmethod
    def close(cls):
        cls.conn.close()
    
    def save(self):
        dc = self.get_fields()
        try:
            updatestr=self.db.update(self.__class__,dc,self.autoId)
            self.cursor.execute(updatestr)            
            
        except AttributeError:
            #assert isinstance(self.id,AutoIncrement)
            savestr=self.db.save(self.__class__,dc)
            self.cursor.execute(savestr)
            self.commit()
            # 如果没有id，把最新的一个id赋予self
            if Model.currentid is None:
                for i in self.select("ORDER BY autoId"):
                    self.getField('autoId').setvalue(self,i.autoId)
                    Model.currentid =i.autoId
                    break
            else:
                Model.currentid +=1
                self.getField('autoId').setvalue(self,Model.currentid)
                #self.id = Model.currentid            
            
        
    def get_fields(self):
        dc = {}
        for k,v in self.fields:
            if isinstance(v,AutoIncrement):
                continue
            dc[k]=getattr(self,k) 
        return dc
    
    @classmethod
    def select(cls,condition_str=''):
        querystr = cls.db.select(cls,condition_str)
        # 考虑到同时读的问题，每次select 都是一个新的cursor
        cursor = cls.conn.cursor()
        for row in cursor.execute(querystr):
            item = cls()
            cnt = 0
            for k,v in cls.fields:
                if cnt==0:
                    cls.getField('autoId').setvalue(item,row[0])
                else:
                    setattr(item,k,row[cnt])
                cnt+=1
            yield item
    
    @classmethod
    def clear(cls):
        cursor = cls.conn.cursor()
        cursor.execute("DELETE FROM "+cls.__name__)
        Model.currentid = None
    
#-------------test-------------
if __name__ == '__main__':
    import sqlite3
    from heOs.mytime import Time
    class test(Model):
        name = CharField()
        age = IntField()
        birthday = DateField(NULL=True)
        #time = MyTimeField(NULL=True)
    conn = sqlite3.connect(':memory:')  
    #conn = sqlite3.connect('dog.db') 
    test.connection(conn)
    test.create()
    
    dc = {"name":'heyulin',"age":34}
    tt = test(**dc)

    tt.birthday=datetime.today().date()
    tt.time = Time(5,10)
    tt.save()
    t2 = test(**{"name":'haha',"age":2000})
    t2.save()
    
    print(t2.name)
    print(t2.autoId)
    
    #test.clear()
    tt = test()
    tt.name='heyulin'  
    tt.age =1100
    tt.save()
    print(tt.autoId)
    test.commit()
    
