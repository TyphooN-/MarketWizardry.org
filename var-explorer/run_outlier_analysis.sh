#!/bin/bash

# This script runs the outlier.py script on all .csv files in the current directory.

for file in *.csv; do
    if [ -f "$file" ]; then
        echo "Processing $file..."
        python3 outlier.py "$file" > "${file%.csv}-outlier.txt"
    fi
done

echo "Processing complete."
