#!/usr/bin/env python3
"""
Dawn at Nurra Nurra - FULL PRODUCTION SCRIPT
Generates complete 336-page photobook PDF from your 330 photos

REQUIREMENTS:
- BookImages/ folder with all 330 photos
- dawn_photos_book.json with photo data
- Python 3 with reportlab and pillow installed

USAGE:
python3 create_full_photobook.py
"""

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image
import json
import os
from datetime import datetime

pdfmetrics.registerFont(TTFont('Roboto', 'Roboto-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Bold', 'Roboto-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Light', 'Roboto-Light.ttf'))

# ===== BLURB SPECIFICATIONS =====
PDF_WIDTH = 24.447 * cm
PDF_HEIGHT = 20.955 * cm
TRIM_WIDTH = 24.13 * cm
TRIM_HEIGHT = 20.321 * cm
BLEED = 0.317 * cm
SAFE_MARGIN_OUTSIDE = 0.635 * cm
SAFE_MARGIN_BINDING = 1.27 * cm

# Image specifications
IMAGE_WIDTH = 7 * inch
IMAGE_ASPECT_RATIO = 4/3
IMAGE_HEIGHT = IMAGE_WIDTH / IMAGE_ASPECT_RATIO

# Typography
TEXT_COLOR = HexColor('#F5F5F5')
DATETIME_SIZE = 12
CAPTION_SIZE = 11
LINE_SPACING = 1.4
IMAGE_TEXT_GAP = 0.375 * inch


def get_top_left_pixel_color(image_path):
    """Extract the color of the top-left pixel from an image."""
    try:
        img = Image.open(image_path)
        pixel = img.getpixel((0, 0))
        hex_color = '#%02x%02x%02x' % pixel[:3]
        return HexColor(hex_color)
    except Exception as e:
        print(f"⚠️  Warning: Could not read color from {os.path.basename(image_path)}: {e}")
        return HexColor('#2B2B2B')  # Fallback color


def get_safe_content_area(is_right_page=True):
    """Calculate the safe content area within the page."""
    trim_left = BLEED
    trim_bottom = BLEED
    
    if is_right_page:
        safe_left = trim_left + SAFE_MARGIN_BINDING
        safe_right = trim_left + TRIM_WIDTH - SAFE_MARGIN_OUTSIDE
    else:
        safe_left = trim_left + SAFE_MARGIN_OUTSIDE
        safe_right = trim_left + TRIM_WIDTH - SAFE_MARGIN_BINDING
    
    safe_bottom = trim_bottom + SAFE_MARGIN_OUTSIDE
    safe_top = trim_bottom + TRIM_HEIGHT - SAFE_MARGIN_OUTSIDE
    
    safe_width = safe_right - safe_left
    safe_height = safe_top - safe_bottom
    
    return safe_left, safe_bottom, safe_width, safe_height


def draw_blank_page(c, bg_color):
    """Draw a blank page with the specified background color."""
    c.setFillColor(bg_color)
    c.rect(0, 0, PDF_WIDTH, PDF_HEIGHT, fill=1, stroke=0)


def draw_title_dedication_page(c, bg_color):
    """Draw the title and dedication page."""
    c.setFillColor(bg_color)
    c.rect(0, 0, PDF_WIDTH, PDF_HEIGHT, fill=1, stroke=0)
    
    trim_center_x = BLEED + (TRIM_WIDTH / 2)
    trim_center_y = BLEED + (TRIM_HEIGHT / 2)
    
    c.setFillColor(TEXT_COLOR)
    c.setFont("Roboto-Light", 18)
    
    title = "Dawn at Nurra Nurra"
    title_width = c.stringWidth(title, "Roboto-Light", 18)
    c.drawString(trim_center_x - (title_width / 2), trim_center_y + 60, title)
    
    c.setFont("Roboto", 12)
    dedication_lines = [
        "For Robert,",
        "",
        "Who spent twenty years revegetating",
        "a small corner of Australia,",
        "and shared the many shades of dawn with us.",
        "",
        "July 2024 - August 2025",
        "Ngarrindjeri Country",
        "-35.5559, 139.2498"
    ]
    
    y_pos = trim_center_y
    for line in dedication_lines:
        line_width = c.stringWidth(line, "Roboto", 12)
        c.drawString(trim_center_x - (line_width / 2), y_pos, line)
        y_pos -= 18


