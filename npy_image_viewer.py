#!/usr/bin/env python3
'''
This script plots a 2D array as an image.
It also gives statistics about the array.

If multiple files are in parameters, then you can switch between files with the arrows of the figure,
or with the left/right, up/down keys.
'''

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Choose your backend
plt.switch_backend("Qt4Agg")


num_files = len(sys.argv)-1
f_index = 0
fig = plt.figure()
data = plt.imshow(np.load(sys.argv[1]),cmap='gray')


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


def callback_left_button(event):
    ''' this function gets called if we hit the left button'''
    # print('Left button pressed')
    global f_index
    if f_index == 1:
        return
    else:
        f_index -= 1

    file = sys.argv[f_index]
    A = np.load(file)
    data.set_data(A)
    plt.title(os.path.basename(file))
    # Redraw
    fig.canvas.draw()
    fig.canvas.flush_events()
    # Print image information
    print_info(A,file)


def callback_right_button(event):
    ''' this function gets called if we hit the left button'''
    # print('Right button pressed')
    global f_index
    global data
    if f_index == num_files:
        return
    else:
        f_index += 1

    file = sys.argv[f_index]
    A = np.load(file)
    data.set_data(A)
    plt.title(os.path.basename(file))
    # Redraw
    fig.canvas.draw()
    fig.canvas.flush_events()
    # Print image information
    print_info(A,file)


# Display first image (avoid duplicating code)
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

if sys.platform.startswith('linux'):
    input("Hit Enter to quit ...")
