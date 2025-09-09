#!/usr/bin/env python3

import os
import re
import glob

def fix_javascript_syntax_errors(file_path):
    """Fix the syntax errors introduced by the mobile viewport script"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove the malformed }, 100); fragments that were incorrectly added
        # These appear in various contexts where they break the JavaScript
        
        # Fix setTimeout syntax errors - remove standalone }, 100); fragments
        content = re.sub(r'\s*},\s*100\);\s*(?=\s*[}\)])', '', content)
        
        # Fix other malformed JavaScript fragments
        content = re.sub(r'},\s*100\);\s*$', '', content, flags=re.MULTILINE)
        
        # Clean up any remaining orphaned }, 100); that break syntax
        content = re.sub(r'},\s*100\);\s*(?=[\s\n]*(?:function|var|const|let|\}|\)|;))', '', content)
        
        # Remove }, 100); that appears before closing braces or parentheses
        content = re.sub(r'},\s*100\);\s*(?=[\s\n]*[}\)])', '', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    # Process all HTML files that contain JavaScript
    html_files = glob.glob("**/*.html", recursive=True)
    
    fixed_count = 0
    
    for file_path in html_files:
        if os.path.isfile(file_path):
            try:
                # Check if file contains JavaScript that might have syntax errors
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if '<script>' in content and '}, 100);' in content:
                    if fix_javascript_syntax_errors(file_path):
                        print(f"Fixed JavaScript syntax errors in: {file_path}")
                        fixed_count += 1
                        
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    print(f"\nFixed JavaScript syntax errors in {fixed_count} files")

if __name__ == "__main__":
    main()