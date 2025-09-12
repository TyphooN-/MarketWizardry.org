#!/bin/bash

# Check if cwebp is installed
if ! command -v cwebp &> /dev/null; then
    echo "Error: cwebp is not installed. Please install it using your package manager."
    echo "On Debian/Ubuntu-based systems, you can install it with:"
    echo "sudo apt-get install webp"
    exit 1
fi

# Set verbose mode if the first argument is -v
VERBOSE=0
if [ "$1" = "-v" ]; then
    VERBOSE=1
fi

# Dry run option
DRY_RUN=0
if [ "$2" = "--dry-run" ] && [ $VERBOSE -eq 1 ]; then
    DRY_RUN=1
    echo "Dry run mode: No files will be converted."
elif [ "$1" = "--dry-run" ]; then
    DRY_RUN=1
    VERBOSE=1
    echo "Dry run mode: No files will be converted."
fi

# Convert all PNG files to WebP recursively
find . -type f -name "*.png" | while read file; do
    # Construct the output filename by replacing .png with .webp
    outfile="${file%.png}.webp"
    
    if [ $VERBOSE -eq 1 ]; then
        echo "Processing file: $file"
    fi
    
    if [ $DRY_RUN -eq 0 ]; then
        # Convert the image using cwebp with default settings
        if cwebp -lossless "$file" -o "$outfile"; then
            if [ $VERBOSE -ge 1 ]; then
                echo "Successfully converted $file to $outfile"
            fi
        else
            echo "Error converting $file to WebP"
            exit 1
        fi
    else
        echo "Would convert: $file -> $outfile"
    fi
done

echo "Conversion completed!"

