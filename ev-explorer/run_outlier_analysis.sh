#!/bin/bash

# This script runs ev_outlier.py and ev_var_outlier.py on all *-EV.csv files in the current directory.
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
    local output_file_ev="${file%.csv}-ev-outlier.txt"
    local output_file_ev_var="${file%.csv}-ev-var-outlier.txt"

    if [ -f "$output_file_ev" ] && [ "$OVERWRITE_OUTPUT" = false ]; then
        echo "Skipping $file for ev_outlier.py: Output file $output_file_ev already exists. Use --overwrite to force."
    else
        echo "Processing $file with ev_outlier.py..."
        python3 ev_outlier.py "$file" > "$output_file_ev"
        echo "Finished processing $file with ev_outlier.py."
    fi

    if [ -f "$output_file_ev_var" ] && [ "$OVERWRITE_OUTPUT" = false ]; then
        echo "Skipping $file for ev_var_outlier.py: Output file $output_file_ev_var already exists. Use --overwrite to force."
    else
        echo "Processing $file with ev_var_outlier.py..."
        python3 ev_var_outlier.py "$file" > "$output_file_ev_var"
        echo "Finished processing $file with ev_var_outlier.py."
    fi
    
    # Remove the source EV CSV file after successful processing of both scripts
    if [ -f "$output_file_ev" ] && [ -f "$output_file_ev_var" ]; then
        rm "$file"
        echo "Removed source EV file: $file"
    fi
}

# --- Main Execution ---

# Export the function and variable so they can be used by xargs
export -f process_file
export OVERWRITE_OUTPUT

# Find all CSV files in the current directory matching *-EV.csv and process them in parallel using xargs.
# The -P flag sets the maximum number of parallel processes.
find . -maxdepth 1 -type f -name '*-EV.csv' | xargs -I {} -P $MAX_JOBS bash -c 'process_file "{}"'

echo "All outlier analysis tasks have been completed."
