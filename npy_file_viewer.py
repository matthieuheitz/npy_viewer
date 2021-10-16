#!/usr/bin/env python3
"""
This script gives statistics about the array in the NPY file
"""


import os
import sys

print("Python version:",sys.version)
print("Python interpreter:",sys.executable)
try:
    import numpy as np

except ImportError as error:
    print(error)
    input("Press any key to exit")
    exit()


for i in range(1,len(sys.argv)):
    file = sys.argv[i]
    # I know this is bad for security, but it's necessary for viewing object arrays.
    A = np.load(file, allow_pickle=True)
    print(os.path.basename(file)," :\n")
    print(A)
    print("\nshape \t=",A.shape)
    A[2] = "hello"*250
    if A.dtype == np.dtype("O"):
        print("A is an 'object' array:")
        for i,e in enumerate(A):
            print("i=%d: type:"%i,type(e),end="")
            try: print(", len = %d"%len(e),end="")     # If e is iterable
            except: pass
            if isinstance(e, str): print(": %s"%e[:100], "..." if len(e)>100 else "", end="")  # If e is a str, print the beginning
            print()
    else:
        print("min \t=",np.min(A))
        print("max \t=",np.max(A))
        print("abs_min\t=",np.min(np.abs(A)))
        print("mean \t=",np.mean(A))
        print("median \t=",np.median(A))
        print("std_dev\t=",np.std(A))
    print("\n")

if sys.platform.startswith('linux'):
    input("Hit Enter to quit ...")
