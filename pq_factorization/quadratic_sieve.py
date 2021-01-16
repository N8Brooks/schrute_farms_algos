#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 11:13:13 2020

@author: nathan
"""

from math import gcd, log
from sympy import isprime
from imath import ispower, issquare, isqrt, primes, mod_sqrt, iroot, primegen
from collections import defaultdict
from itertools import count


def quadratic_factor(n, bound=None):
    """
    return factor of n using congruence of squares
    looks for two congruent b^2s using a dictionary of bitsets
    """
    if n <= 1:
        return 1
    if isprime(n):
        return n
    if ispower(n):
        return ispower(n)

    # heuristic optimization of bound
    if bound is None:
        bound = max(int(10 ** (log(n, 10) / 4)), 3)

    # look for b^2s by iterating a above the sqrt of n
    p_list = list(primes(bound))
    memo = defaultdict(list)
    for ai in count(isqrt(n) + 1):
        vi = 0
        b2 = ai * ai - n

        # odd powers bitset of the factorization of b2 using trial division
        for i, p in enumerate(p_list):
            while b2 % p == 0:
                b2 //= p
                vi ^= 1 << i
            if b2 == 1:
                break
        else:
            # not b-smooth
            if not issquare(b2):
                continue

        # if b2 is square, use fermat's method
        if not vi:
            return ai - isqrt(ai * ai - n)

        # compare against sieved congruent a values
        for aj in memo[vi]:
            x = ai * aj - n
            y = isqrt((ai * ai - n) * (aj * aj - n))
            # pow(x, 2, n) == pow(y, 2, n)
            if 1 < gcd(y - x, n) < n:
                return gcd(y - x, n)

        # add the current a to the memo
        memo[vi].append(ai)


def quadratic_sieve(n, bound=1024, sieve=1000000):
    """
    quadratic sieve to find a factor of an integer
    """
    if n % 2 == 0:
        return 2
    if isprime(n):
        return n
    if ispower(n):
        return ispower(n)

    memo = defaultdict(list)
    for a0 in range(isqrt(n) + 1, isqrt(2 * n), sieve):
        # primes where n is a quadratic residue
        p_list = [p for p in primes(bound) if 0 < pow(n, (p - 1) // 2, p) < p - 1]

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
            for i, p in enumerate(p_list):
                while b2 % p == 0:
                    b2 //= p
                    v ^= 1 << i
                if b2 == 1:
                    break

            # if b2 is square, use fermat's method
            if not v:
                return ai - isqrt(ai * ai - n)

            # compare against sieved congruent a values
            for aj in memo[v]:
                x = ai * aj - n
                y = isqrt((ai * ai - n) * (aj * aj - n))
                if 1 < gcd(y - x, n) < n:
                    return gcd(y - x, n)

            memo[v].append(ai)

        # increase bound size
        bound *= 2


def quadratic_sieve2(n, bound=100000):
    global c_list, v_list
    p_list = list(primes(bound))
    ai = isqrt(n)
    b2 = ai * ai - n

    def vectorize(b2):
        v = 0
        for i, p in enumerate(p_list):
            while b2 % p == 0:
                b2 //= p
                v ^= 1 << i
            if b2 == 1:
                return v

    a_list = list()
    v_list = list()
    b_list = list()
    c_list = [0] * len(p_list)

    # sieving
    for i in range(len(p_list) + 1):
        # find b that is smooth
        vi = None
        while vi is None:
            b2 += 2 * ai + 1
            ai += 1
            vi = vectorize(b2)

        # check fermat simple case
        if not vi:
            print("fermat")
            return ai - isqrt(b2)

        # add to lists
        a_list.append(ai)
        b_list.append(b2)
        v_list.append(vi)

        # add column
        v = vi
        c = 0
        for _ in range(len(p_list)):
            c_list[c] *= 2
            if v % 2:
                c_list[c] += 1
            v //= 2
            c += 1

    # attempt at gauss
    c_copy = c_list[:]
    marks = set(range(len(v_list)))
    for col_j, bits_j in enumerate(c_copy):
        if not bits_j:
            continue
        row_i = 0
        bit_i = 1
        while not bits_j & bit_i:
            row_i += 1
            bit_i *= 2

        marks.discard(row_i)
        for col_k in range(len(c_copy)):
            if col_k == col_j:
                continue
            if bit_i & c_copy[col_k]:
                c_copy[col_k] ^= bits_j

    # find lone rows
    v_copy = list()
    for i in range(len(v_list)):
        v = 0
        for c in range(len(c_copy)):
            v *= 2
            if c_copy[c] % 2:
                v += 1
            c_copy[c] //= 2
        v_copy.append(v)

    # find dependences
    for m in marks:
        j_list = [m]
        row_j = v_copy[m]
        bit_j = 1
        # could be dictionary
        for i in range(row_j.bit_length()):
            if bit_j & row_j:
                j_list.append(v_copy.index(bit_j))
            bit_j *= 2

        # calculate x and y
        x = y = 1
        for j in j_list:
            x = x * a_list[-j - 1] % n
            y = y * b_list[-j - 1]
        y = iroot(y, len(j_list))

        # check if valid
        if 1 < gcd(y - x, n) < n:
            print(len(j_list))
            return gcd(y - x, n)


def pv(v_list):
    print("\n".join(bin(x)[2:].rjust(4, "0") for x in v_list))


def pc(c_list):
    print(
        "\n".join(
            "".join(bin(x)[2:].rjust(5, "0")[i] for x in c_list) for i in range(5)
        )
    )


def create_v():
    global v_list
    v_list = list(
        map(lambda x: int(x, 2), ["1100", "1101", "0111", "0010", "0001"][::-1])
    )


def create_c():
    global c_list
    c_list = [0] * len(p_list)
    for v in v_list:
        c = 0
        for _ in range(len(p_list)):
            c_list[c] *= 2
            if v % 2:
                c_list[c] += 1
            v //= 2
            c += 1
