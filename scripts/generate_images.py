#!/usr/bin/env python3
"""
Script to generate 60 images using the "Surprise Me" functionality
Each image will be saved to the images/ directory in the project root
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

import random
import time
import json
from services.quote_service import QuoteService
from services.image_service import ImageService
from services.text_overlay_service import TextOverlayService
from config.prompts import SPACE_ENTITIES
from dotenv import load_dotenv

load_dotenv(override=True)

def sanitize_filename(text, max_length=50):
    """Sanitize text for use in filename"""
    # Remove or replace invalid filename characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        text = text.replace(char, '_')
    # Remove quotes and extra spaces
    text = text.replace('"', '').replace("'", '').strip()
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length]
    return text

def generate_and_save_image(index, total, images_dir, captions_file, json_file, json_data, quote_service, image_service, text_overlay_service):
    """Generate one image and save it, along with its caption"""
    print(f"\n{'='*60}")
    print(f"Generating image {index + 1}/{total}")
    print(f"{'='*60}")
    
    try:
        # Pick a random entity (same as "Surprise Me" button)
        entity = random.choice(SPACE_ENTITIES)
        print(f"Selected entity: {entity}")
        
        # Generate quote (using 'random' prompt which will pick random entity)
        print("Generating quote...")
        quote = quote_service.generate_quote('random', '')
        print(f"Generated quote: {quote[:80]}...")
        
        # Generate Instagram caption
        print("Generating Instagram caption...")
        caption = quote_service.generate_caption(quote)
        print("Caption generated successfully")
        
        # Generate image
        print("Generating image...")
        generated_image = image_service.generate_image(quote)
        print("Image generated successfully")
        
        # Overlay text on image
        print("Overlaying text...")
        final_image = text_overlay_service.overlay_text(generated_image, quote)
        print("Text overlaid successfully")
        
        # Create filename
        # Use entity name and first few words of quote
        quote_snippet = sanitize_filename(quote[:30])
        filename = f"image_{index + 1:03d}_{entity}_{quote_snippet}.png"
        filepath = os.path.join(images_dir, filename)
        
        # Save image
        final_image.save(filepath, "PNG")
        print(f"✅ Saved: {filepath}")
        
        # Get image paths
        image_path_relative = os.path.relpath(filepath, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Create JSON object with all information
        image_data = {
            "image_number": index + 1,
            "filename": filename,
            "image_path": filepath,
            "image_path_relative": image_path_relative,
            "entity": entity,
            "quote": quote,
            "instagram_caption": caption,
            "generated_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to JSON data array
        json_data.append(image_data)
        
        # Save JSON file (overwrite each time to keep it updated)
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # Also save to text file for backward compatibility
        with open(captions_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Image #{index + 1:03d}\n")
            f.write(f"Filename: {filename}\n")
            f.write(f"Entity: {entity}\n")
            f.write(f"Quote: {quote}\n")
            f.write(f"{'-'*80}\n")
            f.write(f"Instagram Caption:\n{caption}\n")
            f.write(f"{'='*80}\n")
        
        print(f"✅ Caption saved to: {captions_file}")
        print(f"✅ JSON data updated: {json_file}")
        
        return True, quote, caption
        
    except Exception as e:
        print(f"❌ Error generating image {index + 1}: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None

def check_if_running():
    """Check if another instance of this script is already running"""
    try:
        import psutil
        current_pid = os.getpid()
        script_name = os.path.basename(__file__)
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['pid'] == current_pid:
                    continue
                cmdline = proc.info.get('cmdline', [])
                if cmdline and any(script_name in str(arg) or 'generate_images' in str(arg) for arg in cmdline):
                    print(f"⚠️  Another instance of {script_name} is already running (PID: {proc.info['pid']})")
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False
    except ImportError:
        # psutil not available, use simple file-based lock instead
        lock_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".generate_images.lock")
        if os.path.exists(lock_file):
            # Check if lock file is stale (older than 1 hour)
            import time
            if time.time() - os.path.getmtime(lock_file) > 3600:
                os.remove(lock_file)
            else:
                print("⚠️  Lock file exists. Another instance may be running.")
                return True
        # Create lock file
        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))
        return False

def main():
    """Main function to generate 60 images"""
    # Check if another instance is running
    if check_if_running():
        print("❌ Another instance is already running. Exiting...")
        sys.exit(1)
    
    # Create lock file if using file-based locking
    lock_file = None
    try:
        import psutil
    except ImportError:
        lock_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".generate_images.lock")
        # Create lock file
        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))
    
    try:
        # Create images directory if it doesn't exist (in project root)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        images_dir = os.path.join(project_root, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        # Create captions file paths
        captions_file = os.path.join(images_dir, "instagram_captions.txt")  # Text file for backward compatibility
        json_file = os.path.join(images_dir, "instagram_captions.json")  # JSON file with structured data
        
        # Change to project root directory for relative paths
        os.chdir(project_root)
        
        print("\n" + "="*60)
        print("🚀 Starting batch image generation")
        print("="*60)
        print(f"📁 Images will be saved to: {os.path.abspath(images_dir)}")
        print(f"📝 Text captions will be saved to: {os.path.abspath(captions_file)}")
        print(f"📄 JSON data will be saved to: {os.path.abspath(json_file)}")
        print(f"🎯 Generating 60 images...")
        print("="*60)
        
        # Check if API key is set
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ ERROR: GEMINI_API_KEY not found in environment variables.")
            print("Please set GEMINI_API_KEY in your .env file")
            sys.exit(1)
        
        # Initialize JSON data array
        json_data = []
        
        # Initialize captions text file with header (for backward compatibility)
        with open(captions_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("INSTAGRAM CAPTIONS FOR GENERATED IMAGES\n")
            f.write("="*80 + "\n")
            f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total images: 60\n")
            f.write("="*80 + "\n\n")
        
        # Initialize services once (reuse for all images)
        print("\nInitializing services...")
        quote_service = QuoteService()
        image_service = ImageService()
        text_overlay_service = TextOverlayService()
        print("Services initialized successfully\n")
        
        successful = 0
        failed = 0
        
        # Generate 60 images
        for i in range(60):
            result = generate_and_save_image(i, 60, images_dir, captions_file, json_file, json_data, quote_service, image_service, text_overlay_service)
            if result[0]:  # Check if successful
                successful += 1
                # json_data is modified in place, no need to update
            else:
                failed += 1
            
            # Add a small delay between requests to avoid rate limiting
            if i < 59:  # Don't wait after the last image
                print(f"\n⏳ Waiting 2 seconds before next generation...")
                time.sleep(2)
        
        # Summary
        print("\n" + "="*60)
        print("📊 Generation Complete!")
        print("="*60)
        print(f"✅ Successful: {successful}/60")
        print(f"❌ Failed: {failed}/60")
        print(f"📁 Images saved in: {os.path.abspath(images_dir)}")
        print(f"📝 Text captions saved in: {os.path.abspath(captions_file)}")
        print(f"📄 JSON data saved in: {os.path.abspath(json_file)}")
        print(f"📊 Total entries in JSON: {len(json_data)}")
        print("="*60)
    
    finally:
        # Remove lock file if it exists
        if lock_file and os.path.exists(lock_file):
            try:
                os.remove(lock_file)
            except:
                pass

if __name__ == "__main__":
    main()

