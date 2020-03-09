# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:28:50 2020

@author: DSU
"""

from functools import reduce
from operator import mul
from itertools import combinations
from math import gcd

def xgcd(a, b):
    """extended greatest common divisor"""
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

def lcm(a, b):
    """least common multiple"""
    """return the lowest integer which both a and b divide"""
    return abs(a * b) // gcd(a, b)

def is_prime(n):
    """return if n is prime"""
    # return if it is 2 or 3
    if n < 4: return n > 1
    # cut down on iteration checking 2s and 3s
    if n % 2 == 0 or n % 3 == 0: return False
    # check other cases
    return all(n % i and n % (i + 2) for i in range(5, int(n ** 0.5) + 1, 6))

def prime_sieve(n):
    """generate the primes less than n using the sieve of eratosthenes."""
    a = [False, False] + [True] * (n - 2)
    for i, isprime in enumerate(a):
        if isprime:
            yield i
            for j in range(i**2, n, i):
                a[j] = False

def factor(n):
    """return all prime factors of int n - does not include 1 and itself"""
    ret = dict()
    for prime in prime_sieve(int(n ** 0.5) + 1):
        power = 0
        while not n % prime:
            power += 1
            n //= prime
        if power:
            ret[prime] = power
    if n > 1:
        ret[n] = 1
    return ret

def divisors(n):
    """return all divisors of integer n"""
    factors = list()
    original = (1, n,)
    for prime in prime_sieve(int(n ** 0.5) + 1):
        while not n % prime:
            n //= prime
            factors.append(prime)
    if n > 1:
        factors.append(n)
    return {reduce(mul, x) for i in range(1, len(factors)) \
            for x in combinations(factors, i)}.union(original)

def inverse_mod(a, m):
    """return x such that a * x is congruent to 1 (mod m)"""
    """can also be solved with xgcd(m, a)[2] or xgcd(a, m)[1]"""
    a = a % m
    return next((x for x in range(1, m) if a * x % m == 1), 1)

def crt(r, m):
    """chinese remainder theorem"""
    """return x such that x = r (mod m) for all a and n"""
    total = 0
    prod = reduce(mul, m)
    for n_i, a_i in zip(m, r):
        p = prod // n_i
        total += a_i * xgcd(n_i, p)[2] * p
    return total % prod

def bsgs(g, r, p):
    """baby step giant step algorithm"""
    """return x such that g^x = r (mod p)"""
    n = int((p-1) ** 0.5) + 1
    u = xgcd(p, pow(g, n, p))[2] % p
    
    def powers(base, multiplier):
        yield base
        for _ in range(n):
            base = base * multiplier % p
            yield base
    
    list1 = {tmp:i for i, tmp in enumerate(powers(1, g))}
    list2 = enumerate(powers(r,u))
    
    return next(list1[tmp] + j * n for j, tmp in list2 if tmp in list1)

def pha(g, r, p):
    """pohlig-hellman algorithm"""
    """return x such that g^x = r (mod p)"""
    u = p - 1
    ms = [base**exp for base, exp in factor(u).items()]
    rs = [bsgs(pow(g, x, p), pow(r, x, p), p) for x in map(lambda x: u//x, ms)]
    return crt(rs, ms)



















