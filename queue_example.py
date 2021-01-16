# -*- coding: utf-8 -*-
"""
https://www.geeksforgeeks.org/stack-queue-python-using-module-queue/
"""

import queue

# From class queue, Queue is
# created as an object Now L
# is Queue of a maximum
# capacity of 20
L = queue.Queue(maxsize=20)

# Data is inserted into Queue
# using put() Data is inserted
# at the end
L.put(5)
L.put(9)
L.put(1)
L.put(7)

# get() takes data out from
# the Queue from the head
# of the Queue
print(L.get())
print(L.get())
print(L.get())
print(L.get())

# In[]

import queue

L = queue.Queue(maxsize=6)

# qsize() give the maxsize
# of the Queue
print(L.qsize())

L.put(5)
L.put(9)
L.put(1)
L.put(7)

# Return Boolean for Full
# Queue
print("Full: ", L.full())

L.put(9)
L.put(10)
print("Full: ", L.full())

print(L.get())
print(L.get())
print(L.get())

# Return Boolean for Empty
# Queue
print("Empty: ", L.empty())

print(L.get())
print(L.get())
print(L.get())

print("Empty: ", L.empty())
print("Full: ", L.full())

# This would result into Infinite
# Loop as the Queue is empty.
# print(L.get())
