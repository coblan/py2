import numpy as np

x=[[-1,1,-2,0],     # 样本输入
   [-1,0,1.5,-0.5],
   [-1,-1,1,0.5]]

d=np.matrix([[-1,-1,1]])  # 样本输出
w=np.matrix([0.5,1,-1,0])  # 初始w

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
    # 模拟sign函数，向量化是考虑到输入节点是多个的情况，这时x是一个向量
    if x>=0:
        return 1
    else:
        return -1


def learn(w,d,o,x):
    # 这里就是简单的LMS学习算法
    print(d-o)
    return w+ 0.1*(d-o)*x

if __name__=='__main__':
    run()
    print(w)

    w=np.matrix([0.2,0.5,-1,0])  #重新置w的值，再计算
    run()
    print(w)
    
