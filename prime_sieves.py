#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 21:51:04 2020

@author: nathan
"""


from heapq import heapreplace, heappush
from itertools import takewhile
from tqdm import trange
import pandas as pd
from time import time
from psutil import virtual_memory
import gc

def isqrt(n):
    """
    returns the sqrt of n rounded down
    also found in the math library of python 3.8+
    """
    if n == 0: return 0
    x, y = n, (n + 1) // 2
    while y < x:
        x, y = y, (y + n // y) // 2
    return x

def eratosthenes1(n):
    """generate the primes less than n using the sieve of eratosthenes."""
    a = [False, False] + [True] * (n - 2)
    for i, isprime in enumerate(a):
        if isprime:
            yield i
            a[i*i:n:i] = [False] * ((n - i * i + i - 1) // i)

def eratosthenes2(n):
    """generate primes less than n using the sieve of eratosthenes odds"""
    if n > 2: yield 2
    n = n // 2 - 1
    # [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, ...]
    a = [False] + [True] * n
    for i in range(isqrt(n) + 1):
        if a[i]:
            i = 2 * i + 1
            j = i * i // 2
            a[j::i] = [False] * ((n - j + i) // i)
    for i, isprime in enumerate(a):
        if isprime:
            yield 2 * i + 1

def eratosthenes6(n):
    """
    generate primes less than n based on 1 and 5 mod 6 integers
    slower than odds only version
    """
    if n > 2: yield 2
    if n > 3: yield 3
    # [1, 5, 7, 11, 13, 17, 19, ...]
    length = n // 6 * 2 + (n % 6 > 1) - 1
    a = [False] + [True] * length
    for i, isprime in enumerate(a):
        if isprime:
            # current integer
            i = 3 * i + i % 2 + 1
            yield i
            j = i * i // 3
            k = j + 4 * i // 3 if i % 6 == 1 else j + 2 * i // 3
            i *= 2
            a[j::i] = [False] * ((length - j + i) // i)
            a[k::i] = [False] * ((length - k + i) // i)

def eratosthenes235(n):
    """
    yields primes less than n using 235 wheel
    """
    if n > 2: yield 2
    if n > 3: yield 3
    if n > 5: yield 5
    if n < 7: return
    modPrms = [7,11,13,17,19,23,29,31]
    gaps = [4,2,4,2,4,6,2,6,4,2,4,2,4,6,2,6] # 2 loops for overflow
    ndxs = [0,0,0,0,1,1,2,2,2,2,3,3,4,4,4,4,5,5,5,5,5,5,6,6,7,7,7,7,7,7]
    lmtbf = (n + 23) // 30 * 8 - 1 # integral number of wheels rounded up
    lmtsqrt = (int(n ** 0.5) - 7)
    lmtsqrt = lmtsqrt // 30 * 8 + ndxs[lmtsqrt % 30] # round down on the wheel
    buf = [True] * (lmtbf + 1)
    for i in range(lmtsqrt + 1):
        if buf[i]:
            ci = i & 7
            p = 30 * (i >> 3) + modPrms[ci]
            s = p * p - 7
            p8 = p << 3
            for ci in range(ci, ci+8):
                c = s // 30 * 8 + ndxs[s % 30]
                buf[c::p8] = [False] * ((lmtbf - c) // p8 + 1)
                s += p * gaps[ci]
    for i in range(lmtbf - 6 + (ndxs[(n - 7) % 30])): # adjust for extras
        if buf[i]:
            yield (30 * (i >> 3) + modPrms[i & 7])

def pyfac_sieve(*n):
    """
    generates primes
    """
    yield 2; yield 3; yield 5; yield 7; yield 11; yield 13;
    sieve = dict()
    ps = pyfac_sieve()
    p = next(ps) and next(ps)
    q = 9
    n = 13
    while True:
        if n in sieve:
            step = sieve.pop(n)
            nxt = n + step
            while nxt in sieve:
                nxt += step
            sieve[nxt] = step
        elif n < q:
            yield n
        else:
            nxt = q + 2*p
            step = 2 * p
            while nxt in sieve:
                nxt += step
            sieve[nxt] = step
            p = next(ps)
            q = p**2
        n += 2
 
def heap_sieve(*n):
    """
    heap implementation of incremental sieve
    """
    nonprimes = list()
    i = 2
    while True:
        if nonprimes and i == nonprimes[0][0]: # non-prime
            while nonprimes[0][0] == i:
                x = nonprimes[0]
                x[0] += x[1]
                heapreplace(nonprimes, x)
 
        else:
            heappush(nonprimes, [i * i, i])
            yield i
        i += 1

def square_sieve(*n):
    """
    faster incremental sieve
    """
    yield 2; yield 3; yield 5; yield 7;
    bps = (p for p in square_sieve())             # separate supply of "base" primes (b.p.)
    p = next(bps) and next(bps)             # discard 2, then get 3
    q = p * p                               # 9 - square of next base prime to keep track of,
    sieve = {}                              #                       in the sieve dict
    n = 9                                   # n is the next candidate number
    while True:
        if n not in sieve:                  # n is not a multiple of any of base primes,
            if n < q:                       # below next base prime's square, so
                yield n                     # n is prime
            else:
                p2 = p + p                  # n == p * p: for prime p, add p * p + 2 * p
                sieve[q + p2] = p2          #   to the dict, with 2 * p as the increment step
                p = next(bps); q = p * p    # pull next base prime, and get its square
        else:
            s = sieve.pop(n); nxt = n + s   # n's a multiple of some b.p., find next multiple
            while nxt in sieve: nxt += s    # ensure each entry is unique
            sieve[nxt] = s                  # nxt is next non-marked multiple of this prime
        n += 2                              # work on odds only

def wheel7(*n):
    for p in [2,3,5,7]: yield p                 # base wheel primes
    gaps1 = [ 2,4,2,4,6,2,6,4,2,4,6,6,2,6,4,2,6,4,6,8,4,2,4,2,4,8 ]
    gaps = gaps1 + [ 6,4,6,2,4,6,2,6,6,4,2,4,6,2,6,4,2,4,2,10,2,10 ] # wheel2357
    def wheel_prime_pairs():
        yield (11,0); bps = wheel_prime_pairs() # additional primes supply
        p, pi = next(bps); q = p * p            # adv to get 11 sqr'd is 121 as next square to put
        sieve = {}; n = 13; ni = 1              #   into sieve dict; init cndidate, wheel ndx
        while True:
            if n not in sieve:                  # is not a multiple of previously recorded primes
                if n < q: yield (n, ni)         # n is prime with wheel modulo index
                else:
                    npi = pi + 1                # advance wheel index
                    if npi > 47: npi = 0
                    sieve[q + p * gaps[pi]] = (p, npi) # n == p * p: put next cull position on wheel
                    p, pi = next(bps); q = p * p  # advance next prime and prime square to put
            else:
                s, si = sieve.pop(n)
                nxt = n + s * gaps[si]          # move current cull position up the wheel
                si = si + 1                     # advance wheel index
                if si > 47: si = 0
                while nxt in sieve:             # ensure each entry is unique by wheel
                    nxt += s * gaps[si]
                    si = si + 1                 # advance wheel index
                    if si > 47: si = 0
                sieve[nxt] = (s, si)            # next non-marked multiple of a prime
            nni = ni + 1                        # advance wheel index
            if nni > 47: nni = 0
            n += gaps[ni]; ni = nni             # advance on the wheel
    for p, pi in wheel_prime_pairs(): yield p   # strip out indexes

def wheel235(*n):
    whlPrms = [2,3,5,7,11,13,17]                # base wheel primes
    for p in whlPrms: yield p
    def makeGaps():
        buf = [True] * (3 * 5 * 7 * 11 * 13 * 17 + 1) # all odds plus extra for o/f
        for p in whlPrms:
            if p < 3:
                continue              # no need to handle evens
            strt = (p * p - 19) >> 1            # start position (divided by 2 using shift)
            while strt < 0: strt += p
            buf[strt::p] = [False] * ((len(buf) - strt - 1) // p + 1) # cull for p
        whlPsns = [i + i for i,v in enumerate(buf) if v]
        return [whlPsns[i + 1] - whlPsns[i] for i in range(len(whlPsns) - 1)]
    gaps = makeGaps()                           # big wheel gaps
    def wheel_prime_pairs():
        yield (19,0); bps = wheel_prime_pairs() # additional primes supply
        p, pi = next(bps); q = p * p            # adv to get 11 sqr'd is 121 as next square to put
        sieve = {}; n = 23; ni = 1              #   into sieve dict; init cndidate, wheel ndx
        while True:
            if n not in sieve:                  # is not a multiple of previously recorded primes
                if n < q: yield (n, ni)         # n is prime with wheel modulo index
                else:
                    npi = pi + 1                # advance wheel index
                    if npi > 92159: npi = 0
                    sieve[q + p * gaps[pi]] = (p, npi) # n == p * p: put next cull position on wheel
                    p, pi = next(bps); q = p * p  # advance next prime and prime square to put
            else:
                s, si = sieve.pop(n)
                nxt = n + s * gaps[si]          # move current cull position up the wheel
                si = si + 1                     # advance wheel index
                if si > 92159: si = 0
                while nxt in sieve:             # ensure each entry is unique by wheel
                    nxt += s * gaps[si]
                    si = si + 1                 # advance wheel index
                    if si > 92159: si = 0
                sieve[nxt] = (s, si)            # next non-marked multiple of a prime
            nni = ni + 1                        # advance wheel index
            if nni > 92159: nni = 0
            n += gaps[ni]; ni = nni             # advance on the wheel
    for p, pi in wheel_prime_pairs(): yield p   # strip out indexes


algorithms = [eratosthenes1, eratosthenes2, eratosthenes6, eratosthenes235,
              pyfac_sieve, heap_sieve, square_sieve, wheel7, wheel235, primegen]

def unit_test(n):
    """
    make sure algorithms work
    """
    for i in trange(-1, n):
        x = list(eratosthenes2(n))
        for algo in algorithms:
            assert x == list(takewhile(lambda x: x < n, algo(n)))

if __name__ == '__main__':
    df_memory = pd.DataFrame(columns = [algo.__name__ for algo in algorithms])
    df_speed = pd.DataFrame(columns = [algo.__name__ for algo in algorithms])
    
    for i in trange(9):
        i = 10**i
        record_memory = pd.Series(name=i)
        record_speed = pd.Series(name=i)
        
        for algo in algorithms:
            gc.collect()
            t0 = time()
            m0 = virtual_memory()[3]
            ps = algo(i)
            for _ in takewhile(lambda x: x < i, ps):
                pass
            m1 = virtual_memory()[3]
            t1 = time()
            record_memory[algo.__name__] = (m1 - m0)/(1024**2)
            record_speed[algo.__name__] = t1 - t0
            try:
                next(ps)
            except:
                pass
        
        df_memory.loc[i] = record_memory
        df_speed.loc[i] = record_speed












