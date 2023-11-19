#!/bin/bash

# Install required Python modules
modules=("psutil" "pyyaml" "gputil" "pymongo" "pandas" "scikit-learn")

for module in "${modules[@]}"
do
    if pip install "$module" ; then
        echo "Successfully installed $module"
    else
        echo "Failed to install $module. Please check the installation manually."
    fi
done
