#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 16:52:50 2020

@author: nathan
"""

def longestPalindrome(s: str) -> str:
    if len(s) < 2 or s == s[::-1]:
        return s
    n = len(s)
    start, maxlen = 0,1
    
    for i in range(n):
        odd = s[i-maxlen-1:i+1]
        even = s[i-maxlen:i+1]
        
        if i - maxlen -1>=0 and odd == odd[::-1]:
            start = i - maxlen - 1
            maxlen +=2
            continue
        if i - maxlen >=0 and even ==even[::-1]:
            start = i - maxlen 
            maxlen +=1
    return s[start:start+maxlen]


from random import choices
from string import ascii_lowercase as alpha
from time import time
from tqdm import trange
import pandas as pd

# In[]

df = pd.DataFrame(columns=['time'])

beta = ['a', 'b', 'c']
gamma = list(map(chr, range(2048)))

for i in trange(33):
    i = 2**i
    
    data = ''.join(choices(gamma, k=i))
    start = time()
    longestPalindrome(data)
    end = time()
    df.loc[i] = (end - start,)

df.plot()