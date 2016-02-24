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
    prefs.setdefault(user,{})
    prefs[user][movieid]=rating
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
def sim_euclid(x,y):
    # ０で除算してエラーが出ないように１を分母に足した上で逆数をとっている
    # 類似している人ほど距離が小さいので逆数をとって類似しているほど1に近い数字を返す
    dis = sp.spatial.distance.euclidean(x,y)
    # np.linalg.norm(x,y)でも可
    return 1/(1+dis)

# ピアソン相関係数
def sim_pearson(x,y):
    # ピアソン相関係数で相関係数rと有意確率p
    r,p = sp.stats.pearsonr(x,y)
    return r

# cos類似度
def sim_cos(x,y):
    # 1-cos類似度
    # cos類似度
    return -sp.spatial.distance.cosine(x,y)+1

# jaccard係数
def sim_jaccard(x,y):
    return sp.spatial.distance.jaccard(x,y)



def topMatches(prefs, uimat, person, n, similarity=sim_pearson):
    tester=uimat[person-1,:]
    scores=[]
    scores=[(similarity(tester, uimat[int(other)-1,:]),other)
			for other in prefs]
    # 高スコアがリストの最初に来るように並び替える
    # リストにのみ定義されている昇順に並べ替えるsortと逆順に並べ替えるreverse
    scores.sort()
    scores.reverse()
    return scores[0:n]

# アイテムの推薦
# person以外のユーザの評点の重み付き平均を使い、personへの推薦を算出する
def getRecommendations(prefs,topMatchSU,person='30'):
    totals={}
    simSums={}
    #嗜好が類似しているピアユーザに対して
    for sim,other in topMatchSU.items():
        for movieid in prefs[other]:
            if sim<=0: continue
            # まだ見ていない映画のスコアのみを算出
            if movieid not in prefs[person] or prefs[person][movieid]==0:
                totals.setdefault(movieid,0)
                # 他人の評価とその人との類似度の積によるスコアがtotals
                totals[movieid]+=int(prefs[other][movieid]) * sim
                # あるアイテムのtotalsに関わった他人の類似度の合計
                simSums.setdefault(movieid,0)
                simSums[movieid]+= sim
    # スコアを類似度合計で割ることで正規化
    rankings=[(totals[movieid]/simSums[movieid],movieid) for movieid in totals]
    rankings.sort()
    rankings.reverse()
    return rankings

topMatchSU={}
topMatchSU=dict(topMatches(prefs, uimat, person=30 , n=4, similarity=sim_pearson))
UCFRecommendation=getRecommendations(prefs,topMatchSU,person='30')





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
