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

class Name(object):
    def __set__(self,obj,val):
        self.val = val
        print(self,obj,val)
    def __get__(self,obj,tp =None):
        print(self,obj,tp)
        return self.val

class person(object):
    name = Name()

p = person()
p.name='haha'

p2=person()
p2.name = "dog"
print( p.name )
print(p2.name)

