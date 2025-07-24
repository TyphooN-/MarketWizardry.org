#!/bin/bash

# This script runs the outlier.py script on all .csv files in the current directory.
# It processes the files in parallel for efficiency.

# --- Configuration ---
# Set the maximum number of parallel jobs to the number of CPU cores.
MAX_JOBS=$(nproc)

# --- Functions ---

# Function to process a single file.
process_file() {
    local file="$1"

    echo "Processing $file..."

    # Run the Python script for outlier analysis with --overwrite flag
    # The output is redirected to a .txt file
    python3 outlier.py "$file" --overwrite > "${file%.csv}-outlier.txt"
    
    echo "Finished processing $file."
}

# --- Main Execution ---

# Export the function so it can be used by xargs
export -f process_file

# Find all CSV files in the current directory and process them in parallel using xargs.
# The -P flag sets the maximum number of parallel processes.
find . -maxdepth 1 -type f -name '*.csv' | xargs -I {} -P $MAX_JOBS bash -c 'process_file "{}"'

echo "All outlier analysis tasks have been completed."
