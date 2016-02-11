# -*- coding: utf-8 -*-

# from sklearn import metrics
#
# labels_true = [2.5, 3.5, 3.0, 3.5, 3.0, 2.5]
# labels_pred = [3.0, 3.5, 1.5, 5.0, 3.0, 3.5]
# print(metrics.adjusted_mutual_info_score(labels_true, labels_pred))

# from sklearn import metrics
#
# labels_true = [2.5, 3.5, 3.0, 3.5, 3.0, 2.5]
# labels_pred = [3.0, 3.5, 1.5, 5.0, 3.0, 3.5]
# print(metrics.adjusted_mutual_info_score(labels_true, labels_pred))
# print(metrics.pairwise.euclidean_distances(labels_true, labels_pred))

import numpy as np
import scipy as sp
from math import sqrt
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix

# a = np.array([[11, 12, 13], [21, 22, 23]])
# #print(a.shape)
# print(a[0,1])

prefs = {
    '1': {
        '1': 2.5,
        '2': 3.5,
        '3': 3.0,
        '4': 3.5,
        '5': 2.5,
        '6': 3.0
    },
    '2': {
        '1': 3.0,
        '2': 3.5,
        '3': 1.5,
        '4': 5.0,
        '6': 3.0,
        '5': 3.5
    },
    '3': {
        '1': 2.5,
        '2': 3.0,
        '4': 3.5,
        '6': 4.0
    },
    '4': {
        '2': 3.5,
        '3': 3.0,
        '6': 4.5,
        '4': 4.0,
        '5': 2.5
    },
    '5': {
        '1': 3.0,
        '2': 4.0,
        '3': 2.0,
        '4': 3.0,
        '6': 3.0,
        '5': 2.0
    },
    '6': {
        '1': 3.0,
        '2': 4.0,
        '6': 3.0,
        '4': 5.0,
        '5': 3.5
    },
    '7': {
        '2':4.5,
        '5':1.0,
        '4':4.0
    }
}

uimat = np.zeros((7,6))
for user in prefs:
    for movieid in prefs[user]:
        uimat[int(user)-1,int(movieid)-1]=float(prefs[user][movieid])
print(uimat)

uimat_sparse = csr_matrix(uimat)
print(uimat_sparse)

uimat_dense = uimat_sparse.todense()
print(uimat_dense)
