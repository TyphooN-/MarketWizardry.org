#!/usr/bin/env python3

import os
import re
import glob

def fix_remaining_syntax_errors(file_path):
    """Fix the remaining syntax errors in JavaScript"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix missing closing braces and parentheses in setTimeout calls
        # Pattern: }, 100); followed by newline and new function/statement
        content = re.sub(r'\s*},\s*100\);\s*$', '            }, 100);', content, flags=re.MULTILINE)
        
        # Fix cases where we have standalone }); without proper closing
        content = re.sub(r'(\s+)loadMoreImages\(\);\s*}\)\s*;', r'\1loadMoreImages();\n\1}, 100);', content)
        
        # Fix cases where setTimeout is missing proper closure
        content = re.sub(r'(\s+)openImage\(currentImageIndex\);\s*}\s*$', r'\1openImage(currentImageIndex);\n\1}, 100);', content, flags=re.MULTILINE)
        
        # Fix the redirect setTimeout that's missing proper structure
        content = re.sub(
            r'(window\.location\.href = `[^`]+`;\s*)\}',
            r'\1            }, 100);\n        }',
            content
        )
        
        # Fix addEventListener callbacks that are missing proper closure  
        content = re.sub(
            r"(if \(window\.innerHeight \+ window\.scrollY >= document\.body\.offsetHeight - scrollThreshold\) \{\s+loadMoreImages\(\);\s*)\}\)\s*;",
            r'\1        }\n        }, 100);',
            content
        )
        
        # Fix other similar addEventListener patterns
        content = re.sub(
            r"(if \(document\.body\.offsetHeight < window\.innerHeight\) \{\s+loadMoreImages\(\);\s*)\}\)\s*;", 
            r'\1        }\n        }, 100);',
            content
        )
        
        # Fix keydown event handlers
        content = re.sub(
            r"(\s+break;\s+\}\s*)\}\)\s*;(\s+\}\);\s*</script>)",
            r'\1        }\n    }, 100);\n\2',
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    # Focus on the files we know have issues from the system reminders
    problem_files = [
        "blog.html", 
        "nft-gallery/PierceLilholt_gallery.html",
        "nft-gallery/AcidSoupArt_gallery.html"
    ]
    
    fixed_count = 0
    
    for file_path in problem_files:
        if os.path.isfile(file_path):
            if fix_remaining_syntax_errors(file_path):
                print(f"Fixed remaining syntax errors in: {file_path}")
                fixed_count += 1
        else:
            print(f"File not found: {file_path}")
    
    # Also check all other HTML files for similar issues
    all_html_files = glob.glob("**/*.html", recursive=True)
    
    for file_path in all_html_files:
        if file_path not in problem_files and os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for common syntax error patterns
                if ('});' in content and 'setTimeout' in content and 
                    ('}});' in content or '})\s*;' in content)):
                    if fix_remaining_syntax_errors(file_path):
                        print(f"Fixed remaining syntax errors in: {file_path}")
                        fixed_count += 1
                        
            except Exception as e:
                print(f"Error checking {file_path}: {e}")
    
    print(f"\nFixed remaining syntax errors in {fixed_count} files")

if __name__ == "__main__":
    main()