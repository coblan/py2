from sklearn import cluster, datasets
# iris = datasets.load_iris()
# X_iris = iris.data
# y_iris = iris.target

# k_means = cluster.KMeans(n_clusters=3)
# k_means.fit(X_iris) 

# print(k_means.labels_[::10])

# print(y_iris[::10])

digit = datasets.load_digits()
X_iris = digit.data
y_iris = digit.target

k_means = cluster.KMeans(n_clusters=15)
k_means.fit(X_iris) 

print(k_means.labels_[::10])

print(y_iris[::10])