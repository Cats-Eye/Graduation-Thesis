# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans
from scipy import sparse
# 科学技術計算のためのライブラリ

# 嗜好データの読み込み
prefs = []
max_user = 0
max_item = 0
for line in open("./data/u.data"):
    a = line.split("\t")
    user = int(a[0])
    item = int(a[1])
    rate = int(a[2])
    #オブジェクトをリストの最後に追加するappend
    #1行ずつ読み込んでつけたしていく
    prefs.append((user, item, rate))
    # スパース性への対応であとで使う
    if user > max_user:
        max_user = user
    if item > max_item:
        max_item = item

# 疎行列へ変換するScipyのsparce.Lil
# 行列の大きさ、非零の位置とその値を記憶
mat = sparse.lil_matrix((max_item, max_user))
for u, i, r in prefs:
    mat[i - 1, u - 1] = r

print(mat)

# 映画名の読み込み
movies = {}
for line in open("./data/u.item", encoding="ISO-8859-1"):
    a = line.rstrip().split("|")
    movies[int(a[0])] = a[1]

# クラスタリング
kmeans = KMeans(n_clusters=20)
kmeans.fit(mat)

clusters = [[] for _ in range(20)]
for i, label in enumerate(kmeans.labels_):
    clusters[label].append(movies[i + 1])

# クラスタのサイズ順（昇順）に表示
clusters = sorted(clusters, key=len)
for i in range(20):
    print("-" * 60)
    for m in clusters[i]:
        print(m)
