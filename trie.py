# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 09:45:16 2019

@author: Nathan
"""


from typing import Iterable


class Trie:
    def __init__(self, words: Iterable[str] = tuple()) -> None:
        self.trie = dict()
        for word in words:
            self.insert(word)

    def __contains__(self, word: str) -> bool:
        # Trie contains the given word
        cur = self.trie
        for c in word:
            if c not in cur:
                return False
            cur = cur[c]
        return None in cur

    def insert(self, word: str) -> None:
        # Insert the word in the trie
        cur = self.trie
        for c in word:
            cur = cur.setdefault(c, {})
        cur[None] = None

    def startswith(self, prefix: str) -> bool:
        # Current trie contains the given prefix
        cur = self.trie
        for c in prefix:
            if c not in cur:
                return False
            cur = cur[c]
        return True
