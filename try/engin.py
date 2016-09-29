
import weakref
import time
import gc

class big(object):
    def __init__(self):
        self._dog='jj'
        self.data={
            'crt':'update_crt',
            
        }

    def update_crt(self,value):
        print(value)
        
    def dispath(self,key, *arg,**kw):
        func= getattr(self,key,None)
        if func:
            func(*arg,**kw)
        else:
            print(key+ str(arg))

class JJ(object):
    def __init__(self):
        self.data={
            'say': self.say
        }
    def say(self,name):
        print(name)
        
    def dispath(self,key,*arg,**kw):
        self.data.get(key)(*arg,**kw)


class Node(object):
    def __init__(self,obj):
        self.proxy = weakref.ref(obj,self.remove_from_total)
        self.childs=[]
    
    def append(self,obj):
        node = Node(obj)
        totol.append(node)
        self.childs.append(node)
        
    def remove_from_total(self,v):
        totol.remove(self)
    
    def __call__(self):
        return self.proxy()
        
totol=[]

def add_node(child,parent):
    node = get_node(parent)
    
    # todo remove child form total if there has 
    node.append(child)

def get_node(obj):
    ls=[r() for r in totol]
    try:
        index = ls.index(obj)
        return totol[index]
    except ValueError:
        node=Node(obj)
        totol.append(node)
        return node

ls= [] #LIST()

def walk(node,*arg,**kw):
    if not isinstance(node,Node):
        node=get_node(node)
    if node():
        node().dispath(*arg,**kw)
    for child in node.childs:
        if child():
            walk(child,*arg,**kw)
            

def test():
    b1=big()
    b2=big()
    add_node(b2,b1)
    
    del b2
    walk(b1,'update_crt','hello world')
    
    d=JJ()
    add_node(d,b1)
    
    walk(b1,'say','my name dog')
    
    del d
    gc.collect() 
    
    walk(b1,'say','my name dog')


test()

    
    
    

    

    

