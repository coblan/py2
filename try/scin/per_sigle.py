import numpy as np

x=[[-1,1,-2,0],
   [-1,0,1.5,-0.5],
   [-1,-1,1,0.5],
   [-1,0,1.5,-0.5],
   [-1,0,1.5,-0.5]]

d=np.matrix([[-1,-1,1,-1,-1],
             [0,1,1,1,1],
             [0,-1,0,-1,-1]])

for i in range(10):
    x.append([-1,0,1.5,-0.5])
    d = np.column_stack((d,[-1,1,-1]))

w=np.matrix([0.5,1,-1,0])
w=np.row_stack((w,w,w))

def run():
    global w
    for k,xi in enumerate(x):
        x_i=np.matrix(xi)
        rt = out(w,x_i)
        w=learn(w,d[:,k],rt,x_i)
        #print(w)
    
def out(w,x):
    rt =w*x.T
    return transfer(rt)

@np.vectorize
def transfer(x):
    if x>=0:
        return 1
    else:
        return -1


def learn(w,d,rt,x):
    print(d-rt)
    return w+ 0.1*(d-rt)*x


run()
print(w*np.matrix(x[2]).T)
