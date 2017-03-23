# encoding:utf-8

import numpy as np
from numpy import linalg as lin

a=np.array(np.linspace(1,100,90))
b = a.reshape(10,9)
u,s,v=lin.svd(b)
print(s)

# b 约= u[:,:2] x s[2] x v[:2,:]
