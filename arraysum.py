#!/bin/python

import sys


n = int(raw_input().strip())
arr = map(int,raw_input().strip().split(' '))

if n != len(arr):
    print "Error"
else:
    print sum(arr)
