#!/usr/bin/env python3
'''
This script plots a 2D array as in image.
It also gives statistics about the array.
'''

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from mpl_toolkits.mplot3d import Axes3D

# isdigit() doesn't work for decimal numbers
def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`,
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True


plt.ion()

scale0 = 5000
scale = 1
# print("Scale for points : 1000, confirm ? (enter/n)")
print("Scale for point size : %03f"%scale)
key = input("Enter new scale ? (just hit enter if not) : ")
if is_number(key):
    scale = float(key)

for i in range(1,len(sys.argv)):
    file = sys.argv[i]
    A = np.load(file)
    if A.ndim != 3:
        print("Error: Array must be of dimension 3")
        input("Hit Enter to quit ...")
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
    n0,n1,n2 = A.shape
    n = np.cbrt(n0*n1*n2)
    t0 = np.linspace(0,1,n0)
    t1 = np.linspace(0,1,n1)
    t2 = np.linspace(0,1,n2)
    [r, g, b] = np.meshgrid(t2, t1, t0, indexing="ij")
    colors = np.vstack((r.flatten(), g.flatten(), b.flatten())).T
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(r, g, b, s=(scale*scale0/n) * A / np.max(A),c=colors)
    ax.set_xlabel('R (slow index)')
    ax.set_ylabel('G (medium index)')
    ax.set_zlabel('B (fast index)')
    plt.title("scale=%g, max=%e"%(scale,np.max(A)))

# plt.show()
input("Hit Enter to quit ...")

