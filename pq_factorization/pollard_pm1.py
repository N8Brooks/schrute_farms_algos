#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 13:30:46 2020

@author: nathan
"""

from math import gcd
from itertools import count
from sympy import isprime
from imath import primegen, ilog, ispower, primes, isqrt
from random import randrange
from functools import reduce
from operator import mul

def pollard_pm1(n, a=2):
    """
    Pollard's p-1 factorization algorithm
    returns a prime factor for n without finding the product of all primes
    """
    if n <= 1: return 1
    if n % 2 == 0: return 2
    if isprime(n): return n
    
    i = 2
    while True:
        a = pow(a, i, n)
        if a == 1: a = randrange(2, n)
        
        d = gcd(a - 1, n)
        if d > 1: return d
        
        i += 1

def pollard_pm2(n, lo=2, hi=4):
    p_gen = primegen()
    p_lo = list()
    p_hi = list()
    p_next = next(p_gen)
    
    while p_next < lo:
        p_lo.append(p_next)
        p_next = next(p_gen)
    
    am1 = 2
    nsqrt = isqrt(n)
    while True:
        a = am1
        for p in p_lo:
            a = pow(a, p, n)
        d = gcd(a - 1, n)
        if 1 < d < n: return d
        am1 = a
        
        while p_next < hi:
            p_hi.append(p_next)
            p_next = next(p_gen)
        
        for p in p_hi:
            a = pow(a, p, n)
        
        d = gcd(a - 1, n)
        if 1 < d < n: return d
        
        lo, hi = hi, hi * 2
        p_lo, p_hi = p_hi, list()