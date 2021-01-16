# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 09:45:16 2019

@author: Nathan
"""


class union_find:
    """ simple union find """

    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        return x if self.parent[x] == x else self.find(self.parent[x])

    def unite(self, x, y):
        self.parent[self.find(x)] = self.find(y)


class union_find_count:
    """ union find that maintains count of groups """

    def __init__(self, n):
        self.parent = list(range(n))
        self.count = n

    def find(self, x):
        return x if self.parent[x] == x else self.find(self.parent[x])

    def unite(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x != y:
            self.count -= 1
        self.parent[x] = y


class union_find_dict:
    """ union find that uses dictionary """

    def __init__(self):
        self.parent = dict()

    def find(self, x):
        if self.parent.setdefault(x, x) == x:
            return x
        else:
            return self.find(self.parent[x])

    def unite(self, x, y):
        self.parent[self.find(x)] = self.find(y)


class union_find_dict_count:
    """ union find that maintains group count with dictionary """

    def __init__(self):
        self.parent = dict()
        self.count = 0

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.count += 1
            return x
        elif self.parent[x] == x:
            return x
        else:
            return self.find(self.parent[x])

    def unite(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x != y:
            self.count -= 1
        self.parent[x] = y
