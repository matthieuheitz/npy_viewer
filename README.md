# npy_viewer
A bunch of utilities to quickly visualize .npy files

### Information

This repository contains pairs of .desktop files and Python scripts,
that allow to open .npy files with a double click and quickly
visualize the array that it contains, as well as statistics about it.
The scripts also work when opening multiple files at once.

The .desktop files follow the [Desktop Entry specifications](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html),
so they should work for most Linux.
It was tested on Ubuntu 16.04.

### Requirements

The scripts are written in Python 3.
The `.desktop` files will use the python that `python3` refers to in your system.
To change that, simply update the path in the `.desktop` files.

##### Packages

Additionally to `numpy` and `matplotlib`, some packages are required for certain scripts:
- NPYCopyAsCSV: `pyperclip csv`

##### Backends

Depending on you system, there might or might not be an exisiting backend that `matplotlib` can use.
It if doesn't find one, it should tell you what to install.

For `NPY3DArrayViewer`, the `TkAgg` backend is a little shaky when changing files, so you might want
to use a Qt backend, such as `Qt4Agg` or `Qt5Agg`.

The `TkAgg` backend requires the deb package `python3-tk`.
The `Qt4Agg` backend requires the deb package `python3-pyqt4`

### Installing

After downloading the repository or indivual files to your computer,
you will need to update the path to the Python script in the corresponding .desktop file :

`Exec = python3 /path/to/python/script.py %U`

Then, copy the desktop files in your Applications folder:

- globally: `/usr/share/applications/` (requires sudo privileges)
- locally: `~/.local/share/applications/`

After that, the application icon should appear in the *Open With...* menu.
You can set it as default to open it with just a double click.

Have fun ! :wink:
