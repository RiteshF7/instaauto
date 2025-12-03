#!/usr/bin/env python3
"""
Script to migrate captions from text file to JSON for the first 6 images
"""
import json
import os
import re
from datetime import datetime

def parse_text_file_for_images(text_file, image_numbers):
    """Parse the text file and extract data for specific image numbers"""
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    images_data = []
    
    # Split by image separators
    pattern = r'={80}\s+Image #(\d+)\s+Filename: (.+?)\s+Entity: (.+?)\s+Quote: (.+?)\s+-{80}\s+Instagram Caption:\s+(.+?)\s+={80}'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        img_num = int(match.group(1))
        if img_num in image_numbers:
            filename = match.group(2).strip()
            entity = match.group(3).strip()
            quote = match.group(4).strip()
            caption = match.group(5).strip()
            
            # Get image paths
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            images_dir = os.path.join(project_root, "images")
            image_path = os.path.join(images_dir, filename)
            image_path_relative = os.path.relpath(image_path, project_root)
            
            image_data = {
                "image_number": img_num,
                "filename": filename,
                "image_path": image_path,
                "image_path_relative": image_path_relative.replace('\\', '/'),
                "entity": entity,
                "quote": quote,
                "instagram_caption": caption,
                "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            images_data.append(image_data)
    
    return images_data

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    text_file = os.path.join(project_root, "images", "instagram_captions.txt")
    json_file = os.path.join(project_root, "images", "instagram_captions.json")
    
    # Images to migrate (first 6)
    image_numbers = [1, 2, 3, 4, 5, 6]
    
    print(f"Extracting data for images {image_numbers} from text file...")
    new_images = parse_text_file_for_images(text_file, image_numbers)
    
    if not new_images:
        print("No matching images found in text file!")
        return
    
    # Load existing JSON
    existing_data = []
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        print(f"Loaded {len(existing_data)} existing entries from JSON")
    
    # Create a map of existing image numbers
    existing_numbers = {item['image_number'] for item in existing_data}
    
    # Add new images, replacing if they already exist
    for new_img in new_images:
        img_num = new_img['image_number']
        if img_num in existing_numbers:
            # Replace existing entry
            for i, item in enumerate(existing_data):
                if item['image_number'] == img_num:
                    existing_data[i] = new_img
                    print(f"Updated image #{img_num:03d}")
                    break
        else:
            # Insert at the beginning to keep order
            existing_data.insert(0, new_img)
            existing_numbers.add(img_num)
            print(f"Added image #{img_num:03d}")
    
    # Sort by image number
    existing_data.sort(key=lambda x: x['image_number'])
    
    # Save updated JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSuccessfully migrated {len(new_images)} images to JSON file")
    print(f"Total entries in JSON: {len(existing_data)}")

if __name__ == "__main__":
    main()

