#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 12:05:44 2020

@author: nathan
"""

from itertools import combinations


def lcs_combstr(a, b):
    both = (a[i:j] for i, j in combinations(range(len(a) + 1), 2) if a[i:j] in b)
    return max(both, key=len, default="")


def lcs_combset(a, b):
    a = {a[i:j] for i, j in combinations(range(len(a) + 1), 2)}
    a.intersection_update(b[i:j] for i, j in combinations(range(len(b) + 1), 2))
    return max(a, key=len, default="")


def lcs_trie(a, b):
    trie = dict()

    for i in range(len(a) + 1):
        cur_a = trie
        for c in a[i:]:
            cur_a = cur_a.setdefault(c, dict())
            cur_a["#"] = tuple()

    for i in range(len(b) + 1):
        cur_b = trie
        for c in b[i:]:
            cur_b = cur_b.setdefault(c, dict())
            cur_b["$"] = tuple()

    stack = [(trie, "")]
    longest = ""
    while stack:
        cur, sub = stack.pop()
        longest = max(longest, sub, key=len)
        stack.extend(
            (
                val,
                sub + key,
            )
            for key, val in cur.items()
            if "#" in val and "$" in val
        )

    return longest


def lcs_dynamic(a, b):
    m = len(a) + 1
    n = len(b) + 1
    memo = [0] * n

    longest = 0
    index = 0
    for i in range(1, m):
        memo = [0] + [
            memo[j - 1] + 1 if a[i - 1] == b[j - 1] else 0 for j in range(1, n)
        ]
        for i, x in enumerate(memo):
            if x > longest:
                longest = x
                index = i

    return a[index - longest : index]


if __name__ == "__main__":
    import pandas as pd
    from random import choices
    from string import ascii_lowercase as alpha
    from time import time

    algorithms = [lcs_combstr, lcs_combset, lcs_trie, lcs_dynamic]
    df = pd.DataFrame(columns=[algo.__name__ for algo in algorithms])
    for i in range(13):
        a = "".join(choices(alpha, k=2 ** i))
        b = "".join(choices(alpha, k=2 ** i))
        record = pd.Series()
        for algo in algorithms:
            t0 = time()
            print(algo(a, b))
            t1 = time()
            record[algo.__name__] = t1 - t0
        df.loc[2 ** i] = record
