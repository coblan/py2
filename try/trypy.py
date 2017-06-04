# encoding:utf-8

class A(object):
    name='pig'
    @staticmethod
    def fuck():
        name='dog'
        
    @staticmethod
    def say():
        print(name)

b=A()
b.say()