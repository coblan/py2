# -*- encoding:utf-8 -*-
import numpy as np

def m(x):
    return np.matrix(x)

def run(w,x,d,aita):
    delta=1
    while np.abs(delta)>0.01:
        rt = out(w,x)
        delta=d-rt
        w= learn(w,d,rt,aita,x)
    return w

def out(w,x):
    rt =w*x.T
    return transfer(rt)

@np.vectorize
def transfer(x):
    # adaline的传递函数是1
    return x


def learn(w,d,o,aita,x):
    # 这里是LMS算法
    print(d-o)
    return w+ (aita*(d-o)*x)/(x*x.T) 

if __name__=='__main__':
    x=m([-1,1.2,2.7])    # 样本输入
    w=m([-1,0.5,1.1])
    d=2.3
    aita=0.6
    
    w=run(w,x,d,aita)
    print(w)

