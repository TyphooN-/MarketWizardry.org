#!/bin/bash

find . -type f -name "*.webp" | while read file; do
    # Check if the WebP is animated (has multiple frames)
    if webpmux -info "$file" | grep -q "Animation"; then
        echo "Converting $file to GIF..."
        ffmpeg -i "$file" "${file%.webp}.gif"
    fi
done
