#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 12:24:55 2020

@author: nathan
"""

from math import gcd
from imath import primes, isqrt, issquare
from itertools import cycle
from functools import reduce
from operator import mul

def trial_division(n):
    """
    returns the lowest prime that divides n
    """
    for p in primes(isqrt(n)):
        if n % p == 0:
            return p
    return n

start = 7
prime_list = [2, 3, 5]
increments = [4, 2, 4, 2, 4, 6, 2, 6]
def wheel(n):
    """
    uses wheel specified by above parameters to factor n
    """
    if n == 0: return 0
    for p in prime_list:
        if n % p == 0: return p
    
    k = start
    i = cycle(increments)
    while k * k <= n:
        if n % k == 0: return k
        k += next(i)
    
    return n

def euler(n):
    """
    uses euler's method to factor n
    """
    for b in range(1, n):
        a2 = n - b * b
        if issquare(a2):
            a = isqrt(a2)
            break
    else: return
    
    for d in range(b + 1, n):
        c2 = n - d * d
        if issquare(c2):
            c = isqrt(c2)
            break
    if a == d: return
    
    A, B, C, D = a - c, a + c, d - b, d + b
    k, h, i, m = gcd(A, C) // 2, gcd(B, D) // 2, gcd(A, D) // 2, gcd(B, C) // 2

    return (k * k + h * h), (i * i + m * m)
    
    
    
    
    
    
    
    
    
    
    