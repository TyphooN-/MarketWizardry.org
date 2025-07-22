#!/bin/bash

# This script runs the outlier.py script on all .csv files in the current directory,
# creating a timestamped backup of each original file first.
# It processes the files in parallel for efficiency.

# --- Configuration ---
# Set the maximum number of parallel jobs.
# Adjust this based on the number of CPU cores you have.
MAX_JOBS=4

# --- Functions ---

# Function to process a single file.
# This includes creating a backup and running the Python script.
process_file() {
    local file="$1"
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local backup_file="${file%.csv}_backup_${timestamp}.csv"

    echo "Processing $file..."

    # Create a backup of the original file
    echo "Backing up '$file' to '$backup_file'..."
    cp "$file" "$backup_file"

    # Run the Python script for outlier analysis
    # The output is redirected to a .txt file
    python3 outlier.py "$file" > "${file%.csv}-outlier.txt"
    
    echo "Finished processing $file."
}

# --- Main Execution ---

# Export the function so it can be used by xargs
export -f process_file

# Find all CSV files in the current directory (that are not backups)
# and process them in parallel using xargs.
# The -P flag sets the maximum number of parallel processes.
find . -maxdepth 1 -type f -name '*.csv' -not -name '*_backup_*.csv' | xargs -I {} -P $MAX_JOBS bash -c 'process_file "{}"'

echo "All outlier analysis tasks have been completed."