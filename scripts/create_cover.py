#!/usr/bin/env python3
"""Dawn at Nurra Nurra - Cover Generator"""

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image
import os

# Register Roboto fonts
pdfmetrics.registerFont(TTFont('Roboto', 'Roboto-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Light', 'Roboto-Light.ttf'))

# Blurb specs
PDF_WIDTH = 50.799 * cm
PDF_HEIGHT = 20.955 * cm
TRIM_WIDTH = 50.165 * cm
TRIM_HEIGHT = 20.321 * cm
BLEED = 0.317 * cm
SPINE_WIDTH = 1.905 * cm
SAFE_MARGIN = 0.635 * cm
BACK_WIDTH = (TRIM_WIDTH - SPINE_WIDTH) / 2
FRONT_WIDTH = (TRIM_WIDTH - SPINE_WIDTH) / 2
IMAGE_WIDTH = 7 * inch
IMAGE_HEIGHT = IMAGE_WIDTH / (4/3)

def get_color(path):
    try:
        return Image.open(path).getpixel((0, 0))[:3]
    except:
        return (43, 43, 43)

def brightness(rgb):
    return 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]

def text_color(bg):
    return (HexColor('#1a1a1a'), "black") if brightness(bg) > 128 else (HexColor('#f5f5f5'), "white")

def create_cover(img_path, out):
    print("="*70)
    print("📕 COVER GENERATOR")
    print("="*70)
    
    if not os.path.exists(img_path):
        print(f"❌ {img_path} not found")
        return
    
    bg_rgb = get_color(img_path)
    bg = HexColor('#%02x%02x%02x' % bg_rgb)
    txt, txt_type = text_color(bg_rgb)
    
    print(f"🎨 Background: RGB{bg_rgb}")
    print(f"📝 Text: {txt_type}\n")
    
    c = canvas.Canvas(out, pagesize=(PDF_WIDTH, PDF_HEIGHT))
    c.setFillColor(bg)
    c.rect(0, 0, PDF_WIDTH, PDF_HEIGHT, fill=1, stroke=0)
    
    front_start = BLEED + BACK_WIDTH + SPINE_WIDTH
    front_cx = front_start + FRONT_WIDTH/2
    front_cy = BLEED + TRIM_HEIGHT/2
    
    ix = front_cx - IMAGE_WIDTH/2
    iy = front_cy - IMAGE_HEIGHT/2
    
    print("📄 Front cover...")
    c.drawImage(img_path, ix, iy, IMAGE_WIDTH, IMAGE_HEIGHT, preserveAspectRatio=True)
    
    # Title with letter spacing
    c.setFillColor(txt)
    c.setFont("Roboto-Light", 30)
    title = "Dawn at Nurra Nurra"

    # Calculate total width with spacing
    letter_spacing = 0.05 * cm
    total_width = sum(c.stringWidth(char, "Roboto-Light", 30) for char in title)
    total_width += letter_spacing * (len(title) - 1)  # Add spacing between letters

    # Calculate starting x position (centered)
    start_x = front_cx - (total_width / 2)
    ty = BLEED + SAFE_MARGIN + 1.5 * cm

    # Draw each character with spacing
    x = start_x
    for char in title:
        c.drawString(x, ty, char)
        x += c.stringWidth(char, "Roboto-Light", 30) + letter_spacing
    
    c.setFont("Roboto", 14)
    sub = "Robert Mrongovius"
    sx = front_cx - c.stringWidth(sub, "Roboto", 14)/2
    c.drawString(sx, ty - 0.7*cm, sub)
    
    print("📄 Spine...")
    c.saveState()
    c.translate(BLEED + BACK_WIDTH + SPINE_WIDTH/2, PDF_HEIGHT/2)
    c.rotate(90)
    c.setFont("Roboto-Light", 14)
    spine = "Dawn at Nurra Nurra  •  Robert Mrongovius"
    c.drawString(-c.stringWidth(spine, "Roboto-Light", 14)/2, -0.2*cm, spine)
    c.restoreState()
    
    c.save()
    
    print("\n" + "="*70)
    print("✅ COMPLETE!")
    print(f"📄 {out}")
    print(f"📐 {PDF_WIDTH/cm:.1f} x {PDF_HEIGHT/cm:.1f} cm")
    print(f"🎨 {txt_type} text")
    print("="*70)

if __name__ == '__main__':
    import sys
    img = 'BookImages/00006923-PHOTO-2024-07-28-23-15-04.jpg'
    out = 'dawn_at_nurra_nurra_COVER.pdf'
    if not os.path.exists(img):
        print(f"❌ {img} not found")
        sys.exit(1)
    create_cover(img, out)