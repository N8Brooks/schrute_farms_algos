#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:05:50 2020

@author: nathan
"""

from itertools import permutations
from random import shuffle

def perm_sort(arr):
    """
    sort arr in-place by iterating through permutations of arr
    worst: O(n!), average: O(n!), best: O(n)
    """
    length = len(arr)
    for perm in permutations(arr, length):
        if all(perm[j - 1] < perm[j] for j in range(1, length)):
            for j, y in enumerate(perm):
                arr[j] = y
            break

def rand_sort(arr):
    """
    sort arr in-place by iterating through permutations of arr
    worst: inf, average: O(n!), best: O(n)
    """
    length = len(arr)
    while any(arr[i] < arr[i - 1] for i in range(1, length)):
        shuffle(arr)

def bubble_sort(arr):
    """
    sort arr in-place using bubble sort
    O(n^2)
    """
    length = len(arr)
    for i, x in enumerate(arr):
        for j in range(i + 1, length):
            if x > arr[j]:
                x, arr[j] = arr[j], x
                arr[i] = x

def insertion_sort(arr):
    """
    sort arr in-place using insertion sort
    O(n^2)
    """
    for j, x in enumerate(arr, start=-1):
        while j >= 0 and arr[j] > x: 
            arr[j + 1] = arr[j] 
            j -= 1
        arr[j + 1] = x

def selection_sort(arr):
    """
    sort arr in-place using selection sort
    O(n^2)
    """
    length = len(arr)
    for i, x in enumerate(arr):
        j = min(range(i, length), key=lambda j: arr[j])
        arr[i], arr[j] = arr[j], x

def shell_sort(arr): 
    """
    sort arr in-place using shell sort
    O(n^2)
    """
    length = len(arr)
    gap = length // 2
    while gap > 0:
        for i in range(gap, length):
            x = arr[i]
            while i >= gap and arr[i - gap] > x:
                arr[i] = arr[i - gap]
                i -= gap
            arr[i] = x
        gap //= 2

def merge_sort(arr):
    """
    sort arr in-place using merge sort
    O(nlog(n))
    """
    length = len(arr)
    if length < 2: return
    l, r = length // 2, length - length // 2
    L, R = arr[:l], arr[l:]
    merge_sort(L); merge_sort(R)
    
    i = j = k = 0
    while i < l and j < r: 
        if L[i] < R[j]: 
            arr[k] = L[i] 
            i+=1
        else: 
            arr[k] = R[j] 
            j+=1
        k+=1
    
    while i < l: 
        arr[k] = L[i] 
        i+=1
        k+=1
    while j < r: 
        arr[k] = R[j] 
        j+=1
        k+=1

def quick_sort(arr, lo=0, hi=None):
    """
    sort arr in place from lo to hi with quick sort algorithm
    worst: O(n^2), average: O(n*log(n)), best: O(n*log(n))
    """
    def partition(arr, lo, hi):
        i = lo
        x = arr[hi]
        for j in range(lo, hi):
            if arr[j] < x:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[hi] = arr[hi], arr[i]
        return i
    
    if hi is None:
        hi = len(arr) - 1
    if lo < hi:
        pi = partition(arr, lo, hi) 
        quick_sort(arr, lo, pi - 1) 
        quick_sort(arr, pi + 1, hi)
  
def heap_sort(arr): 
    """
    sort arr in place with heap sort algorithm
    O(nlog(n)) for any scenario
    """
    def heapify(arr, n, i): 
        largest = i
        l, r = 2 * i + 1, 2 * i + 2
        if l < n and arr[i] < arr[l]: 
            largest = l 
        if r < n and arr[largest] < arr[r]: 
            largest = r 
        if largest != i: 
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    
    length = len(arr)
    for i in range(length, -1, -1): 
        heapify(arr, length, i)
    for i in range(length-1, 0, -1): 
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

def tim_sort(arr, run=32):
    """
    sort arr in place using timsort algorithm
    O(nlog(n))
    """
    def insort(arr,start,end):    
        for i in range(start+1, end+1):
            elem = arr[i]
            j = i-1
            while j >= start and elem < arr[j]:
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = elem
        return arr
    
    def merge(arr,start,mid,end):
        if mid==end:
            return arr
        ind = start
        ind1 = ind2 = 0
        first, last = arr[start:mid+1], arr[mid+1:end+1]
        len1, len2 = mid-start+1, end-mid
        
        while ind1 < len1 and ind2 < len2:
            if first[ind1] < last[ind2]:
                arr[ind] = first[ind1]
                ind1 += 1
            else:
                arr[ind] = last[ind2]
                ind2 += 1
            ind += 1
        
        while ind1 < len1:
            arr[ind] = first[ind1]
            ind1 += 1
            ind += 1
        
        while ind2 < len2:
            arr[ind] = last[ind2]
            ind2 += 1
            ind += 1
        
        return arr
    
    n = len(arr)
    
    for start in range(0, n, run):
        end = min(start + run - 1, n - 1)
        arr = insort(arr, start, end)
    
    while run < n:    
        for start in range(0, n, run * 2):
            mid = min(n - 1, start + run - 1)
            end = min(n - 1, mid + run)
            arr = merge(arr, start, mid, end)
        run *= 2

def counting_sort(arr):
    """
    sort arr in place with counting sort algorithm
    O(n + k) where k is the max digit
    """
    lo = min(arr)
    domain = max(arr) - lo + 1
    tmp = [0] * len(arr)
    counts = [0] * domain
    for x in arr:
        counts[x - lo] += 1
    for i in range(1, domain):
        counts[i] += counts[i - 1]
    for x in arr:
        counts[x - lo] -= 1
        tmp[counts[x - lo]] = x
    
    for i, y in enumerate(tmp):
        arr[i] = y

def radix_sort(arr, base=10):
    """
    sort arr in place with radix sort algorithm (positive integers only)
    O(d(n + k))
    """
    lo = min(arr, default=0)
    hi = max(arr, default=0) - lo
    exp = 1
    while hi // exp:
        tmp = arr[::-1]
        counts = [0] * base
        for x in tmp:
            counts[(x - lo) // exp % base] += 1
        for i in range(1, base):
            counts[i] += counts[i - 1]
        for x in tmp:
            index = (x - lo) // exp % base
            counts[index] -= 1
            arr[counts[index]] = x
        exp *= base

def bucket_sort(arr, buckets=10000):
    """
    sort arr in place with bucket sorting algorithm
    worst: O(n^2), average: O(n + k), best: O(n + k)
    """
    lo = min(arr, default=0)
    hi = max(arr, default=0)
    sz = (hi - lo) // buckets + 1
    
    slots = [list() for _ in range(buckets)]
    for x in arr:
        slots[(x - lo) // sz].append(x)
    
    i = 0
    for slot in slots:
        for j, x in enumerate(slot, start=-1):
            while j >= 0 and slot[j] > x: 
                slot[j + 1] = slot[j] 
                j -= 1
            slot[j + 1] = x
        for y in slot:
            arr[i] = y
            i += 1

def is_sorted(arr):
    return all(arr[i-1] <= arr[i] for i in range(1, len(arr)))

def gen_arr(n, lo=0, hi=9223372036854775807):
    from random import choices
    return list(choices(range(lo, hi), k=n))

def unit_test():
    from random import randrange
    algorithms = [bubble_sort, insertion_sort, selection_sort, \
                  quick_sort, shell_sort, merge_sort, \
                  heap_sort, radix_sort, tim_sort, bucket_sort]
    
    tests = [list(range(1000)), list(range(1000))[::-1], [], [1], [2, 1]]
    tests.extend(gen_arr(1000, -1000, randrange(900, 1000)) for _ in range(95))
    
    for data in tests:
        for algo in algorithms:
            cp = data[:]
            algo(cp)
            if not is_sorted(cp):
                print(data)
                print(cp)
                print(algo.__name__)
                assert False
    
    print('all tests passed successfully')

if __name__ == '__main__':
    from time import time
    from tqdm import trange
    import pandas as pd
    
    #algorithms = [bubble_sort, insertion_sort, selection_sort, \
    algorithms = [              quick_sort, shell_sort, merge_sort, \
                  heap_sort, radix_sort, tim_sort, bucket_sort]
        
    df = pd.DataFrame(columns=[x.__name__ for x in algorithms])
    
    for i in trange(100000, 100000001, 100000):
        record=pd.Series()
        data = gen_arr(i, 0, 1000000)
        for algo in algorithms:
            cp = data[:]
            t0 = time()
            algo(cp)
            t1 = time()
            record[algo.__name__] = t1 - t0
        df.loc[i] = record
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    