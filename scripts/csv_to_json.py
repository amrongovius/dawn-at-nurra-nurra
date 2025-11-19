#!/usr/bin/env python3
"""
Convert CSV with photo captions to JSON format for photobook generation.

Reads: dawn_photos_2024_2025_COMPACT.csv
Outputs: dawn_photos_book.json

Usage:
    python3 csv_to_json.py
"""

import csv
import json
from datetime import datetime
import os


def parse_datetime(dt_string):
    """
    Parse datetime string from various formats.
    
    Expected formats:
    - "YYYY-MM-DD HH:MM:SS"
    - "DD/MM/YYYY HH:MM"
    - ISO format
    
    Returns:
        tuple: (datetime_original, datetime_display, date)
    """
    try:
        # Try ISO format first
        if 'T' in dt_string:
            dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        # Try common formats
        elif '-' in dt_string and ':' in dt_string:
            dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
        elif '/' in dt_string:
            dt = datetime.strptime(dt_string, "%d/%m/%Y %H:%M")
        else:
            # Fallback
            dt = datetime.fromisoformat(dt_string)
        
        # Format outputs
        datetime_original = dt.isoformat()
        datetime_display = dt.strftime("%B %d, %Y, %-I:%M %p")  # "August 17, 2025, 7:03 AM"
        date = dt.strftime("%Y-%m-%d")
        
        return datetime_original, datetime_display, date
    
    except Exception as e:
        print(f"⚠️  Warning: Could not parse datetime '{dt_string}': {e}")
        return None, dt_string, None


def convert_csv_to_json(csv_file, json_file):
    """
    Convert CSV file to JSON format for photobook generation.
    
    CSV should have columns:
    - filename (or similar)
    - datetime (or timestamp)
    - caption (optional)
    """
    
    print("="*70)
    print("📝 CSV TO JSON CONVERTER")
    print("="*70)
    print(f"📂 Reading: {csv_file}")
    print(f"💾 Output: {json_file}")
    print()
    
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found")
        return None
    
    photos = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        # Try to auto-detect CSV format
        sample = f.read(1024)
        f.seek(0)
        
        # Detect delimiter
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample).delimiter
        
        reader = csv.DictReader(f, delimiter=delimiter)
        
        # Get column names (case-insensitive matching)
        headers = {h.lower(): h for h in reader.fieldnames}
        
        print(f"📋 Detected columns: {', '.join(reader.fieldnames)}")
        print(f"📊 Delimiter: '{delimiter}'")
        print()
        
        # Find the right column names (flexible matching)
        filename_col = None
        datetime_col = None
        caption_col = None
        
        # Try to find filename column
        for possible in ['filename', 'file', 'image', 'photo']:
            if possible in headers:
                filename_col = headers[possible]
                break
        
        # Try to find datetime column
        for possible in ['datetime', 'timestamp', 'date', 'time', 'datetime_original']:
            if possible in headers:
                datetime_col = headers[possible]
                break
        
        # Try to find caption column
        for possible in ['caption', 'description', 'text', 'note', 'message']:
            if possible in headers:
                caption_col = headers[possible]
                break
        
        if not filename_col:
            print("❌ Error: Could not find filename column")
            print(f"   Available columns: {', '.join(reader.fieldnames)}")
            return None
        
        print(f"✅ Using columns:")
        print(f"   Filename: '{filename_col}'")
        print(f"   Datetime: '{datetime_col}'" if datetime_col else "   Datetime: Not found (will use filename)")
        print(f"   Caption: '{caption_col}'" if caption_col else "   Caption: Not found (will be empty)")
        print()
        
        print("📸 Processing photos...")
        
        for i, row in enumerate(reader, 1):
            if i % 50 == 0:
                print(f"   ... {i} photos processed")
            
            filename = row[filename_col].strip()
            
            if not filename:
                continue  # Skip empty rows
            
            # Get datetime
            if datetime_col and row[datetime_col]:
                dt_original, dt_display, date = parse_datetime(row[datetime_col].strip())
            else:
                # Try to extract from filename if format is: NNNNNN-PHOTO-YYYY-MM-DD-HH-MM-SS.jpg
                try:
                    parts = filename.replace('.jpg', '').split('-')
                    if len(parts) >= 7 and parts[1] == 'PHOTO':
                        # YYYY-MM-DD-HH-MM-SS
                        dt_str = f"{parts[2]}-{parts[3]}-{parts[4]} {parts[5]}:{parts[6]}:{parts[7]}"
                        dt_original, dt_display, date = parse_datetime(dt_str)
                    else:
                        dt_original, dt_display, date = None, "", None
                except:
                    dt_original, dt_display, date = None, "", None
            
            # Get caption
            caption = ""
            if caption_col and row[caption_col]:
                caption = row[caption_col].strip()
            
            # Build photo entry
            photo_entry = {
                "filename": filename,
                "datetime_display": dt_display,
                "caption": caption
            }
            
            # Add optional fields if available
            if dt_original:
                photo_entry["datetime_original"] = dt_original
            if date:
                photo_entry["date"] = date
            
            photos.append(photo_entry)
        
        print(f"   ✅ {len(photos)} photos processed")
        print()
    
    # Calculate metadata
    if photos:
        dates = [p.get('date') for p in photos if p.get('date')]
        first_date = min(dates) if dates else "Unknown"
        last_date = max(dates) if dates else "Unknown"
    else:
        first_date = "Unknown"
        last_date = "Unknown"
    
    # Create JSON structure
    output = {
        "photos": photos,
        "metadata": {
            "total_photos": len(photos),
            "photos_with_captions": sum(1 for p in photos if p.get('caption')),
            "date_range": {
                "first": first_date,
                "last": last_date
            },
            "created": datetime.now().isoformat(),
            "source": csv_file
        }
    }
    
    # Write JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("="*70)
    print("✅ CONVERSION COMPLETE!")
    print("="*70)
    print(f"📄 Output: {json_file}")
    print(f"📊 Total photos: {len(photos)}")
    print(f"💬 Photos with captions: {sum(1 for p in photos if p.get('caption'))}")
    print(f"📅 Date range: {first_date} → {last_date}")
    print(f"💾 File size: {os.path.getsize(json_file) / 1024:.1f} KB")
    print()
    print("🎉 Ready to generate photobook!")
    print("="*70)
    
    return output


def main():
    """Main function."""
    import sys
    
    # Default file names
    csv_file = 'dawn_photos_2024_2025_COMPACT.csv'
    json_file = 'dawn_photos_book.json'
    
    # Allow command-line arguments
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    if len(sys.argv) > 2:
        json_file = sys.argv[2]
    
    convert_csv_to_json(csv_file, json_file)


if __name__ == '__main__':
    main()
