import numpy as np
cc=np.array([[1,2,3],
             [2,5,7],
             [7,3,9]])
print(cc)
print(cc.shape)
bb=np.array([1,2,3,4,5,6])
dd=bb.reshape(2,3)

print(np.linalg.inv(cc))
bb=np.matrix(cc)
print(bb.I)
print(bb.T)
print(np.dot(cc,np.linalg.inv(cc)))
print(bb*bb.I)