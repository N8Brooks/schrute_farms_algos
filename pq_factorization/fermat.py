#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 13:32:41 2020

@author: nathan
"""

from imath import issquare, isqrt, ilog, primegen
from sympy import isprime
from collections import defaultdict


def fermat(n):
    """
    return factor of n using fermat method
    """
    if n <= 1:
        return 1
    if n % 2 == 0:
        return 2

    a = isqrt(n)
    b2 = a * a - n
    while not issquare(b2):
        b2 += 2 * a + 1
        a += 1

    b = isqrt(b2)
    return a - b, a + b


def fermat_sieve(n):
    """
    returns factor of N using fermat sieve method
    """
    if n <= 1:
        return 1
    if n % 2 == 0:
        return 2
    if isprime(n):
        return n

    def prime_powers():
        # iterates through increasingly smaller powers of primes
        # modeled after powers of highly composite numbers
        # also finds squares mod p to simply check if square
        perc = 1.0
        for p in primegen():
            p = p ** (max(1, ilog(ilog(n, p), p)))
            yield p, frozenset(i * i % p for i in range(p // 2 + 1))

    def worker(a, b2, astep, i):
        # finishes off steps if it deems it low enough
        # otherwise it finds more squares via quadratic residue
        double = astep + astep
        square = astep * astep
        m, s = modulus[i]
        if astep * m + a >= aend:
            while a < aend:
                b = isqrt(b2)
                if b * b == b2:
                    return a - b, a + b
                else:
                    b2 += double * a + square
                    a += astep
        else:
            for _ in range(m):
                if b2 % m in s:
                    ret = worker(a, b2, astep * m, i + 1)
                    if ret is not None:
                        return ret
                b2 += double * a + square
                a += astep

    # prime power iterator, saved powers, start and end
    ps = prime_powers()
    modulus = defaultdict(lambda: next(ps))
    astart = isqrt(n)
    aend = isqrt(n + n)

    # call to helper function
    while True:
        ret = worker(astart, astart * astart - n, 1, 0)
        if ret is not None:
            return ret
        astart, aend = aend, 2 * aend