def draw_colophon_page(c, bg_color):
    """Draw the colophon page at the end of the book."""
    c.setFillColor(bg_color)
    c.rect(0, 0, PDF_WIDTH, PDF_HEIGHT, fill=1, stroke=0)
    
    trim_center_x = BLEED + (TRIM_WIDTH / 2)
    trim_center_y = BLEED + (TRIM_HEIGHT / 2)
    
    c.setFillColor(TEXT_COLOR)
    c.setFont("Roboto", 12)
    
    colophon_lines = [
        "All photos and captions by Robert Mrongovius",
        "Shared to the Family WhatsApp group",
        "Collated by Alice Mrongovius, November 2025"
    ]
    
    y_pos = trim_center_y
    for line in colophon_lines:
        line_width = c.stringWidth(line, "Helvetica", 12)
        c.drawString(trim_center_x - (line_width / 2), y_pos, line)
        y_pos -= 18


def draw_photo_page(c, image_path, datetime_text, caption_text, is_right_page=True):
    """Draw a photo page with image and caption."""
    
    # Get background color from image
    bg_color = get_top_left_pixel_color(image_path)
    c.setFillColor(bg_color)
    c.rect(0, 0, PDF_WIDTH, PDF_HEIGHT, fill=1, stroke=0)
    
    # Get safe content area
    safe_left, safe_bottom, safe_width, safe_height = get_safe_content_area(is_right_page)
    
    # Center image horizontally within safe area
    image_x = safe_left + (safe_width - IMAGE_WIDTH) / 2
    
    # Position image from top with reduced margin
    natural_top_margin = (safe_width - IMAGE_WIDTH) / 2
    actual_top_margin = natural_top_margin - (0 * cm)
    image_y = (safe_bottom + safe_height) - actual_top_margin - IMAGE_HEIGHT
    
    # Draw the image
    try:
        c.drawImage(image_path, image_x, image_y, 
                    width=IMAGE_WIDTH, height=IMAGE_HEIGHT,
                    preserveAspectRatio=True)
    except Exception as e:
        print(f"⚠️  Warning: Could not draw image {os.path.basename(image_path)}: {e}")
    
    # Draw text below image
    text_x = image_x
    text_y = image_y - IMAGE_TEXT_GAP
    
    # Date/time
    c.setFillColor(TEXT_COLOR)
    c.setFont("Roboto", DATETIME_SIZE)
    c.drawString(text_x, text_y, datetime_text)
    
    # Caption (with line wrapping)
    if caption_text:
        text_y -= 0.25 * inch
        c.setFont("Roboto", CAPTION_SIZE)
        
        # Line wrapping
        words = caption_text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if c.stringWidth(test_line, "Roboto", CAPTION_SIZE) < IMAGE_WIDTH:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw caption lines
        for line in lines:
            c.drawString(text_x, text_y, line)
            text_y -= CAPTION_SIZE * LINE_SPACING


