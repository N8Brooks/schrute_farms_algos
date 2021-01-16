# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:28:50 2020

@author: DSU
"""

from functools import reduce
from operator import mul
from math import gcd, prod
from random import randrange


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


def prime(n):
    """return if n is prime using 6 wheel"""
    # return if it is 2 or 3
    if n < 4:
        return n > 1
    # cut down on iteration checking 2s and 3s
    if n % 2 == 0 or n % 3 == 0:
        return False
    # check if any 5 (mod 6) and 1 (mod 6) integers divide n
    return all(n % i and n % (i + 2) for i in range(5, isqrt(n) + 1, 6))


def fermat(n, a=2):
    """returns if n is probably prime according to fermat's primality test"""
    return pow(a, n - 1, n) == 1


def mrpt(n, k=9):
    """miller rabin primality test"""
    """return if n is probably prime given k random witnesses"""
    if n < 4:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False

    r = -1
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        x = pow(randrange(2, n - 1), d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def prime_sieve(n):
    """generate the primes less than n using the sieve of eratosthenes."""
    a = [False, False] + [True] * (n - 2)
    for i, isprime in enumerate(a):
        if isprime:
            yield i
            for j in range(i * i, n, i):
                a[j] = False


def factor(n):
    """return all prime factors of int n"""
    ret = dict()
    for prime in prime_sieve(isqrt(n) + 1):
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
    ret, tmp, pwr = [1], [], 1
    for prime in prime_sieve(isqrt(n) + 1):
        while not n % prime:
            n //= prime
            pwr *= prime
            tmp.extend([pwr * x for x in ret])
        if tmp:
            ret.extend(tmp)
            tmp, pwr = [], 1
    if n > 1:
        ret.extend([n * x for x in ret])
    return ret


def crt(r, m):
    """chinese remainder theorem"""
    """return x such that x = r (mod m) for all a and n"""
    total = 0
    product = prod(m)
    for m_i, r_i in zip(m, r):
        p = product // m_i
        total += r_i * imod(p, m_i) * p

    return total % product


def bsgs(g, r, p):
    """baby step giant step algorithm"""
    """return x such that g^x = r (mod p)"""
    n = int((p - 1) ** 0.5) + 1
    u = imod(pow(g, n, p), p) % p

    def powers(base, multiplier):
        yield base
        for _ in range(n):
            base = base * multiplier % p
            yield base

    list1 = {tmp: i for i, tmp in enumerate(powers(1, g))}
    list2 = enumerate(powers(r, u))

    return next(list1[tmp] + j * n for j, tmp in list2 if tmp in list1)


def pha(g, r, p):
    """pohlig-hellman algorithm"""
    """return x such that g^x = r (mod p)"""
    u = p - 1
    ms = [base ** exp for base, exp in factor(u).items()]
    rs = [bsgs(pow(g, x, p), pow(r, x, p), p) for x in (u // x for x in ms)]
    return crt(rs, ms)


def ipow(n, e, p):
    """pow that handles negative exponents"""
    if e >= 0:
        return pow(n, e, p)
    else:
        return pow(imod(n, p), -e, p)


def find_base(e, r, p):
    """returns x such that x^e = r (mod p)"""
    phi = reduce(mul, (x - 1 for x in factor(p)))
    x = pow(r, imod(e, phi) % phi, p)
    return x if pow(x, e, p) == r else None


def isqrt(n):
    """
    returns the sqrt of n rounded down
    also found in the math library of python 3.8+
    """
    if n == 0:
        return 0
    x, y = n, (n + 1) // 2
    while y < x:
        x, y = y, (y + n // y) // 2
    return x


def ilog(x, b):
    """
    greatest integer l such that b**l <= x.
    """
    i = 0
    while x >= b:
        x //= b
        i += 1
    return i


def imod(a, m):
    """
    inverse mod
    return x such that a * x = 1 (mod m)
    """
    a, x, u = a % m, 0, 1
    while a:
        x, u, m, a = u, x - m // a * u, a, m % a
    return x


def iroot(n, r=2):
    """
    return greatest x such that x^r <= n
    """
    if n < 0:
        return -iroot(-n, r) if r % 2 else None
    if n < 2:
        return n
    if r == 2:
        return isqrt(n)
    lo, hi = 0, n
    while lo < hi:
        mi = (lo + hi) // 2
        if mi ** r > n:
            hi = mi
        else:
            lo = mi + 1
    return hi - 1


def ispower(n):
    """
    returns x such that x to some power equals n
    returns 0 if there is no such x
    """
    for p in primegen():
        x = iroot(n, p)
        if x is None:
            continue
        if x ** p == n:
            return x
        if x == 1:
            return 0


def primegen():
    yield 2
    yield 3
    yield 5
    yield 7
    yield 11
    yield 13
    ps = primegen()  # yay recursion
    p = next(ps)
    p = next(ps)
    q, sieve, n = p ** 2, {}, 13
    while True:
        if n not in sieve:
            if n < q:
                yield n
            else:
                nxt, step = q + 2 * p, 2 * p
                while nxt in sieve:
                    nxt += step
                sieve[nxt] = step
                p = next(ps)
                q = p ** 2
        else:
            step = sieve.pop(n)
            nxt = n + step
            while nxt in sieve:
                nxt += step
            sieve[nxt] = step
        n += 2


def is_mersenne_prime(p):
    """
    lucas lehmer test
    returns whether 2^p-1 is prime
    """
    if p == 2:
        return True
    else:
        m = 2 ** p - 1
        s = 4
        for _ in range(2, p):
            sqr = s * s
            s = (sqr & m) + (sqr >> p)
            if s >= m:
                s -= m
            s -= 2
        return s == 0


def order(a, p):
    """
    tests the divisors of p - 1
    """
    if not prime(p) or a % p == 0:
        return False
    for k in divisors(p - 1):
        if pow(a, k, p) == 1:
            return k


def is_generator(a, p):
    """
    returns if a is generator/primative root modulo p
    """
    return prime(p) and order(a, p) == p - 1
