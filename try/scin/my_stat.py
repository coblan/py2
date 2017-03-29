import numpy as np
from scipy import stats

from pylab import plt

x=np.arange(-5,5,0.01)
y=stats.norm.pdf(x,0,2)
plt.plot(x,y)
plt.show()
