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
    1: {
        1: 2.5,
        2: 3.5,
        3: 3.0,
        4: 3.5,
        5: 2.5,
        6: 3.0
    },
    2: {
        1: 3.0,
        2: 3.5,
        3: 1.5,
        4: 5.0,
        6: 3.0,
        5: 3.5
    },
    3: {
        1: 2.5,
        2: 3.0,
        4: 3.5,
        6: 4.0
    },
    4: {
        2: 3.5,
        3: 3.0,
        6: 4.5,
        4: 4.0,
        5: 2.5
    },
    5: {
        1: 3.0,
        2: 4.0,
        3: 2.0,
        4: 3.0,
        6: 3.0,
        5: 2.0
    },
    6: {
        1: 3.0,
        2: 4.0,
        6: 3.0,
        4: 5.0,
        5: 3.5
    },
    7: {
        2:4.5,
        5:1.0,
        4:4.0
    }
}

uimat = np.zeros((7,6))
for user in prefs:
    for movieid in prefs[user]:
        uimat[int(user)-1,int(movieid)-1]=float(prefs[user][movieid])
# print(uimat)
# print(uimat[0,:])

max_user = 7

# #ユークリッド距離
# print(np.linalg.norm(uimat[0,:]-uimat[1,:]))
# print(np.sqrt(np.power(uimat[0,:]-uimat[1,:], 2).sum()))

# # コサイン類似度
# print(sp.spatial.distance.cosine(uimat[0,:],uimat[1,:]))

# ピアソン相関係数で相関係数rと有意確率p
# r,p = sp.stats.pearsonr(uimat[0,:],uimat[1,:])
# print(r)

# # スパース行列と戻す操作
# uimat_sparse = csr_matrix(uimat)
# print(uimat_sparse)
#
# uimat_dense = uimat_sparse.todense()
# print(uimat_dense)

# ユークリッド距離
def sim_euclid(person1, person2):
    # ０で除算してエラーが出ないように1を分母に足した上で逆数をとっている
    # 類似している人ほど距離が小さいので逆数をとって類似しているほど1に近い数字を返す
    dis = sp.spatial.distance.euclidean(person1, person2)
    # np.linalg.norm(person1,person2)でも可
    return 1/(1+dis)

def sim_pearson(person1,person2):
    # ピアソン相関係数で相関係数rと有意確率p
    r,p = sp.stats.pearsonr(person1,person2)
    return r

def sim_pearson2(prefs,p1,p2):
    # 二人とも評価しているアイテムには１が入っているリストsiを得る
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1
    # 要素の数を調べる
    n=len(si)
    # 共に評価しているアイテムがなければ0を返す
    if n==0: return 0
    # すべての嗜好を合計する
    # siに入っている要素itだけループ
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
    # 平方を合計する
    sum1Sq=sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it], 2) for it in si])
    # 積を合計する
    pSum=sum([prefs[p1][it] * prefs[p2][it] for it in si])
    # ピアソンによるスコアを計算する
    # 良い評価をする傾向がある評者でもその二人のスコアの差が一貫していれば完全な相関が取れる
    # -1から1の間の値を返す
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1, 2)/n)*(sum2Sq-pow(sum2, 2)/n))
    if den==0: return 0
    r=num/den
    return r

print(sim_pearson(uimat[6,:],uimat[0,:]))
print(uimat[6,:],uimat[0,:])
print(sim_pearson2(prefs,7,1))
print(prefs[7],prefs[1])

# def topMatches(prefs, person, n=5, similarity=sim_pearson):
#     #リストの定義には[]を使う
# 	scores=[(similarity(prefs,person,other),other)
# 			for other in prefs if other!=person]
# 	# 高スコアがリストの最初に来るように並び替える
#     # リストにのみ定義されている昇順に並べ替えるsortと逆順に並べ替えるreverse
# 	scores.sort()
# 	scores.reverse()
# 	return scores[0:n]

def topMatches2(prefs, person, n=5, similarity=sim_pearson2):
    #リストの定義には[]を使う
	scores=[(similarity(prefs,person,other),other)
			for other in prefs if other!=person]
	# 高スコアがリストの最初に来るように並び替える
    # リストにのみ定義されている昇順に並べ替えるsortと逆順に並べ替えるreverse
	scores.sort()
	scores.reverse()
	return scores[0:n]


# 評者のランキング
# ディクショナリprefsからpersonにもっともマッチするものたち上位ｎ個返す
# 結果の数と類似性関数はオプションのパラメータ
# 推薦対象者以外の人との類似性を求める
def topMatches(prefs, uimat, person, n=3, similarity=sim_pearson):
    #リストの定義には[]を使う
	scores=[(similarity(person, uimat[other-1,:]),other)
			for other in prefs]
	# 高スコアがリストの最初に来るように並び替える
    # リストにのみ定義されている昇順に並べ替えるsortと逆順に並べ替えるreverse
	scores.sort()
	scores.reverse()
	return scores[0:n]

# def topMatches(uimat, person, rank=5, similarity=sim_euclid):
    #リストの定義には[]を使う
	scores=[(similarity(person,uimat[other,:]),other)
			for other in range(max_user-1)]
	# 高スコアがリストの最初に来るように並び替える
    # リストにのみ定義されている昇順に並べ替えるsortと逆順に並べ替えるreverse
	scores.sort()
	scores.reverse()
	return scores[0:rank-1]

tester=[0, 4.5, 0, 4.0, 1.0, 0]

# print(topMatches(prefs, uimat, tester, n=4, similarity=sim_pearson))
# print(topMatches2(prefs, 6, n=4, similarity=sim_pearson2))

mydict = {"a": "amembo", "i": "inu", "u": "usagi"}
mydict_inv = {v:k for k, v in mydict.items()}
print (mydict_inv)
