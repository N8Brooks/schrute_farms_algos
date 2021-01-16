# -*- coding: utf-8 -*-

from imath import ilog
from sympy import isprime
from time import time
import pandas as pd
from tqdm import trange
from random import randrange

from trial_division import trial_division
from pollard_pm1 import pollard_pm1, pollard_pm2
from william_pp1 import william_pp1
from fermat import fermat, fermat_sieve
from pollard_rho import brent_rho, pollard_rho
from quadratic_sieve import quadratic_sieve, quadratic_sieve2
from ecm import ecm
from mpqs import mpqs

from cypari import pari
def gfns(n):
    return pari(n).factorint()

algorithms = [brent_rho, pollard_rho, fermat, fermat_sieve, trial_division, ecm, william_pp1, mpqs]
#algorithms = [congrunce_of_squares]
#algorithms = [gfns]
algorithms = [ecm, ecm1]

def pqs(n):
    """
    returns a set of 3 semiprimes with length n
    """
    ret = {4, 6, 9} if n == 1 else set()
    y = n // 2
    x = n - y
    bp1, bq1 = 10**(y - 1), 10**(x - 1)
    bp2, bq2 = bp1 * 10, bq1 * 10
    while len(ret) < 3:
        p = 1
        while not isprime(p):
            p = randrange(bp1, bp2)
        q = 1
        while not isprime(q):
            q = randrange(bq1, bq2)
        if ilog(p * q, 10) + 1 == n:
            ret.add(p * q)
    return ret

if __name__ == '__main__':
    df = pd.DataFrame(columns=[x.__name__ for x in algorithms])
    pbar = trange(3, 200)
    for i in pbar:
        record = list()
        data = pqs(i)
        for algo in algorithms:
            pbar.desc = algo.__name__
            pbar.refresh()
            best = 2**9
            for x in data:
                t0 = time()
                algo(x)
                best = min(time() - t0, best)
            record.append(best)
        df.loc[i] = record