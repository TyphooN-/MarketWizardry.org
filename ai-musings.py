import re

def generate_new_files_entries():
    """
    Generates the content for the files object.
    Returns:
        str: The entries as a string formatted for JavaScript.
    """
    # Example entries, replace with your actual data
    entries = [
        "'index.html': { title: 'Home Page', description: 'Main page' },",
        "'about.html': { title: 'About Us', description: 'Company information' },"
        # Add more entries as needed
    ]
    return '\n'.join('  ' + entry for entry in entries)

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
    new_files_content = "const files = {\n" + generate_new_files_entries() + "\n};\n"
    
    new_lines = []
    for i in range(len(lines)):
        if i < start_index:
            new_lines.append(lines[i])
        elif i >= start_index and i <= end_index:
            new_lines.append(new_files_content)
        else:
            new_lines.append(lines[i])
    
    # Write the updated lines back to the file
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("Successfully updated the files object.")

# Example usage
update_files_object('ai-musings.html')