def create_full_photobook(json_file, images_dir, output_file):
    """Create the complete 336-page photobook PDF."""
    
    print("="*70)
    print("📖 DAWN AT NURRA NURRA - PHOTOBOOK GENERATOR")
    print("="*70)
    print(f"📂 Reading data from: {json_file}")
    print(f"📁 Images directory: {images_dir}")
    print(f"💾 Output file: {output_file}")
    print()
    
    # Load photo data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    photos = data['photos']
    total_photos = len(photos)
    
    if total_photos != 330:
        print(f"⚠️  Warning: Expected 330 photos, found {total_photos}")
    
    print(f"📸 Loaded {total_photos} photos")
    print(f"📅 Date range: {data['metadata']['date_range']['first']} → {data['metadata']['date_range']['last']}")
    print()
    
    # Verify images exist
    missing_images = []
    for photo in photos:
        image_path = os.path.join(images_dir, photo['filename'])
        if not os.path.exists(image_path):
            missing_images.append(photo['filename'])
    
    if missing_images:
        print(f"❌ ERROR: {len(missing_images)} images not found in {images_dir}")
        print(f"   First missing: {missing_images[0]}")
        print(f"   Please ensure all images are in the BookImages/ folder")
        return None
    
    print("✅ All images found")
    print()
    print("🚀 Generating PDF... This will take a few minutes...")
    print()
    
    # Create PDF
    c = canvas.Canvas(output_file, pagesize=(PDF_WIDTH, PDF_HEIGHT))
    
    # Get background colors
    first_photo_path = os.path.join(images_dir, photos[0]['filename'])
    last_photo_path = os.path.join(images_dir, photos[-1]['filename'])
    first_photo_bg = get_top_left_pixel_color(first_photo_path)
    last_photo_bg = get_top_left_pixel_color(last_photo_path)
    
    page_count = 0
    
    # PAGE 1: Dedication (Right)
    print("📄 Page 1: Dedication")
    draw_title_dedication_page(c, first_photo_bg)
    c.showPage()
    page_count += 1
    
    # PAGE 2: Blank (Left)
    print("📄 Page 2: Blank")
    draw_blank_page(c, first_photo_bg)
    c.showPage()
    page_count += 1
    
    # PAGE 3: Photo 1 alone (Right)
    print(f"📄 Page 3: Photo 1 - {photos[0]['filename']}")
    image_path = os.path.join(images_dir, photos[0]['filename'])
    draw_photo_page(c, image_path, photos[0]['datetime_display'], 
                   photos[0]['caption'], is_right_page=True)
    c.showPage()
    page_count += 1
    
    # Middle photos in spreads
    middle_photos = total_photos - 2  # Exclude first and last
    print(f"📄 Pages 4-{3+middle_photos}: Photos 2-{total_photos-1} ({middle_photos//2} spreads)")
    
    for i in range(1, total_photos - 1, 2):  # Photos 2 to second-to-last
        if i % 20 == 1:
            print(f"   ... Page {page_count + 1}: Photo {i + 1}")
        
        # Left page (even page number)
        image_path = os.path.join(images_dir, photos[i]['filename'])
        draw_photo_page(c, image_path, photos[i]['datetime_display'],
                       photos[i]['caption'], is_right_page=False)
        c.showPage()
        page_count += 1
        
        # Right page (odd page number)
        if i + 1 < len(photos) - 1:  # Don't go past photo 329
            image_path = os.path.join(images_dir, photos[i + 1]['filename'])
            draw_photo_page(c, image_path, photos[i + 1]['datetime_display'],
                           photos[i + 1]['caption'], is_right_page=True)
            c.showPage()
            page_count += 1
    
    # PAGE 332: Blank (Left)
    print("📄 Page 332: Blank")
    draw_blank_page(c, last_photo_bg)
    c.showPage()
    page_count += 1
    
    # PAGE 333: Photo 330 alone (Right)
    print(f"📄 Page 333: Photo 330 - {photos[-1]['filename']}")
    image_path = os.path.join(images_dir, photos[-1]['filename'])
    draw_photo_page(c, image_path, photos[-1]['datetime_display'],
                   photos[-1]['caption'], is_right_page=True)
    c.showPage()
    page_count += 1
    
    # PAGE 334: Blank (Left)
    print("📄 Page 334: Blank")
    draw_blank_page(c, last_photo_bg)
    c.showPage()
    page_count += 1
    
    # PAGE 335: Colophon (Right)
    print("📄 Page 335: Colophon")
    draw_colophon_page(c, last_photo_bg)
    c.showPage()
    page_count += 1
    
    # PAGE 336: Blank (Left)
    print("📄 Page 336: Blank")
    draw_blank_page(c, last_photo_bg)
    c.showPage()
    page_count += 1
    
    # Save PDF
    c.save()
    
    print()
    print("="*70)
    print("✅ PHOTOBOOK COMPLETE!")
    print("="*70)
    print(f"📄 File: {output_file}")
    print(f"📊 Total pages: {page_count}")
    print(f"📸 Total photos: {total_photos}")
    print(f"📐 Dimensions: {PDF_WIDTH/cm:.3f} x {PDF_HEIGHT/cm:.3f} cm (with bleed)")
    print(f"💾 File size: {os.path.getsize(output_file) / (1024*1024):.1f} MB")
    print()
    print("🎉 Ready to upload to Blurb!")
    print("="*70)
    
    return output_file


def main():
    """Main function with file path setup."""
    import sys
    
    # Default paths (adjust if needed)
    json_file = 'dawn_photos_book.json'
    images_dir = 'BookImages'
    output_file = 'dawn_at_nurra_nurra_FINAL.pdf'
    
    # Check if files exist
    if not os.path.exists(json_file):
        print(f"❌ ERROR: Could not find {json_file}")
        print(f"   Please ensure the JSON file is in the same directory as this script")
        sys.exit(1)
    
    if not os.path.exists(images_dir):
        print(f"❌ ERROR: Could not find {images_dir}/ directory")
        print(f"   Please ensure the BookImages folder is in the same directory as this script")
        sys.exit(1)
    
    # Generate photobook
    create_full_photobook(json_file, images_dir, output_file)


if __name__ == '__main__':
    main()
