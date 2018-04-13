#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

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
    plt.figure()
    plt.imshow(A,cmap='gray')
    plt.title(os.path.basename(file))

plt.show()
input("Hit Enter to quit ...")
