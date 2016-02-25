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
        '1': '2',
        '2': '3',
        '3': '3',
        '4': '3',
        '5': '2',
        '6': '3'
    },
    '2': {
        '1': '3',
        '2': '3',
        '3': '1',
        '4': '5',
        '6': '3',
        '5': '3'
    },
    '3': {
        '1': '2',
        '2': '3',
        '4': '3',
        '6': '4'
    },
    '4': {
        '2': '3',
        '3': '3',
        '6': '4',
        '4': '4',
        '5': '2'
    },
    '5': {
        '1': '3',
        '2': '4',
        '3': '2',
        '4': '3',
        '6': '3',
        '5': '2'
    },
    '6': {
        '1': '3',
        '2': '4',
        '6': '3',
        '4': '5',
        '5': '3'
    },
    '7': {
        '2':'4',
        '5':'1',
        '4':'4'
    }
}

movies = {
    1:'Lady in the Water',
    2:'Snakes on a Plane',
    3:'Just My Luck',
    4:'Superman Returns',
    5:'You, Me and Dupree',
    6:'The Night Listener'
}

uimat = np.zeros((7,6))
for user in prefs:
    for movieid in prefs[user]:
        uimat[int(user)-1,int(movieid)-1]=float(prefs[user][movieid])

max_user = 7

# 類似度計算
# ユークリッド距離
def sim_euclid(x,y):
    # ０で除算してエラーが出ないように１を分母に足した上で逆数をとっている
    # 類似している人ほど距離が小さいので逆数をとって類似しているほど1に近い数字を返す
    dis = sp.spatial.distance.euclidean(uimat[x-1,:],uimat[y-1,:])
    # np.linalg.norm(x,y)でも可
    return 1/(1+dis)

# ピアソン相関係数
def sim_pearson(x,y):
    # ピアソン相関係数で相関係数rと有意確率p
    r,p = sp.stats.pearsonr(uimat[x-1,:],uimat[y-1,:])
    return r

# cos類似度
def sim_cos(x,y):
    # 1-cos類似度
    # cos類似度
    return 1-sp.spatial.distance.cosine(uimat[x-1,:],uimat[y-1,:])

# jaccard係数
def sim_jaccard(x,y):
    return sp.spatial.distance.jaccard(uimat[x-1,:],uimat[y-1,:])

def topMatches(prefs, uimat, person, n, similarity):
    scores=[]
    scores=[(similarity(person, int(other)),other)
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

# topMatchSU={}
# topMatchSU=dict(topMatches(prefs, uimat, 7 , 4, sim_pearson))
# # print(topMatchSU)
# UCFRecommendation=getRecommendations(prefs, topMatchSU, 7)
print (prefs)
print (prefs['1'].popitem())
print (prefs)

# print(UCFRecommendation)
