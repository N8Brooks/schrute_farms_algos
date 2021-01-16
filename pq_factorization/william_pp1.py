#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 15:17:58 2020

@author: nathan
"""

from math import gcd
from imath import ispower, ilog, isqrt, primegen
from itertools import count
from sympy import isprime


def mlucas(b, m, n):
    """
    returns m-th element v of the sequence characterized by b
    """
    x = b
    y = (b * b - 2) % n
    for bit in bin(m)[3:]:
        if bit == "1":
            x = (x * y - b) % n
            y = (y * y - 2) % n
        else:
            y = (x * y - b) % n
            x = (x * x - 2) % n
    return x


def william_pp1(n):
    """
    williams p+1 algorithm for finding factors of a number
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n % 2 == 0:
        return 2
    if isprime(n):
        return n

    nsqrt = isqrt(n)
    if nsqrt * nsqrt == n:
        return nsqrt

    for v in count(1):
        for p in primegen():
            e = ilog(nsqrt, p)
            if e == 0:
                break
            for _ in range(e):
                v = mlucas(v, p, n)

            g = gcd(v - 2, n)
            if g == n:
                break
            if 1 < g:
                return g
