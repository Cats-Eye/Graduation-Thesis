# -*- coding: utf-8 -*-

from math import sqrt

# criticsというディクショナリを作成。複数の要素を管理するデータ型。見出し語と対応する要素を紐付け管理
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5
    },
    'Toby': {
        'Snakes on a Plane':4.5,
        'You, Me and Dupree':1.0,
        'Superman Returns':4.0
    }
}



# ユークリッド距離
# person1とperson2の距離をもとにした類似性スコアを返す
def sim_distance(prefs,person1,person2):
	# 二人とも評価しているアイテムには１が入っているリストsiを得る
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

	# 両者共に評価しているものが一つもなければ0を返す
    # 文字列の長さ、要素数を返すlen関数
    if len(si)==0: return 0

	# すべての差の平方を足し合わせる
    # 累乗を返すpow関数
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
						for item in prefs[person1] if item in prefs[person2]])

	# sqrtで平方根を計算
    # ０で除算してエラーが出ないように１を分母に足した上で逆数をとっている
    # 類似している人ほど距離が小さいので逆数をとって類似しているほど1に近い数字を返す
    return 1/(1+sqrt(sum_of_squares))



# ピアソン相関係数
# p1とp2のピアソン相関係数を返す
def sim_pearson(prefs,p1,p2):
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



# 評者のランキング
# ディクショナリprefsからpersonにもっともマッチするものたちを返す
# 結果の数と類似性関数はオプションのパラメータ
# 推薦対象者以外の人との類似性を求める
def topMatches(prefs, person, n=5, similarity=sim_pearson):
	scores=[(similarity(prefs,person,other),other)
			for other in prefs if other!=person]

	# 高スコアがリストの最初に来るように並び替える
    # リストにのみ定義されている昇順に並べ替えるsortと逆順に並べ替えるreverse
	scores.sort()
	scores.reverse()
	return scores[0:n]



# アイテムの推薦
# person以外の全ユーザの評点の重み付き平均を使い、personへの推薦を算出する
def getRecommendations(prefs,person,similarity=sim_pearson):
	totals={}
	simSums={}
	for other in prefs:

		# 自分自身とは比較しない
        # for文やwhile文でそれ以降の処理を行わないcontinue
		if other==person: continue

		sim=similarity(prefs,person,other)

        #０以下のスコアは無視する
		if sim<=0: continue

		for item in prefs[other]:
			# まだ見ていない映画の特典のみを算出
			if item not in prefs[person] or prefs[person][item]==0:
				# 類似度 * スコア
                # itemに値があればその値を返すが、itemというキーがなければそのキーを作り０を書き込む
				totals.setdefault(item,0)
                # 他人の評価とその人との類似度の積によるスコアがtotals
				totals[item]+=prefs[other][item]*sim
				# あるアイテムのtotalsに関わった他人の類似度の合計
				simSums.setdefault(item,0)
				simSums[item]+=sim

	# スコアを類似殿合計で割ることで正規化
	rankings=[(total/simSums[item],item) for item,total in totals.items()]

	# ソート済みのリストを返す
	rankings.sort()
	rankings.reverse()
	return rankings



# 類似製品
def transformPrefs(prefs):
	result={}
	for person in prefs:
		for item in prefs[person]:
            # 空の辞書`{}
			result.setdefault(item,{})
			# result[item][person]には評価地を入れる
			result[item][person]=prefs[person][item]
	return result


print(sim_distance(critics,'Lisa Rose','Gene Seymour'))
print(sim_pearson(critics,'Lisa Rose','Gene Seymour'))
print(topMatches(critics,'Toby',n=3))
print(topMatches(critics,'Toby',n=3,similarity=sim_distance))
print(getRecommendations(critics,'Toby'))
print(transformPrefs(critics))
#
