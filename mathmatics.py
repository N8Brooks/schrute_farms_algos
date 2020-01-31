# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:28:50 2020

@author: DSU
"""

from math import gcd

def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

def prime_test(n):
    """return if n is prime"""
    # return if it is 2 or 3
    if n < 4: return n > 1
    
    # cut down on iteration checking 2s and 3s
    if n % 2 == 0 or n % 3 == 0: return False
    
    # check other cases
    return all(n % i and n % (i + 2) for i in range(5, int(n ** 0.5) + 1, 6))

def prime_sieve(n):
    """Generate the primes less than ``n`` using the Sieve of Eratosthenes."""
    a = [True] * n
    a[0] = a[1] = False
    for i, isprime in enumerate(a):
        if isprime:
            yield i
            for j in range(i * i, n, i):
                a[j] = False

def factor(n):
    """return factors of integer n"""
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

    