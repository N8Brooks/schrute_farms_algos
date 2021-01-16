#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:29:13 2020

@author: nathan
"""

from array import array
from bisect import bisect_left


def longest_increasing_subsequence(nums) -> int:
    tails = array("i")
    count = 0

    for x in nums:
        i = bisect_left(tails, x)
        if i == count:
            tails.append(x)
            count += 1
        else:
            tails[i] = x

    return count
