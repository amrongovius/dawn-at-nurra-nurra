#!/usr/bin/env python3
"""
Extract Photo Book Images
Copies only the photos needed for your book from the large WhatsApp folder.
"""

import json
import shutil
import os
from pathlib import Path


def extract_book_images(json_file, source_folder, destination_folder):
    """
    Extract only the images needed for the photo book.
    
    Args:
        json_file: Path to dawn_photos_book.json
        source_folder: Path to folder with ALL WhatsApp images
        destination_folder: Path to folder for ONLY book images
    """
    
    # Load the JSON file
    print(f"📂 Loading photo list from: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    photos = data['photos']
    total_photos = len(photos)
    
    print(f"📸 Found {total_photos} photos in your book")
    
    # Create destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
    print(f"📁 Destination folder: {destination_folder}")
    
    # Extract each image
    copied = 0
    missing = []
    
    print("\n🔍 Searching for images...")
    
    for i, photo in enumerate(photos, 1):
        filename = photo['filename']
        source_path = os.path.join(source_folder, filename)
        dest_path = os.path.join(destination_folder, filename)
        
        # Check if source file exists
        if os.path.exists(source_path):
            # Copy the file
            shutil.copy2(source_path, dest_path)
            copied += 1
            
            # Progress indicator
            if copied % 50 == 0:
                print(f"  ✓ Copied {copied}/{total_photos} images...")
        else:
            missing.append(filename)
    
    # Print summary
    print("\n" + "="*60)
    print("✅ EXTRACTION COMPLETE!")
    print("="*60)
    print(f"✓ Copied: {copied} images")
    print(f"✗ Missing: {len(missing)} images")
    print(f"📁 Location: {destination_folder}")
    print("="*60)
    
    # Show missing files if any
    if missing:
        print("\n⚠️  Missing files (not found in source folder):")
        for filename in missing[:10]:  # Show first 10
            print(f"  - {filename}")
        if len(missing) > 10:
            print(f"  ... and {len(missing) - 10} more")
        print("\n💡 Tip: Check if these files exist in your WhatsApp export folder")
    
    return copied, missing


def main():
    """Main function with user-friendly prompts."""
    import sys
    
    print("="*60)
    print("Photo Book Image Extractor")
    print("="*60)
    print()
    
    # Get file paths from command line or prompt user
    if len(sys.argv) >= 4:
        json_file = sys.argv[1]
        source_folder = sys.argv[2]
        destination_folder = sys.argv[3]
    else:
        print("📋 You need to provide three paths:")
        print("   1. JSON file (dawn_photos_book.json)")
        print("   2. Source folder (your big WhatsApp folder with ALL images)")
        print("   3. Destination folder (where to put ONLY the book images)")
        print()
        print("Usage:")
        print("  python extract_images.py <json_file> <source_folder> <destination_folder>")
        print()
        print("Example:")
        print("  python extract_images.py dawn_photos_book.json WhatsApp_Images/ BookImages/")
        print()
        return
    
    # Check if files/folders exist
    if not os.path.exists(json_file):
        print(f"❌ Error: JSON file not found: {json_file}")
        return
    
    if not os.path.exists(source_folder):
        print(f"❌ Error: Source folder not found: {source_folder}")
        return
    
    # Extract images
    extract_book_images(json_file, source_folder, destination_folder)
    
    print("\n✨ Done! Your book images are ready.")
    print("📦 You can now safely commit these to GitHub without family photos.")


if __name__ == '__main__':
    main()
