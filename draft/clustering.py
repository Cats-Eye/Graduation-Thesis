# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
from math import sqrt
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix
# 科学技術計算のためのライブラリscipy



# 映画名の読み込んでディクショナリを作る
movies = {}
for line in open("./data/u.item", encoding="ISO-8859-1"):
    # 文字列を分割しリストを返すsplit関数
    # [n:m]でn番目からm-1番目まで取り出すことができる
    (id,title)=line.split('|')[0:2]
    movies[int(id)]=title

# 嗜好データの読み込み
prefs = {}
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
    # 1682個の映画と943人のユーザ

# 配列は1ずつ数がずれているから注意
uimat = np.zeros((int(max_user),int(max_movieid)))
for user in prefs:
    for movieid in prefs[user]:
        uimat[int(user)-1,int(movieid)-1]=int(prefs[user][movieid])

# 製品と人物を逆にした転置行列
t_uimat = uimat.T

# スパース行列と戻す操作
uimat_sparse = csr_matrix(uimat)
# uimat_dense = uimat_sparse.todense()

# 類似度計算
# ユークリッド距離
def sim_euclid(person1,person2):
    # ０で除算してエラーが出ないように１を分母に足した上で逆数をとっている
    # 類似している人ほど距離が小さいので逆数をとって類似しているほど1に近い数字を返す
    dis = sp.spatial.distance.euclidean(person1,person2)
    # np.linalg.norm(person1,person2)でも可
    return 1/(1+dis)

# ピアソン相関係数
def sim_pearson(person1,person2):
    # ピアソン相関係数で相関係数rと有意確率p
    r,p = sp.stats.pearsonr(person1,person2)
    return r

# cos類似度
def sim_cos(person1,person2):
    # 1-cos類似度
    # cos類似度
    return -sp.spatial.distance.cosine(person1,person2)+1

# jaccard係数
def sim_jaccard(person1,person2):
    return sp.spatial.distance.jaccard(person1,person2)



def topMatches(prefs, uimat, person, n=3, similarity=sim_pearson):
    #リストの定義には[]を使う
	scores=[(similarity(person, uimat[other-1,:]),other)
			for other in prefs]
	# 高スコアがリストの最初に来るように並び替える
    # リストにのみ定義されている昇順に並べ替えるsortと逆順に並べ替えるreverse
	scores.sort()
	scores.reverse()
	return scores[0:n]


tester=uimat[1,:]

print(topMatches(prefs, uimat, person=tester , n=4, similarity=sim_pearson))




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
