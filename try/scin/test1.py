import numpy as np
from pylab import *

x=np.linspace(0,1,500)
y=-x*np.log2(x)
plt.plot(x,y)
plt.show()
