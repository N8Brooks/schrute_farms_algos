#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:25:09 2020

@author: nathan
"""

import multiprocessing as mp
from random import randrange
from math import gcd
from sympy import isprime
from imath import ispower, primegen, ilog


def add(p1, p2, p0, n):
    x1, z1 = p1
    x2, z2 = p2
    x0, z0 = p0

    t1 = (x1 - z1) * (x2 + z2)
    t2 = (x1 + z1) * (x2 - z2)

    newx = z0 * pow(t1 + t2, 2, n) % n
    newz = x0 * pow(t1 - t2, 2, n) % n

    return newx, newz


def double(p, A, n):
    x, z = p
    An, Ad = A

    t1 = pow(x + z, 2, n)
    t2 = pow(x - z, 2, n)
    t = t1 - t2

    newx = t1 * t2 * 4 * Ad % n
    newz = (4 * Ad * t2 + t * An) * t % n

    return newx, newz


def multiply(m, p, A, n):
    if m == 0:
        return 0, 0
    elif m == 1:
        return p
    else:
        q = double(p, A, n)

        if m == 2:
            return q

        b = 1
        while b < m:
            b <<= 1
        b >>= 2

        r = p
        while b:
            if m & b:
                q, r = double(q, A, n), add(q, r, p, n)
            else:
                q, r = add(r, q, p, n), double(r, A, n)
            b >>= 1
        return r


def ecm1(n):
    seed = randrange(6, n)
    u = (seed * seed - 5) % n
    v = 4 * seed % n
    p = pow(u, 3, n)
    Q = (pow(v - u, 3, n) * (3 * u + v) % n, 4 * p * v % n)
    C = (p, pow(v, 3, n))
    i = 2
    i = 2
    while 1 == gcd(Q[1], n):
        Q = multiply(i, Q, C, n)
        print(Q, C)
        i += 1
    return gcd(Q[1], n)


def ecm(n):
    if isprime(n):
        return n
    if ispower(n):
        return ispower(n)

    B1 = round(145 * 1.07 ** n.bit_length())
    B2 = round(480 * 1.12 ** n.bit_length())

    while True:
        # print(B1, B2)
        seed = randrange(6, n)
        u = (seed * seed - 5) % n
        v = 4 * seed % n
        p = pow(u, 3, n)
        Q = (pow(v - u, 3, n) * (3 * u + v) % n, 4 * p * v % n)
        C = (p, pow(v, 3, n))

        # print('Stage 1')
        pg = primegen()
        p = next(pg)
        while p < B1:
            Q = multiply(p ** ilog(B1, p), Q, C, n)
            p = next(pg)

        g = gcd(Q[1], n)
        if g == n:
            B1, B2 = B1 // 2, B2 // 2
            continue
        elif 1 < g:
            return g

        # print('Stage 2')
        while p < B2:
            Q = multiply(p, Q, C, n)
            g = g * Q[1] % n
            p = next(pg)

        g = gcd(g, n)
        if g == 1:
            B1, B2 = B1 * 2, B2 * 2
        elif g == n:
            B1, B2 = B1 // 2, B2 // 2
        else:
            return g


def parecm(n, count=20):
    with mp.Pool(count) as p:
        processes = [p.apply_async(ecm, args=(n,)) for _ in range(count)]
        while True:
            for process in processes:
                if process.ready():
                    return process.get()
