#!/usr/bin/env python3

import os
import subprocess
import re

def get_working_gallery_from_git(artist_name, commit="e27f474"):
    """Get a working gallery file from git history"""
    try:
        result = subprocess.run([
            'git', 'show', f'{commit}:nft-gallery/{artist_name}_gallery.html'
        ], capture_output=True, text=True, cwd='/home/typhoon/git/MarketWizardry.org')
        
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Could not find {artist_name}_gallery.html in commit {commit}")
            return None
    except Exception as e:
        print(f"Error getting {artist_name} from git: {e}")
        return None

def extract_flavor_text(content):
    """Extract flavor text from gallery content"""
    pattern = r'<div class="flavor-text">(.*?)</div>'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def extract_seo_meta(content):
    """Extract SEO meta tags from gallery content"""
    seo_tags = {}
    
    # Extract description
    desc_pattern = r'<meta name="description" content="([^"]*)"'
    match = re.search(desc_pattern, content)
    if match:
        seo_tags['description'] = match.group(1)
    
    # Extract og:description  
    og_desc_pattern = r'<meta property="og:description" content="([^"]*)"'
    match = re.search(og_desc_pattern, content)
    if match:
        seo_tags['og_description'] = match.group(1)
    
    # Extract twitter:description
    twitter_desc_pattern = r'<meta name="twitter:description" content="([^"]*)"'
    match = re.search(twitter_desc_pattern, content)
    if match:
        seo_tags['twitter_description'] = match.group(1)
    
    return seo_tags

def update_working_gallery_with_new_features(working_content, current_content):
    """Update working gallery with new flavor text and SEO while keeping working functionality"""
    
    # Extract new features from current content
    current_flavor_text = extract_flavor_text(current_content)
    current_seo = extract_seo_meta(current_content)
    
    updated_content = working_content
    
    # Update flavor text if we have a new one
    if current_flavor_text:
        # Find old flavor text in working content
        old_flavor_pattern = r'(<div class="flavor-text">)([^<]*)(</div>)'
        if re.search(old_flavor_pattern, updated_content):
            updated_content = re.sub(old_flavor_pattern, f'\\1{current_flavor_text}\\3', updated_content)
        else:
            print("Could not find flavor text section to update")
    
    # Update SEO meta tags
    if current_seo.get('description'):
        desc_pattern = r'(<meta name="description" content=")[^"]*(")'
        updated_content = re.sub(desc_pattern, f'\\1{current_seo["description"]}\\2', updated_content)
    
    if current_seo.get('og_description'):
        og_desc_pattern = r'(<meta property="og:description" content=")[^"]*(")'
        updated_content = re.sub(og_desc_pattern, f'\\1{current_seo["og_description"]}\\2', updated_content)
    
    if current_seo.get('twitter_description'):
        twitter_desc_pattern = r'(<meta name="twitter:description" content=")[^"]*(")'
        updated_content = re.sub(twitter_desc_pattern, f'\\1{current_seo["twitter_description"]}\\2', updated_content)
    
    return updated_content

def restore_gallery(artist_name):
    """Restore a single gallery to working state while preserving new features"""
    
    current_file = f'/home/typhoon/git/MarketWizardry.org/nft-gallery/{artist_name}_gallery.html'
    
    if not os.path.exists(current_file):
        print(f"Current file not found: {current_file}")
        return False
    
    # Get working version from git
    working_content = get_working_gallery_from_git(artist_name)
    if not working_content:
        return False
    
    # Get current content to preserve new features
    with open(current_file, 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # Update working content with new features
    updated_content = update_working_gallery_with_new_features(working_content, current_content)
    
    # Write the restored file
    with open(current_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Restored {artist_name}_gallery.html with preserved new features")
    return True

def main():
    """Restore all galleries to working state while preserving new features"""
    
    gallery_dir = "/home/typhoon/git/MarketWizardry.org/nft-gallery"
    
    updated_count = 0
    total_count = 0
    
    for filename in os.listdir(gallery_dir):
        if filename.endswith("_gallery.html") and filename != "all.html":  # Skip all.html as it's working
            artist_name = filename.replace("_gallery.html", "")
            total_count += 1
            
            if restore_gallery(artist_name):
                updated_count += 1
    
    print(f"\nCompleted: Restored {updated_count} out of {total_count} galleries with preserved new features")

if __name__ == "__main__":
    main()