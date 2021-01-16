#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 12:44:05 2020

@author: nathan
"""

from itertools import count
from math import gcd
from random import randrange
from sympy import isprime
from imath import ispower

def pollard_rho(n):
    """
    return factor of n using pollard's rho algorithm with floyd cycle detection
    """
    if n < 0: return pollard_rho(-n)
    if n % 2 == 0: return 2
    if n == 0 or n == 1 or isprime(n): return n
    d = 1
    x = y = 2
    while True:
        x = (x * x + 1) % n
        y = (y * y + 1) % n
        y = (y * y + 1) % n
        d = gcd(abs(x - y), n)
        if 1 < d < n:
            return d
        else:
            x = randrange(1, n)
            y = randrange(1, n)

def brent_rho(n):
    """
    returns factor of n using pollar rho algorithm with brent cycle detection
    """
    if n < 0: return brent_rho(-n)
    if n == 0 or n == 1 or isprime(n): return n
    g = n
    while g == n:
        y = randrange(1, n)
        c = randrange(1, n)
        m = randrange(1, n)
        g = r = q = 1
        while g == 1:
            x = y
            k = 0
            for i in range(r):
                y = (y * y + c) % n
            while k < r and g == 1:
                ys = y
                for i in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
    
    return g
    
