# encoding:utf-8

class a(object):
    def say(self):
        print('jj')

class b(a):
    pass

bb=b()
print hasattr(bb,'say')