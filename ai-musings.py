import re
import os
import glob

def generate_ai_musings_files():
    """
    Generates the files object by scanning the ai-musings directory.
    Returns:
        str: The entries as a string formatted for JavaScript.
    """
    ai_musings_dir = './ai-musings'
    files = []

    if os.path.exists(ai_musings_dir):
        # Get all files in the ai-musings directory
        for file_path in glob.glob(os.path.join(ai_musings_dir, '*')):
            if os.path.isfile(file_path):
                filename = os.path.basename(file_path)
                # Use filename without extension as key, full filename as value
                key = os.path.splitext(filename)[0]
                files.append(f"        '{key}': '{filename}',")

    return '\n'.join(files) if files else '        // No files found'

def update_files_object(html_file_path):
    # Read all lines from the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    start_index = None
    end_index = None
    
    # Find the start of the files object using regex
    pattern_start = re.compile(r'^\s*const\s+files\s*=\s*\{')
    for i, line in enumerate(lines):
        if pattern_start.match(line):
            start_index = i
            break
    
    # If start not found, return early
    if start_index is None:
        print("Could not find the start of the files object.")
        return
    
    # Find the end of the files object (closing brace)
    depth = 0
    for i in range(start_index, len(lines)):
        line = lines[i]
        if re.match(r'^\s*const\s+files\s*=\s*\{', line):
            depth += 1
        elif line.strip() == '}':
            depth -= 1
            if depth < 0:
                end_index = i
                break
    
    # If end not found, return early
    if end_index is None:
        print("Could not find the end of the files object.")
        return
    
    # Update the lines array with new content
    new_files_content = "    const files = {\n" + generate_ai_musings_files() + "\n    };\n"
    
    # Replace the content between start_index and end_index (inclusive)
    new_lines = lines[:start_index] + [new_files_content] + lines[end_index + 1:]
    
    # Write the updated lines back to the file
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("Successfully updated the files object.")

# Example usage
update_files_object('ai-musings.html')
