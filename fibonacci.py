# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 14:07:35 2020

@author: DSU
"""


def fib_exp(n):
    # O(1.6180^n)
    return 1 if n < 2 else fib_exp(n - 1) + fib_exp(n - 2)


def fib_dyn(n):
    # O(n)
    memo = [1, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        memo[i] = memo[i - 1] + memo[i - 2]
    return memo[-1]


def fib_lin(n):
    # O(n)
    a = b = 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def fib_log_free(n):
    # O(log(n))
    if n < 2:
        return 1

    fibj = fib_log_free(n // 2 - 1)
    fibk = fib_log_free(n // 2)

    if n % 2:
        return fibk * (2 * fibj + fibk)
    else:
        return fibk * fibk + fibj * fibj


def fib_log_memo(n, dp={0: 1, 1: 1}):
    # O(log(n)) ... kind of
    if n in dp:
        return dp[n]

    fibj = fib_log_memo(n // 2 - 1, dp)
    fibk = fib_log_memo(n // 2, dp)

    if n % 2:
        return dp.setdefault(n, fibk * (2 * fibj + fibk))
    else:
        return dp.setdefault(n, fibk * fibk + fibj * fibj)


def fib_log_knap(n):
    # knapsack to find relevent fibonacci indexes
    keys = cur = {n}
    for _ in range(n.bit_length() + 1):
        cur = {x // 2 for x in cur} | {x // 2 - 1 for x in cur}
        keys.update(cur)
    keys.difference_update(range(-2, 2))

    # calculate fibonacci for each index
    dp = {0: 1, 1: 1}
    for n in sorted(keys):
        if n - 2 in keys and n - 1 in keys:
            dp[n] = dp[n - 2] + dp[n - 1]
        else:
            fibj = dp[n // 2 - 1]
            fibk = dp[n // 2]
            dp[n] = fibk * (2 * fibj + fibk) if n % 2 else fibk * fibk + fibj * fibj
    return dp[n]


def fib_const(n):
    # O(1) ... kind of
    return round(((1 + 5 ** 0.5) / 2) ** (n + 1) / 5 ** 0.5)


if __name__ == "__main__":
    import pandas as pd
    from time import time
    from tqdm import trange

    algorithms = [fib_log_memo, fib_log_free, fib_log_knap]

    df = pd.DataFrame(columns=[algo.__name__ for algo in algorithms])
    pbar = trange(0, 32)
    for i in pbar:
        i = 2 ** i
        pbar.desc = str(i)
        pbar.refresh()
        record = pd.Series(name=i)
        for algo in algorithms:
            start = time()
            algo(i)
            record[algo.__name__] = time() - start
        df.loc[i] = record
    df = df.transpose()

    df.plot()
