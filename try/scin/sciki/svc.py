# encoding:utf-8

from sklearn import svm
from sklearn import datasets
digits = datasets.load_digits()

# 应该是 软间隔分类
clf = svm.SVC(gamma=0.001, C=100)
clf.fit(digits.data[:-1], digits.target[:-1])  
print(clf.predict(digits.data[-1:]))