import numpy as np

def comptition(w,x,aita):
    for x_i in x:
        o=w.dot(x_i)
        i=o.argmax()
        w[i]+=aita*(x_i-w[i])
        w[i]=norm_one(w[i])
    
    for w_i in w:
        print(np.arctan(w_i[1]/w_i[0])*180/np.pi)
    

def norm_one(x):
    ''
    if x.ndim==1:
        return x/np.linalg.norm(x)
    else:
        o =1/np.linalg.norm(x,axis=1)
        o=o.reshape(-1,1)
        return x*o

if __name__=='__main__':
    x=np.array([[0.8,0.6],
                [0.1736,-0.9848],
                [0.707,0.707],
                [0.342,-0.9397],
                [0.6,0.8]])
    
    x=norm_one(x)
    w=np.array([[1,0],
                [-1,0]])
    w=norm_one(w)
    aita=0.5
    
    for i in range(20):
        comptition(w, x, aita)