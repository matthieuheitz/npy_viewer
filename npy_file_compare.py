#!/usr/bin/env python3
"""
This script compares the content of two NPY files
It gives statistics about the difference array A-B
If the arrays are 2D, a visual difference is plotted.
"""

import os
import sys
print("Python version:",sys.version)
print("Python interpreter:",sys.executable)
try:
    import matplotlib.pyplot as plt
    import numpy as np

except ImportError as error:
    print(error)
    input("Press any key to exit")
    exit()


def hit_enter_to_quit():
    if sys.platform.startswith('linux'):
        input("Hit Enter to quit ...")


if len(sys.argv) != 3:
    print("ERROR: Exactly two files must be selected for comparison")
    hit_enter_to_quit()
    exit(0)

f1 = sys.argv[1]
f2 = sys.argv[2]
A1 = np.load(f1)
A2 = np.load(f2)

print("Comparing the 2 files:\n")
print("f1: ",os.path.basename(f1),"\n")
print(A1)
print("\n")
print("f2: ",os.path.basename(f2),"\n")
print(A2)
print("\n")

if A1.shape != A2.shape:
    print("The two files have different shapes:")
    print(os.path.basename(f1)," has shape ",A1.shape)
    print(os.path.basename(f2)," has shape ",A2.shape)
    print("The two files must be of same shape for further comparison.")
    hit_enter_to_quit()
    exit(0)

abs_err = np.abs(A2-A1)
if np.sum(abs_err != 0) == 0:
    print("The two files are identical.\n")
    hit_enter_to_quit()
    exit(0)

print("The two files have the same shape: ",A1.shape,"\n")

print("Distance functions :")
print("0-norm = ",np.sum(abs_err != 0))
print("Total Variation = ",np.sum(abs_err))
print("Quadratic Loss = ",np.sum((A2-A1)**2))
print("KL(A1|A2) = ",np.sum(A1*np.log(A1/A2)-A1+A2))
print("KL(A2|A1) = ",np.sum(A2*np.log(A2/A1)-A2+A1))
print("\n")

print("Stats on the absolute difference : \n")
print("min \t=",np.min(abs_err))
print("max \t=",np.max(abs_err))
print("mean \t=",np.mean(abs_err))
print("median \t=",np.median(abs_err))
print("std_dev\t=",np.std(abs_err))
print("\n")

print("Number of equal values: ",np.sum(abs_err == 0))
print("Stats on the absolute difference without equal values: \n")
print("min \t=",np.min(abs_err[abs_err > 0]))
print("mean \t=",np.mean(abs_err[abs_err > 0]))
print("std_dev\t=",np.std(abs_err[abs_err > 0]))
print("\n")

if len(A1.shape) == 2:
    plt.figure(figsize=(8,8))
    plt.subplot(221)
    plt.imshow(A1,cmap='gray')
    plt.title("f1")
    plt.colorbar()
    plt.subplot(222)
    plt.imshow(A2,cmap='gray')
    plt.title("f2")
    plt.colorbar()
    plt.subplot(223)
    plt.imshow(A1-A2,cmap='gray')
    plt.title("f1-f2")
    plt.colorbar()
    plt.subplot(224)
    plt.imshow(np.abs(A1-A2),cmap='gray')
    plt.title("abs(f1-f2)")
    plt.colorbar()
    plt.show()

hit_enter_to_quit()
