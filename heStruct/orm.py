class Field(object):
    def __init__(self,default =''):
        self.default=default
    def __str__(self):
        return self.default
#class CharField(Field):
    #pass

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
        for k,v in model.fields.items():
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
        for k in table.fields:
            querystr+=k+" text,"
        querystr=querystr.rstrip(",")
        querystr+=")"
        return querystr
            

class Meta(type):
    def __init__(cls,cls_name,parent,attr):
        fields = {}
        for k , v in attr.items():
            if isinstance(v,Field):
                fields[k]=v
        cls.fields = fields

class Model(object):
    __metaclass__=Meta
    connection=None
    db=Sqlite
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
        savestr=self.db.save(self.__class__.__name__,dc)
        self.cursor.execute(savestr)
        
    def get_fields(self):
        dc = {}
        for k,v in self.fields.items():
            dc[k]=getattr(self,k) 
        return dc
    
    @classmethod
    def select(cls,condition_str=''):
        querystr = cls.db.select(cls,condition_str)
        for row in cls.cursor.execute(querystr):
            item = cls()
            cnt = 0
            for k in cls.fields:
                setattr(item,k,row[cnt])
                cnt+=1
            yield item


    
#-------------test-------------
if __name__ == '__main__':
    import sqlite3
    class TestModel(Model):
        name = Field()
        age = Field()
    TestModel.connection()
    TestModel.create()
    
    tt = TestModel()
    tt.name='heyulin'
    tt.age = 34
    TestModel(name='heyulin',age='18').save()
    tt.save()
    t2 = TestModel(**{"name":'haha',"age":2000})
    t2.save()
    
    for i in TestModel.select("WHERE name='heyulin'"):
        print(i.age)