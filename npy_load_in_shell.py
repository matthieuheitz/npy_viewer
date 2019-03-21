#!/usr/bin/env python3
'''
This script opens an interactive shell with the NPY file loaded as the array A.
If multiple files are passed, then it builds a dictionary of arrays,
where each array can be accessed in order : A[0], A[1], etc.
It also displays the array(s) and gives some statistics.
PyPlot is preloaded so that you don't have to type it.
'''

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

A = []

for i in range(0,len(sys.argv)-1):
    file = sys.argv[i+1]
    A.append(np.load(file))
    print(os.path.basename(file)," :\n")
    print(A[i])
    print("shape \t=",A[i].shape)
    print("min \t=",np.min(A[i]))
    print("max \t=",np.max(A[i]))
    print("abs_min\t=",np.min(np.abs(A[i])))
    print("mean \t=",np.mean(A[i]))
    print("median \t=",np.median(A[i]))
    print("std_dev\t=",np.std(A[i]))
    print("\n")

# If only one array is passed, don't use a dictionary
if len(sys.argv) == 2:
    A = A[0]