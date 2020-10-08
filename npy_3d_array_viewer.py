#!/usr/bin/env python3
"""
This script plots a 3D array as a scatter plot with point size depending on array values.
It also gives statistics about the array.

If multiple files are in parameters, then you can switch between files with the arrows of the figure,
or with the left/right, up/down keys.
"""

import os
import sys
print("Python version:",sys.version)
print("Python interpreter:",sys.executable)
try:
    import matplotlib.pyplot as plt
    import numpy as np
    import time
    from mpl_toolkits.mplot3d import Axes3D
    import cv2

except ImportError as error:
    print(error)
    input("Press any key to exit")
    exit()

# Recommended because the Tk backend is shaky when replotting.
plt.switch_backend("Qt4Agg")
# plt.switch_backend("TkAgg")

num_files = len(sys.argv)-1
f_index = 1
# fig = plt.figure(figsize=(9,6))
fig = plt.figure()
file = sys.argv[1]
data = None
n = N = 0
colorspaces = ["RGB","LAB"]
colorspace = "RGB"
disp_mode = 1   # 0: data on size and no color, 1: data on size and color, 2: data on color, size constant
threshold_enabled = True
threshold = 0
threshold_factor = 2
threshold_disp_below = True
[r, g, b] = [None]*3
colors = None
cb = None
get_minmax_from_array = False
minmax = (0, 1)


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


def hit_enter_to_quit():
    input("Hit Enter to quit ...")
    exit(0)


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


# Makes the graph so that it really displays those exact limits
def get_fix_mins_maxs(mins, maxs):
    deltas = (maxs - mins) / 12.
    mins = mins + deltas / 4.
    maxs = maxs - deltas / 4.
    return [mins, maxs]

# Makes the graph so that it displays extra border like in the default behavior
def get_fix_mins_maxs_default(min, max):
    delta = (max - min) / 20
    return [min - delta, max + delta]


def plot_array(A,fig,file):
    # fig.clf()
    global data
    global n, N
    global threshold
    global r,g,b
    global colors
    global colorspace

    if len(A.shape) != 3:
        print("ERROR: The array should be 3-dimensional ([n1,n2,n3])")
        hit_enter_to_quit()
    n0,n1,n2 = A.shape
    N = n0*n1*n2
    n = np.cbrt(n0*n1*n2)
    t0 = np.linspace(0,1,n0)
    t1 = np.linspace(0,1,n1)
    t2 = np.linspace(0,1,n2)
    [r, g, b] = np.meshgrid(t0, t1, t2, indexing="ij")

    # Guess from the filename if the histogram is Lab or RGB
    if "-lab-" in os.path.basename(file): colorspace = "LAB"
    else: colorspace = "RGB"

    ax = fig.add_subplot(111, projection='3d')
    if colorspace == "RGB":  ax.set_xlabel('R (slow index)'); ax.set_ylabel('G (medium index)'); ax.set_zlabel('B (fast index)');
    elif colorspace == "LAB":  ax.set_xlabel('L (slow index)'); ax.set_ylabel('A (medium index)'); ax.set_zlabel('B (fast index)');

    time0 = time.time()

    scat_r = scat_g = scat_b = None
    scat_colors = None
    scat_scale = None
    scat_cmap = None
    if disp_mode == 0:
        scat_scale = (scale * scale0 / n) * A / np.max(A)
        scat_colors = None
        fig.set_size_inches(8, 6)
    elif disp_mode == 1:
        scat_scale = (scale * scale0 / n) * A / np.max(A)
        if colorspace == "RGB":
            scat_colors = np.vstack((r.flatten(), g.flatten(), b.flatten())).T
        elif colorspace == "LAB":
            C = (np.vstack((r.flatten(), g.flatten(), b.flatten())).T).astype(np.float32)
            C[:,0] *= 100; C[:,1:] = C[:,1:]*255 - 128  # Put in the good range
            scat_colors = cv2.cvtColor(np.expand_dims(C,0), cv2.COLOR_LAB2RGB)[0]
        fig.set_size_inches(8, 6)
    elif disp_mode == 2:
        scat_scale = (scale * scale0 / n)
        scat_colors = A.flatten()
        scat_cmap = 'coolwarm'
        fig.set_size_inches(9, 6)

    # If there is a treshold, apply it on everything
    if threshold_enabled:
        threshold = 1/N    # mean for a uniform distribution
        # Only keep values higher than threshold
        T = A >= threshold if threshold_disp_below else A <= threshold
        scat_r = r[T]; scat_g = g[T]; scat_b = b[T]
        if scat_colors is not None: scat_colors = scat_colors[T.flatten()]
        if disp_mode != 2: scat_scale = scat_scale[T]
        suptitle = "%s\n scale=%.2g, max=%e, threshold=%.2g, disp_ratio=%.2g" % (os.path.basename(file), scale, np.max(A), threshold, np.count_nonzero(T)/np.size(A))
    else:
        suptitle = "%s\n scale=%.2g, max=%e" % (os.path.basename(file), scale, np.max(A))

    data = ax.scatter(scat_r, scat_g, scat_b, s=scat_scale, c=scat_colors, cmap=scat_cmap)
    plt.suptitle(suptitle)
    if not get_minmax_from_array:
        data.axes.set_xlim(minmax); data.axes.set_ylim(minmax); data.axes.set_zlim(minmax)
    if disp_mode == 2:
        global cb
        cb = plt.colorbar(data)

    print("Time = ",time.time() - time0)


