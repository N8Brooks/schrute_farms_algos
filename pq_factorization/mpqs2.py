#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:59:35 2020

@author: nathan
"""

from math import gcd, log
from imath import ispower, isqrt, primes, mod_sqrt, issquare
from sympy import isprime
from collections import defaultdict, Counter
from itertools import product

def quadratic_sieve(n, bound=1024, sieve=1000000):
    """
    quadratic sieve to find a factor of an integer
    """
    
    if n % 2 == 0: return 2
    if isprime(n): return n
    if ispower(n): return ispower(n)
    
    # primes where n is a quadratic residue - 0 would mean divisable ... 
    p_list = [p for p in primes(bound) if pow(n, (p-1) // 2, p) != p-1]
    pi = len(p_list)
    
    rows = list()
    a_list = list()
    b_list = list()
    
    for a0 in range(isqrt(n) + 1, isqrt(2 * n), sieve):
        
        # sieving for b smooth numbers
        v_list = [a * a - n for a in range(a0, a0 + sieve)]
        for p in p_list:
            r = mod_sqrt(n, p)
            for i in range((r - a0) % p, sieve, p):
                while v_list[i] % p == 0:
                    v_list[i] //= p
            for i in range((p - r - a0) % p, sieve, p):
                while v_list[i] % p == 0:
                    v_list[i] //= p
        
        # factoring and checking
        for ai, r in enumerate(v_list):
            if r != 1 and not issquare(r):
                continue
            
            # factor all b smooth numbers
            ai += a0
            b2 = ai * ai - n
            v = 0
            factors = Counter()
            for i, p in enumerate(p_list):
                power = 0
                while b2 % p == 0:
                    b2 //= p
                    power += 1
                if power:
                    factors[p] = power
                    if power % 2: v |= 1 << i
                if b2 == 1: break
            
            # if b2 is square, use fermat's method
            if not v:
                print('fermat')
                return ai - isqrt(ai * ai - n)
            
            rows.append(v)
            a_list.append(ai)
            b_list.append(factors)
        
        # look for 3+ that combine
        print(len(rows))
        cols = [sum(1<<i for i, x in enumerate(rows) if (1<<j)&x) for j in range(pi)]
        marks = set(range(len(a_list)))
        
        # gaussian elimination
        for j, col in enumerate(cols):
            if not col: continue
            mask = 1
            i = 0
            while not mask & col:
                mask *= 2
                i += 1
            marks.remove(i)
            for k, col2 in enumerate(cols):
                if j == k: continue
                elif mask & col2: cols[k] ^= col
        
        # find matches
        rows2 = [sum(1<<i for i, x in enumerate(reversed(cols)) if (1<<j)&x) for j in range(len(a_list))]
        for mark in marks:
            r_list = [mark]
            mask = 1
            row = rows2[mark]
            for _ in range(pi):
                if mask & row:
                    r_list.append(rows2.index(mask))
                mask *= 2
            
            # combine with 0s?
            x = y = 1
            sq = Counter()
            for r in r_list:
                x = x * a_list[r] % n
                sq += b_list[r]
            for k, v in sq.items():
                y = y * pow(k, v//2, n) % n
            f = gcd(y - x, n)
            
            if 1 < f < n: return f
                
                
            
        