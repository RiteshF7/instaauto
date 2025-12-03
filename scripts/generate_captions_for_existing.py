#!/usr/bin/env python3
"""
Script to generate Instagram captions for existing images that don't have captions yet
This reads existing images and generates captions for them
"""
import sys
import os
# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add parent directory to path to import services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import time
import json
from services.quote_service import QuoteService
from dotenv import load_dotenv

load_dotenv(override=True)

def print_progress(current, total, prefix='Progress', suffix='', length=50):
    """Print a progress bar"""
    percent = f"{100 * (current / float(total)):.1f}"
    filled = int(length * current // total)
    bar = '█' * filled + '░' * (length - filled)
    print(f'\r{prefix} |{bar}| {current}/{total} ({percent}%) {suffix}', end='', flush=True)
    if current == total:
        print()  # New line when complete

def extract_info_from_filename(filename):
    """Extract image number and entity from filename"""
    # Pattern: image_001_Entity_quote_snippet.png
    match = re.match(r'image_(\d+)_(.+?)_(.+)\.png', filename)
    if match:
        return int(match.group(1)), match.group(2), match.group(3)
    return None, None, None

def main():
    """Generate captions for existing images"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(project_root, "images")
    captions_file = os.path.join(images_dir, "instagram_captions.txt")  # Keep for backward compatibility
    json_file = os.path.join(images_dir, "instagram_captions.json")
    
    if not os.path.exists(images_dir):
        print(f"❌ Images directory not found: {images_dir}")
        sys.exit(1)
    
    # Get all PNG images
    image_files = [f for f in os.listdir(images_dir) if f.endswith('.png') and f.startswith('image_')]
    image_files.sort()
    
    if not image_files:
        print("❌ No image files found in images directory")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("📝 Generating Instagram Captions for Existing Images")
    print("="*60)
    print(f"📁 Found {len(image_files)} images")
    print(f"📝 Text captions will be saved to: {os.path.abspath(captions_file)}")
    print(f"📄 JSON data will be saved to: {os.path.abspath(json_file)}")
    print("="*60)
    
    # Check if API key is set
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in environment variables.")
        print("Please set GEMINI_API_KEY in your .env file")
        sys.exit(1)
    
    # Initialize service
    print("\nInitializing QuoteService...")
    quote_service = QuoteService()
    print("Service initialized successfully\n")
    
    # Read existing captions file if it exists to avoid duplicates
    existing_captions = set()
    if os.path.exists(captions_file):
        with open(captions_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract image numbers that already have captions
            for match in re.finditer(r'Image #(\d+)', content):
                existing_captions.add(int(match.group(1)))
        print(f"Found {len(existing_captions)} existing captions in file")
    
    # Initialize JSON file
    json_data = []
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            print(f"📄 Loaded {len(json_data)} existing entries from JSON file")
        except json.JSONDecodeError:
            print("⚠️  JSON file exists but is invalid. Starting fresh.")
            json_data = []
    
    # Initialize or append to text captions file (for backward compatibility)
    mode = 'a' if os.path.exists(captions_file) else 'w'
    if mode == 'w':
        with open(captions_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("INSTAGRAM CAPTIONS FOR GENERATED IMAGES\n")
            f.write("="*80 + "\n")
            f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total images: {len(image_files)}\n")
            f.write("="*80 + "\n\n")
    
    # Filter out images that already have captions
    images_to_process = []
    for image_file in image_files:
        image_num, entity, quote_snippet = extract_info_from_filename(image_file)
        if image_num is not None and image_num not in existing_captions:
            images_to_process.append((image_file, image_num, entity))
    
    total_to_process = len(images_to_process)
    print(f"\n📊 Processing {total_to_process} images (skipping {len(existing_captions)} with existing captions)")
    print("="*60 + "\n")
    
    if total_to_process == 0:
        print("✅ All images already have captions!")
        return
    
    successful = 0
    skipped = len(existing_captions)
    failed = 0
    start_time = time.time()
    
    for idx, (image_file, image_num, entity) in enumerate(images_to_process, 1):
        # Calculate progress
        elapsed_time = time.time() - start_time
        if idx > 1:
            avg_time_per_image = elapsed_time / (idx - 1)
            remaining = total_to_process - idx
            eta_seconds = avg_time_per_image * remaining
            eta_str = f"ETA: {int(eta_seconds // 60)}m {int(eta_seconds % 60)}s"
        else:
            eta_str = "ETA: calculating..."
        
        # Print progress bar
        print_progress(idx, total_to_process, prefix='Progress', suffix=eta_str)
        
        # Print detailed info
        print(f"\n{'='*60}")
        print(f"[{idx}/{total_to_process}] Processing image #{image_num:03d}")
        print(f"{'='*60}")
        print(f"📁 File: {image_file}")
        print(f"🌌 Entity: {entity}")
        
        try:
            # We need to regenerate the quote to get the caption
            # Since we don't have the full quote, we'll use the entity
            from config.prompts import SPACE_ENTITIES
            if entity in SPACE_ENTITIES:
                print("⏳ Generating quote...")
                quote = quote_service.generate_quote(entity, '')
                print(f"✅ Quote generated: {quote[:60]}...")
                
                print("⏳ Generating Instagram caption...")
                caption = quote_service.generate_caption(quote)
                print("✅ Caption generated")
                
                # Get full image path
                image_path = os.path.join(images_dir, image_file)
                image_path_relative = os.path.relpath(image_path, project_root)
                
                # Create JSON object
                image_data = {
                    "image_number": image_num,
                    "filename": image_file,
                    "image_path": image_path,
                    "image_path_relative": image_path_relative,
                    "entity": entity,
                    "quote": quote,
                    "instagram_caption": caption,
                    "generated_at": time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Check if entry already exists in JSON data
                existing_index = None
                for idx, entry in enumerate(json_data):
                    if entry.get("image_number") == image_num:
                        existing_index = idx
                        break
                
                if existing_index is not None:
                    json_data[existing_index] = image_data
                    print(f"🔄 Updated JSON entry for image #{image_num:03d}")
                else:
                    json_data.append(image_data)
                    print(f"➕ Added JSON entry for image #{image_num:03d}")
                
                # Save to JSON file
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
                
                # Also save to text file for backward compatibility
                with open(captions_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n{'='*80}\n")
                    f.write(f"Image #{image_num:03d}\n")
                    f.write(f"Filename: {image_file}\n")
                    f.write(f"Entity: {entity}\n")
                    f.write(f"Quote: {quote}\n")
                    f.write(f"{'-'*80}\n")
                    f.write(f"Instagram Caption:\n{caption}\n")
                    f.write(f"{'='*80}\n")
                
                print(f"💾 Saved caption for image #{image_num:03d} (JSON + text)")
                successful += 1
            else:
                print(f"⚠️  Entity '{entity}' not found in SPACE_ENTITIES")
                failed += 1
                
        except Exception as e:
            print(f"❌ Error processing image #{image_num:03d}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        
        # Small delay to avoid rate limiting
        if idx < total_to_process:
            print("⏳ Waiting 1 second...")
            time.sleep(1)
        
        print()  # Empty line for readability
    
    # Summary
    total_time = time.time() - start_time
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    
    print("\n" + "="*60)
    print("📊 Caption Generation Complete!")
    print("="*60)
    print(f"✅ Successful: {successful}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"⏱️  Total time: {minutes}m {seconds}s")
    if successful > 0:
        avg_time = total_time / successful
        print(f"⏱️  Average time per image: {avg_time:.1f}s")
    print(f"📝 Text captions saved in: {os.path.abspath(captions_file)}")
    print(f"📄 JSON data saved in: {os.path.abspath(json_file)}")
    print(f"📊 Total entries in JSON: {len(json_data)}")
    print("="*60)

if __name__ == "__main__":
    main()