def callback_button(event, change_file=None):
    """ this function gets called if we hit the left button"""
    global f_index
    if change_file == "previous":
        # print('Left button pressed')
        if f_index == 1:
            return
        else:
            f_index -= 1
    if change_file == "next":
        # print('Right button pressed')
        if f_index == num_files:
            return
        else:
            f_index += 1

    file = sys.argv[f_index]
    A = np.load(file)
    if A.ndim != 3:
        print("Error: Array must be of dimension 3")
        exit(-1)

    global data
    global r, g, b
    global n, N
    global colors
    global colorspace
    # If points have changed
    if A.shape != r.shape:
        n0,n1,n2 = A.shape
        N = n0*n1*n2
        n = np.cbrt(n0*n1*n2)
        t0 = np.linspace(0,1,n0)
        t1 = np.linspace(0,1,n1)
        t2 = np.linspace(0,1,n2)
        [r, g, b] = np.meshgrid(t0, t1, t2, indexing="ij")

    # Choose color depending on filename, but only when switching files.
    # If I don't add this condition, I can never visualize an RGB file in LAB,
    # which can be useful if the file doesn't have -lab- in it, but is still LAB.
    if change_file:
        # Guess from the filename if the histogram is Lab or RGB
        if "-lab-" in os.path.basename(file): colorspace = "LAB"
        else: colorspace = "RGB"

    scat_r = r
    scat_g = g
    scat_b = b
    scat_colors = None
    scat_scale = None
    scat_cmap = None
    # Remove the colorbar if there is one
    if data.colorbar:
        data.colorbar.remove()
        fig.subplots_adjust()

    if disp_mode == 0:
        scat_scale = (scale * scale0 / n) * A / np.max(A)
        scat_colors = None
        fig.set_size_inches(8, 6)
    elif disp_mode == 1:
        scat_scale = (scale * scale0 / n) * A / np.max(A)
        if colorspace == "RGB":
            scat_colors = np.vstack((r.flatten(), g.flatten(), b.flatten())).T
        elif colorspace == "LAB":
            C = (np.vstack((r.flatten(), g.flatten(), b.flatten())).T).astype(np.float32)
            C[:,0] *= 100; C[:,1:] = C[:,1:]*255 - 128  # Put in the good range
            scat_colors = cv2.cvtColor(np.expand_dims(C,0), cv2.COLOR_LAB2RGB)[0]
        fig.set_size_inches(8, 6)
    elif disp_mode == 2:
        scat_scale = (scale * scale0 / n)
        scat_colors = A.flatten()
        scat_cmap = 'coolwarm'
        fig.set_size_inches(10, 6)


    # If there is a treshold, apply it on everything
    if threshold_enabled:
        # threshold = 1/N
        # Only keep values higher than threshold
        T = A >= threshold if threshold_disp_below else A <= threshold
        scat_r = r[T]; scat_g = g[T]; scat_b = b[T]
        if scat_colors is not None: scat_colors = scat_colors[T.flatten()]
        if disp_mode != 2: scat_scale = scat_scale[T]
        suptitle = "%s\n scale=%.2g, max=%e, threshold=%.2g, disp_ratio=%.2g" % (os.path.basename(file), scale, np.max(A), threshold, np.count_nonzero(T)/np.size(A))
    else:
        suptitle = "%s\n scale=%.2g, max=%e" % (os.path.basename(file), scale, np.max(A))

    # print("scat_r.shape:",scat_r.shape)
    # print("scat_g.shape:",scat_g.shape)
    # print("scat_b.shape:",scat_b.shape)
    # print("scat_scale.shape:",scat_scale.shape)
    # print("scat_colors.shape:",scat_colors.shape)
    data.axes.cla()
    # fig.clf()
    data = data.axes.scatter(scat_r, scat_g, scat_b, s=scat_scale, c=scat_colors, cmap=scat_cmap)
    # data.axes.scatter(scat_r, scat_g, scat_b, s=scat_scale, c=scat_colors)
    if colorspace == "RGB":  data.axes.set_xlabel('R (slow index)'); data.axes.set_ylabel('G (medium index)'); data.axes.set_zlabel('B (fast index)')
    elif colorspace == "LAB":  data.axes.set_xlabel('L (slow index)'); data.axes.set_ylabel('A (medium index)'); data.axes.set_zlabel('B (fast index)')

    plt.suptitle(suptitle)
    if not get_minmax_from_array:
        data.axes.set_xlim(minmax); data.axes.set_ylim(minmax); data.axes.set_zlim(minmax)
    if disp_mode == 2:
        global cb
        plt.colorbar(data)


    # # Compute colors
    # colors = (np.vstack((r.flatten(), g.flatten(), b.flatten())).T if disp_mode == 1 else None)
    #
    # # Modify plot
    # if disp_threshold:
    #     T = A > threshold
    #     data.axes.cla()
    #     if colors is not None: colors = colors[T.flatten()]
    #     data.axes.scatter(r[T], g[T], b[T], s=(scale * scale0 / n) * A[T] / np.max(A), c=colors)
    #     if not get_minmax_from_array:
    #         data.axes.set_xlim(minmax); data.axes.set_ylim(minmax); data.axes.set_zlim(minmax)
    #     plt.suptitle("%s\n scale=%.2g, threshold=%.2g, disp_ratio=%.2g" % (os.path.basename(file), scale, threshold, np.count_nonzero(T)/np.size(A)))
    #     data.axes.set_xlabel('R (slow index)'); data.axes.set_ylabel('G (medium index)'); data.axes.set_zlabel('B (fast index)')
    # else:
    #     data.set_sizes((scale*scale0/n) * A.flatten() / np.max(A))

    # plt.suptitle("%s\n scale=%g, max=%e"%(os.path.basename(file),scale,np.max(A)))
    # Redraw
    fig.canvas.draw()
    fig.canvas.flush_events()
    # Print image information if file has changed
    if change_file:
        print_info(A,file)


