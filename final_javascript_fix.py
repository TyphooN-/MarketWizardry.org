#!/usr/bin/env python3

import os
import re
import glob

def final_fix_javascript(file_path):
    """Final comprehensive fix for all JavaScript syntax errors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix addEventListener callback syntax
        content = re.sub(
            r"(document\.addEventListener\('DOMContentLoaded', \(\) => \{[^}]*?if \(document\.body\.offsetHeight < window\.innerHeight\) \{[^}]*?loadMoreImages\(\);)\s*}, 100\)\s*;\s*\}\);",
            r'\1\n            }\n        });',
            content,
            flags=re.DOTALL
        )
        
        content = re.sub(
            r"(window\.addEventListener\('scroll', \(\) => \{[^}]*?if \(window\.innerHeight[^}]*?loadMoreImages\(\);)\s*}, 100\)\s*;\s*\}\);",
            r'\1\n            }\n        });', 
            content,
            flags=re.DOTALL
        )
        
        # Fix function definitions
        content = re.sub(
            r'(function (?:previousImage|nextImage)\(\) \{[^}]*?openImage\(currentImageIndex\);)\s*}, 100\)\s*;',
            r'\1\n        }',
            content,
            flags=re.DOTALL
        )
        
        # Fix keydown event handlers  
        content = re.sub(
            r"(document\.addEventListener\('keydown'[^}]*?break;\s*})\s*}, 100\)\s*;\s*\}\);",
            r'\1\n            }\n        });',
            content,
            flags=re.DOTALL
        )
        
        # Remove orphaned }, 100); fragments
        content = re.sub(r'\s*},\s*100\)\s*;(?=\s*[}\)])', '', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    html_files = glob.glob("**/*.html", recursive=True)
    
    fixed_count = 0
    
    for file_path in html_files:
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if file needs fixing
                if ('}, 100);' in content or 
                    ('addEventListener' in content and '});' in content)):
                    if final_fix_javascript(file_path):
                        print(f"Final fix applied to: {file_path}")
                        fixed_count += 1
                        
            except Exception as e:
                print(f"Error checking {file_path}: {e}")
    
    print(f"\nApplied final JavaScript fixes to {fixed_count} files")

if __name__ == "__main__":
    main()