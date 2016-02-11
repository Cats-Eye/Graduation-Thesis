# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans

def main():

    _items = []
    _f = open('./u.data' )
    _lines = _f.readlines()

    for _line in _lines:
        _items.append(_line.split(','))

    _f.close()

    km = KMeans(init='k-means++')
    km.fit(_items)

    print(km.labels_)


if __name__ == '__main__':
    main()
