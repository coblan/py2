
from sklearn import svm
from sklearn import datasets
iris = datasets.load_iris()

clf = svm.SVC()
clf.fit(iris.data,iris.target)
print(clf)