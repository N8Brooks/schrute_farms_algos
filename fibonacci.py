# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 14:07:35 2020

@author: DSU
"""

def fib_exp(n):
    # O(1.6180^n)
    return 1 if n < 2 else fib_exp(n-1) + fib_exp(n-2)

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

def fib_log_memo(n, dp={0:1, 1:1}):
    # O(log(n))
    if n in dp:
        return dp[n]
    
    fibj = fib_log_memo(n // 2 - 1, dp)
    fibk = fib_log_memo(n // 2, dp)
    
    if n % 2:
        return dp.setdefault(n, fibk * (2 * fibj + fibk))
    else:
        return dp.setdefault(n, fibk * fibk + fibj * fibj)

def fib_const(n):
    return round(((1 + 5**0.5) / 2) ** (n + 1) / 5**0.5)

if __name__ == '__main__':
    import pandas as pd
    import time
    from tqdm import trange
    
    df = pd.DataFrame()
    
    algorithms = [fib_log_memo, fib_log_free]
    
    for i in trange(32):
        i = 2 ** i
        record = pd.Series(name=i)
        for algo in algorithms:
            start = time.clock()
            algo(i)
            record[algo.__name__] = time.clock() - start
        df[i] = record
    df = df.transpose()
    
    df.plot()