def callback_left_button(event):
    callback_button(event, "previous")


def callback_right_button(event):
    callback_button(event, "next")


# See shorcuts already taken :
# https://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
def callback_disp_help(event):
    print("NPY 3D Viewer")
    print("-------------")
    print("Valid keystrokes:")
    print("'\u2192','\u2193': Next file")
    print("'\u2190','\u2191': Previous file")
    print("'d': Switch between data display modes")
    print("'c': Switch between color spaces")
    print("'/': Decrease point size")
    print("'*': Increase point size")
    print("'p': Enter new point size")
    print("'-': Increase display value threshold (decrease number of points)")
    print("'+': Decrease display value threshold (increase number of points)")
    print("'T': Toggle threshold use")
    print("'%': Display above or below threshold")
    print("'t': Enter new threshold")
    print("'m': Enter new threshold (multiplying) factor when increasing/decreasing")
    print("'h': Display this help")
    print("Matplotlib defaults")
    print("'f': Enter fullscreen")
    print("'s': Save figure")
    print("'q': Quit window")



def callback_scale_button(event):
    global scale
    if event.key == '/':    scale /= 1.5
    if event.key == '*':    scale *= 1.5
    if event.key == 'p':
        print("Scale for point size : %03f" % scale)
        key = input("Enter new scale ? (just hit enter if not) : ")
        if is_number(key):
            scale = float(key)

    # Refresh
    callback_button(event)

