# npy_viewer
A bunch of utilities to quickly visualize .npy files

### Information

This repository contains pairs of .desktop files and Python scripts,
that allow to open .npy files with a double click and quickly
visualize the array that it contains, as well as statistics about it.

The .desktop files follow the [Desktop Entry specifications](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html),
so they should work for most Linux.
It was tested on Ubuntu 16.04.

The Python scripts are written for Python 2, but they can be easily changed to work for Python 3.

### Installing

After downloading the repository or indivual files to your computer,
you will need to update the path to the Python script in the corresponding .desktop file :

`Exec = python2 /path/to/python/script.py %U`

Then, copy the desktop file in your Applications folder.

On Ubuntu : `sudo cp /path/to/npy_viewer/NPYFileViewer.desktop /usr/share/applications/`

After that, the application icon should appear in the *Open With...* menu.
You can set it as default to open it with just a double click.

Have fun ! :wink:
