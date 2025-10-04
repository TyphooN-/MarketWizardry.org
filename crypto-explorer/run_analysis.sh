#!/bin/bash

# This script runs the analyze.py script on all crypto CSV files in the current directory.
# It processes the files in parallel for efficiency.

# --- Configuration ---
# Set the maximum number of parallel jobs to the number of CPU cores.
MAX_JOBS=$(nproc)
OVERWRITE_OUTPUT=false

# --- Parse Arguments ---
for arg in "$@"; do
  case $arg in
    --overwrite)
      OVERWRITE_OUTPUT=true
      shift # Remove --overwrite from processing
      ;;
  esac
done

# --- Functions ---

# Function to process a single file.
process_file() {
    local file="$1"
    local output_file="${file%.csv}-analysis.txt"

    if [ -f "$output_file" ] && [ "$OVERWRITE_OUTPUT" = false ]; then
        echo "Skipping $file: Output file $output_file already exists. Use --overwrite to force."
        return
    fi

    echo "Processing $file..."

    # Run the Python script for crypto analysis
    # The output is redirected to a .txt file
    python3 analyze.py "$file" > "$output_file"

    echo "Finished processing $file."
}

# --- Main Execution ---

# Export the function and variable so they can be used by xargs
export -f process_file
export OVERWRITE_OUTPUT

echo "Processing crypto CSV files from current directory..."
# Find all crypto CSV files in the current directory and process them in parallel using xargs.
# The -P flag sets the maximum number of parallel processes.
find . -maxdepth 1 -type f -name '*-Crypto-*.csv' | xargs -I {} -P $MAX_JOBS bash -c 'process_file "{}"'

echo "All crypto analysis tasks have been completed."
