#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 09:35:06 2020

@author: nathan
"""

from random import randrange


def is_prime(n):
    """return if n is prime"""
    # return if it is 2 or 3
    if n < 4:
        return n > 1
    # cut down on iteration checking 2s and 3s
    if n % 2 == 0 or n % 3 == 0:
        return False
    # check other cases
    return all(n % i and n % (i + 2) for i in range(5, int(n ** 0.5) + 1, 6))


def get_prime(n):
    a, b = 10 ** (n - 1), 10 ** n
    while True:
        x = randrange(a, b)
        if is_prime(x):
            return x


def linear_recurrence(seed, a, x, n):
    while True:
        seed = (a * seed + c) % n
        yield seed


def square_last_term(seed, n=get_prime(8) * get_prime(8)):
    while True:
        seed = pow(seed, 2, n)
        yield seed


def square_the_middle(seed, n=4):
    half = 10 ** (n // 2)
    max_digit = 10 ** n
    min_digit = 10 ** (2 * n - 1)
    while True:
        seed **= 2
        while 0 < seed < min_digit:
            seed *= 10
        seed = seed // half % max_digit
        yield seed
