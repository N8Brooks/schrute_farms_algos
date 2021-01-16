#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 11:18:33 2020

@author: nathan
"""

def isqrt(n):
    """
    return greatest x such that x^2 <= n
    """
    if n == 0: return 0
    x = n
    y = (n + 1) // 2
    while y < x:
        x = y
        y = (y + n // y) // 2
    return x

def iroot(n, r=2):
    """
    return greatest x such that x^r <= n
    """
    if n < 0: return -iroot(-n, r) if r % 2 else None
    if n < 2: return n
    if r == 2: return isqrt(n)
    lo, hi = 0, n
    while lo < hi:
        mi = (lo + hi) // 2
        if mi**r > n: hi = mi
        else: lo = mi + 1
    return hi - 1

def ilog(n, b):
    """
    returns the greatest x such that b^x <= n
    """
    l = 0
    while n >= b:
        n //= b
        l += 1
    return l

def ispower(n):
    """
    returns base b where b^x == n
    returns 0 if it is not a power
    """
    for p in primegen():
        r = iroot(n, p)
        if r is None: continue
        if r ** p == n: return r
        if r == 1: return 0

def legendre(a, p):
    """ legendre symbol """
    return pow(a % p, (p - 1) // 2, p)

def mod_sqrt(n, p):
    """
    modular sqrt where p is prime
    p - return for other square root
    """
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p + 1):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

def quadratic_residue(n):
    """squares modulo n"""
    return {i * i % n for i in range(n // 2 + 1)}

squares = quadratic_residue(720720)
def issquare(n):
    """
    fast function to find if n is a perfect square using quadratic residue
    720720 is hard coded in - other numbers that work well are superior highly
    composite numbers - you could also have several stages of powers of primes
    """
    return n % 720720 in squares and isqrt(n)**2 == n

def primegen():
    """
    infinite incremental sieve of eratosthenes with 235 wheel
    """
    whlPrms = [2,3,5,7,11,13,17]
    for p in whlPrms:
        yield p
    
    # generate gaps
    buf = [True] * (3 * 5 * 7 * 11 * 13 * 17 + 1)
    for p in whlPrms:
        if p < 3:
            continue
        strt = (p * p - 19) >> 1
        while strt < 0:
            strt += p
        buf[strt::p] = [False] * ((len(buf) - strt - 1) // p + 1)
    whlPsns = [i + i for i,v in enumerate(buf) if v]
    gaps = [whlPsns[i + 1] - whlPsns[i] for i in range(len(whlPsns) - 1)]
    
    def wheel_prime_pairs():
        yield 19, 0
        bps = wheel_prime_pairs()
        p, pi = next(bps)
        q = p * p
        sieve = dict()
        n = 23
        ni = 1
        while True:
            if n not in sieve:
                if n < q:
                    yield n, ni
                else:
                    npi = pi + 1
                    if npi > 92159:
                        npi = 0
                    sieve[q + p * gaps[pi]] = (p, npi)
                    p, pi = next(bps)
                    q = p * p
            else:
                s, si = sieve.pop(n)
                nxt = n + s * gaps[si]
                si = si + 1
                if si > 92159:
                    si = 0
                while nxt in sieve:
                    nxt += s * gaps[si]
                    si = si + 1
                    if si > 92159:
                        si = 0
                sieve[nxt] = (s, si)
            nni = ni + 1
            if nni > 92159:
                nni = 0
            n += gaps[ni]
            ni = nni
    
    for p, _ in wheel_prime_pairs():
        yield p

def primes(n):
    """
    yields primes less than  or equal to n using 235 wheel
    """
    if n >= 2: yield 2
    if n >= 3: yield 3
    if n >= 5: yield 5
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
        if buf[i]: yield (30 * (i >> 3) + modPrms[i & 7])

