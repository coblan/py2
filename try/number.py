class A(object):
    def say(self):
        print('a say')

class B(object):
    def say(self):
        print('b say')

class C(A,B):
    pass

c=C()
c.say()
print(c.__class__.__mro__)