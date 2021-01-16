# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 09:45:16 2019

@author: Nathan
"""


class Trie:
    def __init__(self):
        self.trie = dict()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        cur = self.trie
        for c in word:
            cur = cur.setdefault(c, dict())
        cur[True] = None

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        cur = self.trie
        for c in word:
            if c not in cur:
                return False
            cur = cur[c]
        return True in cur

    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        cur = self.trie
        for c in prefix:
            if c not in cur:
                return False
            cur = cur[c]
        return True
