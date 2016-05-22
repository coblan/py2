# -*- encoding:utf-8 -*-
import numpy as np
import numpy.linalg as l


def run(w,x,d,aita):
    delta=1
    while np.abs(delta)>0.01:
        rt = out(w,x)
        delta=d-rt
        w= learn(w,d,rt,aita,x)
    return w

def out(w,x):
    rt =w.dot(x)
    return transfer(rt)

@np.vectorize
def transfer(x):
    # adaline的传递函数是1
    return x


def learn(w,d,o,aita,x):
    # 这里是LMS算法
    print(d-o)
    return w+ (aita*(d-o)*x)/x.dot(x) 

if __name__=='__main__':
    x=np.array([-1,1.2,2.7])    # 样本输入
    w=np.array([-1,0.5,1.1])    # 初始权值
    d=2.3                # 样本输出
    aita=0.6             # 权值修正率
    
    w=run(w,x,d,aita)
    print(w)

