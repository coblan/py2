# -*- encoding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8') 

class Field(object):
    cnt = 0
    def __init__(self,default =''):
        self.cnt=Field.cnt
        Field.cnt+=1
        self.default=default
    def __str__(self):
        return self.default
    
    def create(self):
        return self.name+" text"

class AutoIncrement(Field):
    def create(self):
        return  self.name+ " INTEGER PRIMARY KEY"

class Sqlite(object):
    @staticmethod
    def save(table, dc):
        querystr="INSERT INTO "+table+"("
        for k,v in dc.items():
            querystr+=k+","
        querystr=querystr.rstrip(",")
        querystr+=") VALUES ("
        for k,v in dc.items():
            querystr+= "'%s'"%str(v)+"," 
        querystr=querystr.rstrip(",")
        querystr+=")"
        return querystr
    
    @staticmethod
    def select(model,condition_str):
        querystr="SELECT "
        for k,v in model.fields:
            querystr+=k+','
        querystr=querystr.rstrip(",")
        querystr += " FROM %s %s"%( model.__name__,condition_str)
        return querystr
    
    @staticmethod
    def connection():
        return sqlite3.connect(':memory:')  
    
    @staticmethod
    def create(table):
        querystr = "CREATE TABLE "+table.__name__+"("
        for k,v in table.fields:
            querystr += v.create()+','
        querystr=querystr.rstrip(",")
        querystr+=")"
        return querystr
    @staticmethod
    def update(table,dc,id):
        querystr="UPDATE "+table+" SET "
        for k,v in dc.items():
            querystr+= k+"='%s',"%v
        querystr=querystr.rstrip(",")
        querystr+=" WHERE id=%s"%id
        return querystr
        #UPDATE Person SET Address = 'Zhongshan 23', City = 'Nanjing'
#WHERE LastName = 'Wilson'

        
            

class Meta(type):
    def __init__(cls,cls_name,parents,attr):
        fields =[]
        if hasattr(parents[0],'fields'):
            fields.extend( parents[0].fields)

        for k , v in attr.items():
            if isinstance(v,Field):
                #fields[k]=v
                fields.append((k,v))
                v.name=k
        fields.sort(cmp=lambda x,y: cmp(x[1].cnt , y[1].cnt))
        cls.fields = fields

class Model(object):
    __metaclass__=Meta
    connection=None
    db=Sqlite
    # 添加一个自增
    id = AutoIncrement()
    currentid=None
    def __init__(self,**kw):
        self.__dict__.update(kw)
    
    @classmethod
    def create(cls):
        querystr = cls.db.create(cls)
        cls.cursor.execute(querystr)  
        
    @classmethod
    def connection(cls,conn=None):
        if conn:
            cls.conn=conn
        else:
            cls.conn=cls.db.connection()
        cls.cursor = cls.conn.cursor()
        
    @classmethod
    def commit(cls):
        cls.conn.commit()
        
    @classmethod
    def close(cls):
        cls.conn.close()
    
    def save(self):
        dc = self.get_fields()
        if isinstance(self.id,AutoIncrement):
            savestr=self.db.save(self.__class__.__name__,dc)
            self.cursor.execute(savestr)
            # 如果没有id，把最新的一个id赋予self
            if Model.currentid is None:
                for i in self.select():
                    self.id=i.id
                    Model.currentid =i.id
                    break
            else:
                Model.currentid +=1
                self.id = Model.currentid
        else:
            updatestr=self.db.update(self.__class__.__name__,dc,self.id)
            self.cursor.execute(updatestr)
            
        
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
                setattr(item,k,row[cnt])
                cnt+=1
            yield item


    
#-------------test-------------
if __name__ == '__main__':
    import sqlite3
    class test(Model):
        name = Field()
        age = Field()
        
    test.connection()
    test.create()
    
    tt = test()
    tt.name='heyulin'
    tt.age = 34
    test(name='heyulin',age='18').save()
    tt.save()
    t2 = test(**{"name":'haha',"age":2000})
    t2.save()
    print(t2.name)
    print(t2.id)
    t2.name = 'dog'
    t2.save()
    print(t2.id)
    
    for i in test.select("WHERE id='3'"):
        print(i.name)
    #for i in test.select("WHERE name='heyulin'"):
        #print(i.age)