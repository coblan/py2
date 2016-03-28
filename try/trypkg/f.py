# -*- encoding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

import json
engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()


import sqlalchemy.types as types

class MyType(types.TypeDecorator):
     '''Prefixes Unicode values with "PREFIX:" on the way in and
     strips it off on the way out.
     '''

     impl = types.String

     def process_bind_param(self, value, dialect):
          return json.dumps(value)

     def process_result_value(self, value, dialect):
          return json.loads(value)


class User(Base):
     __tablename__ = 'users'
     id = Column(Integer, primary_key=True)
     name = Column(String)
     fullname = Column(String)
     password = Column(String)
     friends=Column(MyType)

     def __repr__(self):
          return "<User(name='%s', fullname='%s', password='%s')>" % (
                             self.name, self.fullname, self.password)


Base.metadata.create_all(engine)
print(User.__table__)

DBSession = sessionmaker(bind=engine)
session = DBSession()
new_user = User(id='5', name='Bob',friends=[])
new_user.friends.append('jack')
new_user.friends.append('suck')
# 添加到session:
session.add(new_user)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()


# 创建Session:
session = DBSession()
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).filter(User.id=='5').one()
# 打印类型和对象的name属性:
print 'type:', type(user)
print 'name:', user.name
# 关闭Session:
session.close()