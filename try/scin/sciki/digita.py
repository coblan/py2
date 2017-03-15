
from sklearn import svm
from sklearn import datasets
import matplotlib.pyplot as plt 

digits = datasets.load_digits()

plt.imshow(digits.images[-1])
data = digits.images.reshape((digits.images.shape[0], -1))
digits.images