# encoding:utf-8

def fun1():
    name='dog'
    return locals()

def fun2():
    dc = locals()
    dc.update(fun1())
    print(name)


fun2()