# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
from math import sqrt
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix
# 科学技術計算のためのライブラリscipy



# 映画名の読み込み
movies = {}
for line in open("./data/u.item", encoding="ISO-8859-1"):
    #文字列を分割しリストを返すsplit関数
    #[n:m]でn番目からm-1番目まで取り出すことができる
    (id,title)=line.split('|')[0:2]
    movies[int(id)]=title

# 嗜好データの読み込み
prefs={}
max_user = 0
max_movieid = 0
for line in open("./data/u.data"):
    (user,movieid,rating,timestamp) = line.split("\t")
    prefs.setdefault(int(user),{})
    prefs[int(user)][int(movieid)]=int(rating)
    if int(user) > int(max_user):
        max_user = int(user)
    if int(movieid) > int(max_movieid):
        max_movieid = int(movieid)
    #1682個の映画と943人のユーザ

#配列は1ずつ数がずれているから注意
uimat = np.zeros((int(max_user),int(max_movieid)))
for user in prefs:
    for movieid in prefs[user]:
        uimat[int(user)-1,int(movieid)-1]=int(prefs[user][movieid])

# print(uimat[942,:])




# # クラスタリング
# kmeans = KMeans(n_clusters=20)
# kmeans.fit(mat)
#
#
# clusters = [[] for _ in range(20)]
# for i, label in enumerate(kmeans.labels_):
#     clusters[label].append(movies[i + 1])
#
# # クラスタのサイズ順（昇順）に表示
# clusters = sorted(clusters, key=len)
# for i in range(20):
#     print("-" * 60)
#     for m in clusters[i]:
#         print(m)
