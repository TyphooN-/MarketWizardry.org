#!/usr/bin/env python3

import subprocess
import os

def restore_all_galleries():
    """Restore all user gallery files from commit 741fcd4"""

    # Get list of gallery files from the original commit
    cmd = ["git", "ls-tree", "741fcd4", "nft-gallery/"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return

    gallery_files = []
    for line in result.stdout.strip().split('\n'):
        if '_gallery.html' in line:
            parts = line.split('\t')
            if len(parts) >= 2:
                filename = parts[1]  # Get the filename part
                gallery_files.append(filename)

    print(f"Found {len(gallery_files)} gallery files to restore")

    # Restore each gallery file
    for filename in gallery_files:
        print(f"Restoring {filename}...")
        cmd = ["git", "show", f"714db08:{filename}"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            # Write the file content
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            print(f"✓ Restored {filename}")
        else:
            print(f"✗ Failed to restore {filename}: {result.stderr}")

if __name__ == "__main__":
    restore_all_galleries()