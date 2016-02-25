# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
from math import sqrt
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix
# 科学技術計算のためのライブラリscipy

# 映画名の読み込んでディクショナリを作る
def loadMovieLens_movies(path):
    movies = {}
    for line in open(path, encoding="ISO-8859-1"):
        # 文字列を分割しリストを返すsplit関数
        # [n:m]でn番目からm-1番目まで取り出すことができる
        (id,title)=line.split('|')[0:2]
        movies[int(id)]=title
    return movies

def loadMovieLens_prefs(path):
    # 嗜好データの読み込み
    prefs = {}
    max_user = 0
    max_movieid = 0
    for line in open(path):
        (user,movieid,rating,timestamp) = line.split("\t")
        prefs.setdefault(user,{})
        prefs[user][movieid]=rating
        if int(user) > int(max_user):
            max_user = int(user)
        if int(movieid) > int(max_movieid):
            max_movieid = int(movieid)
        # 1682個の映画と943人のユーザと少なくとも20の映画評価
    return [prefs,max_user,max_movieid]

def loadMovieLens_uimat(prefs,max_user,max_movieid):
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
    return uimat



# 類似度計算
# ユークリッド距離
def sim_euclid(x,y,uimat):
    # ０で除算してエラーが出ないように１を分母に足した上で逆数をとっている
    # 類似している人ほど距離が小さいので逆数をとって類似しているほど1に近い数字を返す
    dis = sp.spatial.distance.euclidean(uimat[x-1,:],uimat[y-1,:])
    # np.linalg.norm(x,y)でも可
    return 1/(1+dis)

# ピアソン相関係数
def sim_pearson(x,y,uimat):
    # ピアソン相関係数で相関係数rと有意確率p
    r,p = sp.stats.pearsonr(uimat[x-1,:],uimat[y-1,:])
    return r

# cos類似度
def sim_cos(x,y,uimat):
    # 1-cos類似度
    # cos類似度
    return 1-sp.spatial.distance.cosine(uimat[x-1,:],uimat[y-1,:])

# jaccard係数
def sim_jaccard(x,y,uimat):
    return sp.spatial.distance.jaccard(uimat[x-1,:],uimat[y-1,:])

#特定ユーザpersonの類似ユーザotherのなかで上位n人のリスト
def topMatches(prefs, uimat, person, n, similarity):
    scores=[]
    scores=[(similarity(int(person), int(other),uimat),other)
			for other in prefs]
    # 高スコアがリストの最初に来るように並び替える
    # リストにのみ定義されている昇順に並べ替えるsortと逆順に並べ替えるreverse
    scores.sort()
    scores.reverse()
    return scores[0:n]

# アイテムの推薦
# person以外のユーザの評点の重み付き平均を使い、personへの推薦を算出する
def getRecommendations(prefs,topMatchSU,person):
    totals={}
    simSums={}
    #嗜好が類似しているピアユーザに対して
    for sim,other in topMatchSU.items():
        for movieid in prefs[other]:
            if sim<=0: continue
            # まだ見ていない映画のスコアのみを算出
            if movieid not in prefs[str(person)] or prefs[str(person)][movieid]==0:
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



movies=loadMovieLens_movies(path="./data/u.item")

# prefs,max_user,max_movieid=loadMovieLens_prefs(path="./data/u.data")
# uimat=loadMovieLens_uimat(prefs,max_user,max_movieid)
# topMatchSU=dict(topMatches(prefs, uimat, 30 , 4, sim_pearson))
# UCFRecommendation=getRecommendations(prefs, topMatchSU, 30)
# print(UCFRecommendation)

prefs,max_user,max_movieid=loadMovieLens_prefs(path="./data/100kcross/u1.base")
uimat=loadMovieLens_uimat(prefs,max_user,max_movieid)
te1prefs,max_te1user,max_te1movieid=loadMovieLens_prefs(path="./data/100kcross/u1.test")



# user=30
# totals={}
# simSums={}
# # 変化させるのは近傍
# topMatchSU=dict(topMatches(prefs, uimat, user, 5, sim_pearson))
# rankings=getRecommendations(prefs, topMatchSU, user)
# for (sim,movieid) in rankings:
#     if movieid in te1prefs[str(user)]:
#         s=abs(float(te1prefs[str(user)][movieid])-sim)
#         totals.setdefault(user,0)
#         totals[user]+=s
#         simSums.setdefault(user,0)
#         simSums[user]+=1
# pNMAE=totals[user]/simSums[user]
# NMAE=+pNMAE
# print(NMAE)

