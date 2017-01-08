# -*- encoding:utf-8 -*-
import numpy as np
import numpy.linalg as l
from matplotlib import pyplot as plt
from pylab import *

def run(v,w,x,d,aita):
    for x_i,d_i in zip(x,d):
        y = transfer(v.dot(x_i))
        o = transfer(w.dot(y))
        d_w=(d_i-o)*o*(1-o)
        d_v=d_w.dot(w)*y*(1-y)
        d_k,y_j=np.meshgrid(y,d_w)
        dlta_w=aita*d_k*y_j
        d_j,x__i=np.meshgrid(x_i,d_v)
        dlta_v=aita*d_j*x__i
        #print(dlta_w)
        w+=dlta_w
        v+=dlta_v
    return w,v


def two_layer(u,v,w,x,d,aita):
    for x_i,d_i in zip(x,d):
        y = transfer(u.dot(x_i))
        z = transfer(v.dot(y))
        o = transfer(w.dot(z))
        
        d_w=(d_i-o)*o*(1-o)
        d_v=d_w.dot(w)*z*(1-z)
        d_u=d_v.dot(v)*y*(1-y)
        
        d_k,z_j=np.meshgrid(z,d_w)
        dlta_w=aita*d_k*z_j
        d_y,y_i=np.meshgrid(y,d_v)
        dlta_v=aita*d_y*y_i
        d_j,x__i=np.meshgrid(x_i,d_u)
        dlta_u=aita*d_j*x__i
        #print(dlta_w)
        w+=dlta_w
        v+=dlta_v
        u+=dlta_u
    return u,v,w


def scale(x):
    return (x-x.min())/(x.max()-x.min())

#@np.vectorize
def transfer(x):
    # adaline的传递函数是1
    return 1/(1+np.exp(-x))


def learn(w,d,o,aita,x):
    # 这里是LMS算法
    print(d-o)
    return w+ (aita*(d-o)*x)/(x*x.T) 



if __name__=='__main__':
    x=np.array([[0.05,0.13,0.08,0.14,0.04],
               [0.065,0.07,0.12,0.16,0.02],
               [0.08,0.19,0.08,0.06,0.],
               [0.095,0.11,0.06,0.16,0.04],
               [0.11,0.05,0.02,0.06,0.02],
               [0.125,0.17,0,0.14,0]])    # 样本输入
    x=scale(x)
    
    d=np.array([0.945,0.8805,0.6025,0.9305,0.9465,0.96])              # 样本输出
    aita=0.6             # 权值修正率
    error=1
    a=[]
    
    #v=np.random.rand(4,5)*2-1
    #w=np.random.rand(1,4)*2-1    

    #while error>0.05:
        #w,v=run(v,w,x,d,aita)
        #rt =transfer(w.dot(transfer(v.dot(x.T))))
        #error=np.sqrt( ((rt-d)**2).sum()/rt.shape[0])
        #a.append(error)

    
    #print(transfer(w.dot(transfer(v.dot(x.T)))))
    
    u=np.random.rand(4,5)*2-1
    v=np.random.rand(2,4)*2-1
    w=np.random.rand(1,2)*2-1     
    while error>0.01:
        u,v,w=two_layer(u,v,w,x,d,aita)
        rt =transfer(w.dot(transfer(v.dot(transfer(u.dot(x.T))))))
        error=np.sqrt( ((rt-d)**2).sum()/rt.shape[1])
        a.append(error) 
         
    print(transfer(w.dot(transfer(v.dot(transfer(u.dot(x.T)))))))
    
    plt.plot(a)
    plt.show()    
