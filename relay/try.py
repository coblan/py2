import trypk

print(trypk.dog)

class MC(object):
    def set(self,name,value):
        setattr(self,name,value)
    def get(self,name):
        return getattr(self,name)
_mc= MC()

class __MC(object):
    def __setattr__(self,name,value):
        _mc.set(name,value)
    def __getattr__(self,name):
        return _mc.get(name)
gd=__MC()


gd.name='dog'
print(gd.name)
print(gd.age)