#!/usr/bin/env python3
'''
This script gives statistics about the array in the NPY file
'''

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
    A = np.load(file)
    print(os.path.basename(file)," :\n")
    print(A)
    print("shape \t=",A.shape)
    print("min \t=",np.min(A))
    print("max \t=",np.max(A))
    print("abs_min\t=",np.min(np.abs(A)))
    print("mean \t=",np.mean(A))
    print("median \t=",np.median(A))
    print("std_dev\t=",np.std(A))
    print("\n")

if sys.platform.startswith('linux'):
    input("Hit Enter to quit ...")
