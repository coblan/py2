# -*- encoding:utf8 -*-

#class p(object):
    #def __new__(cls,name):
        #print('new')
        #print(cls)
        #return object.__new__(cls,name)
    #def __init__(self,name):
        #print('init')
        #self.name = name
    
#a= p('jj')
#print(a.name)

# ----------------------------------------------------------------------------------------
#class myMeta(type):
    #def __new__(cls_meta, future_class_name, future_class_parents, future_class_attr):
        #print('-'*30)
        #print(cls_meta)
        #print(future_class_name)
        #print(future_class_parents)
        #print(future_class_attr)
        
        #return type.__new__(cls_meta,future_class_name, future_class_parents, future_class_attr)
    #def __init__(cls,future_class_name, future_class_parents, future_class_attr):
        #print('*'*30)
        #print(cls)
        #print(future_class_name)
        #print(future_class_parents)
        #print(future_class_attr)
        

#class me(object):
    #__metaclass__=myMeta
    #age = 100

#print( me().__dict__)
# ------------------------描述器
#class Name(object):
    #def __set__(self,obj,val):
        #self.val = val
        #print(self,obj,val)
    #def __get__(self,obj,tp =None):
        #print(self,obj,tp)
        #return self.val
    #def tostr(self,obj):
        #return obj

#class person(object):
    #name = Name()

#print(person.name)
#p = person()
#p.name='haha'

#p2=person()
#p2.name = "dog"
#print( p.name )
#print(p2.name)


#print('\u00e5\u00ae\u00b9')

#import memcache
    
#_mc = memcache.Client(['127.0.0.1:11211'],debug=0)  
#class __MC(object):
    #def __setattr__(self,name,value):
        #_mc.set(name,value)
    #def __getattr__(self,name):
        #obj = _mc.get(name)
        #if isinstance(obj,list):
            #return _proxy(obj)
        #else:
            #return _mc.get(name)
        
#class _proxy(object):
    #def __init__(self,ls):
        #self.ls=ls
    #def __getattr__(self,name):
        #def func(*args,**kw):
            #ls =self.ls
            #getattr(ls,name)(*args,**kw)
            #self.ls=ls
        #return func
        
#gd=__MC()    

#gd.mm='ri'
#print(gd.mm)
#gd.ls=[]
##ls=gd.ls
##ls.append('haha')
##gd.ls=ls
#gd.ls.append('haha')

#print(gd.ls)
ls = []
print(ls.append('kk'))

# <<<<<<< HEAD
# # print('\u00e5\u00ae\u00b9')

# from string import Template
# class MyTemp(Template):
    # delimiter ='$$'

# s = 'hello $${name} mornint'
# j=MyTemp(s).safe_substitute({'name':'dog'})
# print(j)
# =======
# #print('\u00e5\u00ae\u00b9')
# >>>>>>> 849aab8be0d096ec7df42667da9a697e06e54590

# ls =('dog','pig')
# ls +=('jj',)
# print(ls)

# import base64
# p = base64.b64encode('中国')
# print(p)

def func(name,**kw):
    print(name)
    
dc ={'name':'dog','age':18}

func(**dc)
print(dir(func))
print(func.func_globals)
help(func)

