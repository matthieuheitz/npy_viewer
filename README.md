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
For example:
    `sed -i 's,python3,/usr/local/bin/python3,' NPY*.desktop`

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
the paths to the Python scripts need to be updated in the .desktop files.

You can do so:

- Automagically, by running `setup_npy_scripts.sh`, which will put them in `~/.local/share/applications`
- Manually by changing the lines in the .desktop files.
 `Exec= python3 /path/to/python/script.py %U`

On Ubuntu, the usual directories to put .dekstop files in are :
- `/usr/share/applications/` for all users to access (requires sudo privileges)
- `~/.local/share/applications/` for a specific user

After that, the application icon should appear in the *Open With...* menu.
You can set it as default to open it with just a double click.

Have fun ! :wink:
