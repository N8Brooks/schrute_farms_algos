# -*- coding: utf-8 -*-
"""
Modified union_find for number of sets
"""

class union_find:
    def __init__(self, n):
        self.parent = list(range(n))
        self.count = n

    def find(self, x):
        if (self.parent[x] == x):
            return x
        else:
            y = self.find(self.parent[x])
            self.parent[x] = y
            return y
    
    def unite(self, x, y):
        x = self.find(x)
        y = self.find(y)
        
        if x != y: self.count -= 1
        self.parent[x] = y
    
    