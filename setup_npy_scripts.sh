#!/bin/bash

# Get directory where this script is.
scripts_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Directory where the .dekstop files will be copied
target_dir=~/.local/share/applications

echo "Copying .desktop files to $target_dir."
cp $scripts_dir/NPY*.desktop $target_dir/

echo "Linking the .desktop files to this directory"
# sed takes whatever follows the "s" as the separator
sed -i "s,/path/to/npy_viewer,$scripts_dir,g" $target_dir/NPY*.desktop

echo "Done !"
echo "To remove them, run :"
echo -e "\t rm ~/.local/share/applications/NPY*.desktop"