for user in te1prefs:
    totals={}
    simSums={}
    # 変化させるのは近傍
    topMatchSU=dict(topMatches(prefs, uimat, user, 5, sim_pearson))
    rankings=getRecommendations(prefs, topMatchSU, user)
    for (sim,movieid) in rankings:
        if movieid in te1prefs[str(user)]:
            s=abs(float(te1prefs[str(user)][movieid])-sim)
            totals.setdefault(user,0)
            totals[user]+=s
            simSums.setdefault(user,0)
            simSums[user]+=1
    pNMAE=totals[user]/simSums[user]
    NMAE=+pNMAE
NMAE=NMAE/max_user
print(NMAE)

# print(rankings)
# リストの要素取り出し！
# ranking_inv = {v:k for (k,v) in rankings}
# print(ranking_inv)

# # 各ユーザについて8:2の交差検定
# tr1prefs,max_tr1user,max_tr1movieid=loadMovieLens_prefs(path="./data/100kcross/u1.base")
# tr1uimat=loadMovieLens_uimat(tr1prefs,max_tr1user,max_tr1movieid)
#
# topMatchSU=dict(topMatches(tr1prefs, tr1uimat, 30, 20, sim_pearson))
# UCFRecommendation=dict(getRecommendations(tr1prefs, topMatchSU, 30))
# print(UCFRecommendation)
#
# te1prefs,max_te1user,max_te1movieid=loadMovieLens_prefs(path="./data/100kcross/u1.test")
# te1uimat=loadMovieLens_uimat(te1prefs,max_te1user,max_te1movieid)
# # 943と462


# #これはまわった
# print(prefs['1'])
# def maketestprefs(prefs):
#     for x in range (1):
#         for user in prefs:
#             prefs[user].popitem()
#     return prefs
# newprefs=maketestprefs(train1prefs)
# print(newprefs['1'])

# #　これもまわった
# print(pretest1prefs['1'])
# for x in range (10):
#     pretest1prefs['1'].popitem()
# print(pretest1prefs['1'])

# print(prefs['1'])
#
# for user in prefs:
#     for x in range (10):
#         prefs[user].popitem()
#
# print(prefs['1'])


# print(prefs['1'])
# # print(pretest1prefs['1'])
#
# # def maketestprefs(prefs):
# #     for x in range (10):
# #         for user in prefs:
# #             prefs[user].popitem()
# #     return prefs
#
# # newprefs=maketestprefs(pretest1prefs)
#
# print(newprefs['1'])
# # sinprefs=maketestprefs(pretest1prefs)
# # maketestprefs(prefs)


# train2prefs,train2uimat,max_train2user,max_train2movieid=loadMovieLens_prefs(path="./data/100kcross/u2.base")
# pretest2prefs,pretest2uimat,max_pretest2user,max_pretest2movieid=loadMovieLens_prefs(path="./data/100kcross/u2.test")
# # 943と658
# train3prefs,train3uimat,max_train3user,max_train3movieid=loadMovieLens_prefs(path="./data/100kcross/u3.base")
# pretest3prefs,pretest3uimat,max_pretest3user,max_pretest3movieid=loadMovieLens_prefs(path="./data/100kcross/u3.test")
# # 943と877
# train4prefs,train4uimat,max_train4user,max_train4movieid=loadMovieLens_prefs(path="./data/100kcross/u4.base")
# pretest4prefs,pretest4uimat,max_pretest4user,max_pretest4movieid=loadMovieLens_prefs(path="./data/100kcross/u4.test")
# # 943と943
# train5prefs,train5uimat,max_train5user,max_train5movieid=loadMovieLens_prefs(path="./data/100kcross/u5.base")
# pretest5prefs,pretest5uimat,max_pretest5user,max_pretest5movieid=loadMovieLens_prefs(path="./data/100kcross/u5.test")
# # 943と943


#ディクショナリは順番決まってないからpopitemで先頭取り出すはつまりランダム！

# popitem
# popitem(prefs['1'].popitem())



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