def callback_disp_threshold_button(event):
    global threshold
    global threshold_factor
    global threshold_enabled
    global threshold_disp_below
    if event.key == '-':    threshold /= threshold_factor
    if event.key == '+':    threshold *= threshold_factor
    if event.key == 'T':    threshold_enabled = not threshold_enabled
    if event.key == 't':
        print("Threshold for point display: %g" % threshold)
        key = input("Enter new threshold ? (just hit enter if not) : ")
        if is_number(key):
            threshold = float(key)
    if event.key == 'm':
        print("Multiplying factor when increasing and decreasing threshold: %g" % threshold)
        key = input("Enter new threshold factor ? (just hit enter if not) : ")
        if is_number(key):
            threshold_factor = float(key)
    if event.key == "%" :
        threshold_disp_below = not threshold_disp_below

    # Refresh
    callback_button(event)

def callback_disp_mode(event):

    global disp_mode
    disp_mode = (disp_mode+1) % 3     # Switch between 0, 1, and 2

    # Refresh
    callback_button(event)


def callback_colorspace(event):

    global colorspace
    colorspace = colorspaces[(colorspaces.index(colorspace)+1)%len(colorspaces)]     # Switch between colorspaces

    # Refresh
    callback_button(event)


def on_keyboard(event):
    # print('You pressed', event.key, event.xdata, event.ydata)
    if event.key in {'left', 'up'}:
        callback_left_button(event)
    elif event.key in {'right', 'down'}:
        callback_right_button(event)
    elif event.key in {'/', '*', 'p'}:
        callback_scale_button(event)
    elif event.key in {'+', '-', 't', 'T', 'm','%'}:
        callback_disp_threshold_button(event)
    elif event.key in {'d'}:
        callback_disp_mode(event)
    elif event.key in {'h'}:
        callback_disp_help(event)
    elif event.key in {'c'}:
        callback_colorspace(event)


# Initialize variables
# minmax = get_fix_mins_maxs(minmax[0], minmax[1])
minmax = get_fix_mins_maxs_default(minmax[0], minmax[1])
# minmax = (minmax[0], minmax[1])

# Display first image (avoid duplicating code)
im = np.load(file)
plot_array(im,fig,file)

# Print image information
print_info(im, file)

# Rewire keyboard events
plt.gcf().canvas.mpl_connect('key_press_event', on_keyboard)

# Rewire actions for toolbar arrow buttons
# if plt.get_backend() == "Qt4Agg":
#     toolbar_elements = fig.canvas.toolbar.children()
#     left_button = toolbar_elements[6]
#     right_button = toolbar_elements[8]
#     left_button.clicked.connect(callback_left_button)
#     right_button.clicked.connect(callback_right_button)

# # This doesn't work yet.
# if(plt.get_backend() == "TkAgg"):
#     toolbar_elements = fig.canvas.toolbar.winfo_children() # With tkinter backend
#     left_button = toolbar_elements[6]
#     right_button = toolbar_elements[8]
#     left_button.config(command=callback_left_button)  # Doesn't work while debugging, but works if not debugging
#     right_button.config(command=callback_right_button)


# GUI main loop
plt.show()
