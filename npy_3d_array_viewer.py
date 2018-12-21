#!/usr/bin/env python3
'''
This script plots a 3D array as a scatter plot with point size depending on array values.
It also gives statistics about the array.

If multiple files are in parameters, then you can switch between files with the arrows of the figure,
or with the left/right, up/down keys.
'''

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from mpl_toolkits.mplot3d import Axes3D

# Choose your backend
plt.switch_backend("Qt4Agg")

num_files = len(sys.argv)-1
f_index = 0
fig = plt.figure()
file = sys.argv[1]
data = None
n = 0
# data = plt.imshow(np.load(sys.argv[1]),cmap='gray')

# isdigit() doesn't work for decimal numbers
def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`,
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True

scale0 = 5000
scale = 1
# print("Scale for points : 1000, confirm ? (enter/n)")
print("Scale for point size : %03f"%scale)
key = input("Enter new scale ? (just hit enter if not) : ")
if is_number(key):
    scale = float(key)



def hit_enter_to_quit():
    exit(0)
    # if sys.platform.startswith('linux'):
    #     input("Hit Enter to quit ...")


def print_info(A,file):

    print(os.path.basename(file), " :\n")
    print(A)
    print("shape \t=", A.shape)
    print("min \t=", np.min(A))
    print("max \t=", np.max(A))
    print("abs_min\t=", np.min(np.abs(A)))
    print("mean \t=", np.mean(A))
    print("median \t=", np.median(A))
    print("std_dev\t=", np.std(A))
    print("")   # Jumps one line
    # print("\n") # Jumps two lines


def plot_array(A,fig,file):
    # fig.clf()
    global data
    global n
    n0,n1,n2 = A.shape
    n = np.cbrt(n0*n1*n2)
    t0 = np.linspace(0,1,n0)
    t1 = np.linspace(0,1,n1)
    t2 = np.linspace(0,1,n2)
    [r, g, b] = np.meshgrid(t2, t1, t0, indexing="ij")
    colors = np.vstack((r.flatten(), g.flatten(), b.flatten())).T
    # fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    data = ax.scatter(r, g, b, s=(scale*scale0/n) * A / np.max(A),c=colors)
    ax.set_xlabel('R (slow index)')
    ax.set_ylabel('G (medium index)')
    ax.set_zlabel('B (fast index)')



def callback_left_button(event):
    """ this function gets called if we hit the left button"""
    # print('Left button pressed')
    global f_index
    if f_index == 1:
        return
    else:
        f_index -= 1

    file = sys.argv[f_index]
    A = np.load(file)
    if A.ndim != 3:
        print("Error: Array must be of dimension 3")
        exit(-1)
    # Modify plot
    data.set_sizes((scale*scale0/n) * A.flatten() / np.max(A))
    plt.suptitle("%s\n scale=%g, max=%e"%(os.path.basename(file),scale,np.max(A)))
    # Redraw
    fig.canvas.draw()
    fig.canvas.flush_events()
    # Print image information
    print_info(A,file)


def callback_right_button(event):
    """ this function gets called if we hit the left button"""
    # print('Right button pressed')
    global f_index
    if f_index == num_files:
        return
    else:
        f_index += 1

    file = sys.argv[f_index]
    A = np.load(file)
    if A.ndim != 3:
        print("Error: Array must be of dimension 3")
        exit(-1)
    # Modify plot
    data.set_sizes((scale*scale0/n) * A.flatten() / np.max(A))
    plt.suptitle("%s\n scale=%g, max=%e"%(os.path.basename(file),scale,np.max(A)))
    # Redraw
    fig.canvas.draw()
    fig.canvas.flush_events()
    # Print image information
    print_info(A,file)


# Display first image (avoid duplicating code)
plot_array(np.load(file),fig,file)
callback_right_button(None)


# Rewire keyboard events
def on_keyboard(event):
    if event.key == 'left' or event.key == 'up':
        callback_left_button(event)
    elif event.key == 'right' or event.key == 'down':
        callback_right_button(event)

plt.gcf().canvas.mpl_connect('key_press_event', on_keyboard)


# Rewire button actions
if(plt.get_backend() == "Qt4Agg"):
    toolbar_elements = fig.canvas.toolbar.children()
    left_button = toolbar_elements[6]
    right_button = toolbar_elements[8]
    left_button.clicked.connect(callback_left_button)
    right_button.clicked.connect(callback_right_button)

# # This doesn't work yet.
# if(plt.get_backend() == "TkAgg"):
#     toolbar_elements = fig.canvas.toolbar.winfo_children() # With tkinter backend
#     left_button = toolbar_elements[6]
#     right_button = toolbar_elements[8]
#     left_button.config(command=callback_left_button)  # Doesn't work while debugging, but works if not debugging
#     right_button.config(command=callback_right_button)


# GUI main loop
plt.show()

hit_enter_to_quit()
