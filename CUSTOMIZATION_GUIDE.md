# Customization Guide

A complete walkthrough of the Dawn at Nurra Nurra photobook creation process, showing how each script works and where you can make modifications.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Complete Workflow](#complete-workflow)
3. [Design Adjustments](#design-adjustments)
4. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Software Requirements

**Install Python dependencies:**
```bash
pip3 install reportlab pillow
```

### Font Files

Download from [Google Fonts - Roboto](https://fonts.google.com/specimen/Roboto):
- Roboto-Regular.ttf
- Roboto-Bold.ttf
- Roboto-Light.ttf

Place in the same folder as your scripts.

### Your Source Materials

Depending on your starting point, you'll need:
- **From WhatsApp:** Chat export folder + caption CSV
- **From other photos:** Photo folder + data JSON

---

## Complete Workflow

This section walks through the entire process from WhatsApp export to printed book, showing what each script does and where you can customize.

---

### Starting Point: WhatsApp Export

Export your WhatsApp chat:

**iPhone:** WhatsApp → Chat → Chat name → Export Chat → With Media  
**Android:** WhatsApp → Chat → ⋮ → More → Export chat → Include Media

**Result:** A folder containing:
- `_chat.txt` - All messages with timestamps
- 1000s of image files

---

### Step 1: Create Your Caption CSV

**What you're doing:** Manually selecting which photos to include and transcribing captions from WhatsApp messages.

**Create:** `dawn_photos_2024_2025_COMPACT.csv`

**Format:**
```csv
filename,datetime,caption
00006878-PHOTO-2024-07-22-23-07-43.jpg,2024-07-23 06:37:13,The position of the sunrise has moved further to the right.
00006879-PHOTO-2024-07-22-23-51-01.jpg,2024-07-23 07:21:01,
00006880-PHOTO-2024-07-23-06-22-41.jpg,2024-07-23 08:52:41,Good morning from a very frosty Narrung.
```

**Columns:**
- `filename` - Exact filename from WhatsApp export
- `datetime` - When photo was taken (YYYY-MM-DD HH:MM:SS format)
- `caption` - Caption text (leave empty if no caption)

**Tools:** Use Excel, Google Sheets, or Numbers

**Tips:**
- Review `_chat.txt` to find captions
- Match timestamps to photos
- Keep filenames exactly as they appear in export
- This is where you decide which 326 photos (or however many) to include

---

### Step 2: CSV → JSON

**Script:** `csv_to_json.py`

**What it does:**
- Reads your CSV file
- Auto-detects delimiter and column names
- Formats dates nicely ("August 17, 2025, 7:03 AM")
- Creates structured JSON
- Calculates metadata (photo count, date range)

**Run:**
```bash
python3 csv_to_json.py dawn_photos_2024_2025_COMPACT.csv dawn_photos_book.json
```

**Output:** `dawn_photos_book.json` with this structure:
```json
{
  "photos": [
    {
      "filename": "00006878-PHOTO-2024-07-22-23-07-43.jpg",
      "datetime_original": "2024-07-23T06:37:13",
      "datetime_display": "July 23, 2024, 6:37 AM",
      "caption": "The position of the sunrise has moved...",
      "date": "2024-07-23"
    }
  ],
  "metadata": {
    "total_photos": 326,
    "photos_with_captions": 289,
    "date_range": {
      "first": "2024-07-23",
      "last": "2025-08-17"
    }
  }
}
```

**🎨 Customization Options:**

**Use different column names:** Script auto-detects, but if it fails:
- Ensure CSV has headers
- Column names can be flexible (e.g., "file" instead of "filename")

**Change date format:** Edit the `parse_datetime()` function to handle your format

**Add custom fields:** Modify the `photo_entry` dictionary to include additional data

---

### Step 3: Extract Images

**Script:** `extract_images.py`

**What it does:**
- Reads JSON to see which photos are needed (326 in this case)
- Searches your WhatsApp export for those specific files
- Copies only the needed photos to a clean folder
- Reports any missing files

**Why this is important:**
- WhatsApp export has 1000s of photos (family pics, screenshots, etc.)
- You only need the 326 dawn photos
- Keeps your working directory clean
- Makes it safe to manage in GitHub (only dawn photos, no private family photos)

**Run:**
```bash
python3 extract_images.py dawn_photos_book.json WhatsApp_Export/ BookImages/
```

**Arguments:**
1. Your JSON file
2. Source folder (where ALL WhatsApp images are)
3. Destination folder (where to put ONLY book images)

**Output:**
- `BookImages/` folder with exactly 326 photos
- Progress report showing copied/missing files

**🎨 Customization Options:**

**Skip this step if:**
- Your photos are already organized in one folder
- Just rename your folder to `BookImages/`

**Use different folder names:** Change arguments when running script

---

### Step 4: Generate Interior PDF

**Script:** `create_full_photobook.py`

**What it does:**
- Loads photo data from JSON
- Extracts background color from each photo's top-left pixel
- Creates 332-page PDF with:
  - Dedication page
  - Blank pages for structure
  - 324 pages of photo spreads
  - Colophon page

**Run:**
```bash
python3 create_full_photobook.py
```

**Output:**
- `dawn_at_nurra_nurra_FINAL.pdf`
- ~150-200 MB
- 332 pages
- Takes 3-5 minutes

**🎨 Customization Points:**

#### A. Dedication Page

Find `draw_title_dedication_page()` function (around line 115):

```python
title = "Dawn at Nurra Nurra"  # ← Change book title

dedication_lines = [
    "For Robert,",                    # ← Customize these lines
    "",                               # Empty = blank line
    "Who spent twenty years revegetating",
    "a small corner of Australia,",
    "and shared the many shades of dawn with us.",
    "",
    "July 2024 - August 2025",        # ← Date range
    "Ngarrindjeri Country",           # ← Location
    "-35.5559, 139.2498"             # ← Coordinates (optional)
]
```

**Tips:**
- Keep lines under 50 characters
- Use `""` for blank lines
- Text is centered automatically

---

#### B. Colophon Page

Find `draw_colophon_page()` function (around line 145):

```python
colophon_lines = [
    "All photos and captions by Robert Mrongovius",  # ← Credits
    "Shared to the Family WhatsApp group",           # ← Platform
    "Collated by Alice Mrongovius, November 2025"   # ← Your name/date
]
```

---

#### C. Font Customization

At the top of the script, after imports:

```python
# Register custom fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('YourFont', 'YourFont-Regular.ttf'))
pdfmetrics.registerFont(TTFont('YourFont-Bold', 'YourFont-Bold.ttf'))
```

Then replace `"Roboto"` with `"YourFont"` throughout the script.

---

#### D. Colors and Sizes

Find these constants near the top:

```python
TEXT_COLOR = HexColor('#F5F5F5')  # Soft white
DATETIME_SIZE = 11                # Date/time text size
CAPTION_SIZE = 10                 # Caption text size
LINE_SPACING = 1.4                # Space between caption lines
IMAGE_WIDTH = 7 * inch            # Image width
```

---

#### E. Page Structure

The script automatically adapts to your photo count:
- Page count formula: `(total_photos - 2) + 8 = total_pages`
- Must be divisible by 4

**Examples:**
- 326 photos → 332 pages ✓
- 100 photos → 106 pages ✓
- 99 photos → 105 pages ✗ (add 3 photos → 108 ✓)

---

### Step 5: Generate Cover

**Script:** `create_cover.py`

**What it does:**
- Loads one photo for the cover
- Extracts background color from photo
- Auto-detects best text color (black or white based on background brightness)
- Creates wraparound cover PDF:
  - Back cover (background color only)
  - Spine (title + author, vertical text)
  - Front cover (photo + title + subtitle)

**Run:**
```bash
python3 create_cover.py
```

**Output:**
- `dawn_at_nurra_nurra_COVER.pdf`
- ~1-2 MB
- Takes 5-10 seconds

**🎨 Customization Points:**

#### A. Cover Image

At the bottom of the script:

```python
if __name__ == '__main__':
    img = 'BookImages/00006923-PHOTO-2024-07-28-23-15-04.jpg'  # ← Change this
    out = 'dawn_at_nurra_nurra_COVER.pdf'                      # ← Output filename
```

---

#### B. Cover Text

Find the title/subtitle section (around line 65):

```python
# Title
title = "Dawn at Nurra Nurra"              # ← Change title

# Subtitle
sub = "Robert Mrongovius"                  # ← Change subtitle

# Spine (appears vertically when book is on shelf)
spine = "Dawn at Nurra Nurra  •  Robert Mrongovius"  # ← Change spine text
```

---

#### C. Letter Spacing (Optional)

The cover title has letter spacing for elegance. Find:

```python
letter_spacing = 0.15 * cm  # Adjust spacing
```

**Options:**
- No spacing: `0`
- Subtle: `0.05 * cm`
- Medium (current): `0.15 * cm`
- Wide: `0.25 * cm`

Or remove letter spacing entirely by replacing the title section with:

```python
# Simple title (no spacing)
c.setFont("Roboto-Light", 30)
title = "Your Title"
tx = front_cx - c.stringWidth(title, "Roboto-Light", 30)/2
c.drawString(tx, ty, title)
```

---

### Step 6: Upload to Blurb

1. Go to [Blurb.com](https://www.blurb.com)
2. Create account / Sign in
3. Create → Photo Books → Upload PDF
4. Select: **Standard Landscape 10×8 inches**
5. Upload both PDFs:
   - Interior: `dawn_at_nurra_nurra_FINAL.pdf`
   - Cover: `dawn_at_nurra_nurra_COVER.pdf`
6. Preview in Blurb's tool
7. Choose options:
   - **Paper:** Standard (for 332 pages, premium would be very thick)
   - **Cover:** Matte Softcover
8. Order!

**First time?** Consider ordering a **proof copy** (cheaper softcover) to check colors and layout before ordering the final version.

---

## Design Adjustments

Fine-tuning options for the look and feel of your book.

### Image Positioning

**Change top margin:**

In `create_full_photobook.py`, find `draw_photo_page()` function:

```python
# Position image from top with increased margin
actual_top_margin = natural_top_margin + (2.5 * cm)  # ← Adjust this value
```

**Values:**
- Less space at top: `+ (1.5 * cm)`
- Current: `+ (2.5 * cm)`
- More space at top: `+ (3.5 * cm)`

---

### Image Size

In both scripts, find near the top:

```python
IMAGE_WIDTH = 7 * inch              # Change width
IMAGE_HEIGHT = IMAGE_WIDTH / (4/3)  # Adjust aspect ratio if needed
```

**Common sizes:**
- Smaller (more white space): `6 * inch`
- Current: `7 * inch`
- Larger (less white space): `7.5 * inch`

---

### Text Colors

**Interior pages:**

```python
TEXT_COLOR = HexColor('#F5F5F5')  # Soft white (current)
```

**Common alternatives:**
- Pure white: `'#FFFFFF'`
- Light gray: `'#CCCCCC'`
- Warm white: `'#FFF8DC'`

**Cover:** Text color is auto-detected based on background. To override, edit the `text_color()` function in `create_cover.py`.

---

### Typography

**Font sizes:**

In `create_full_photobook.py`:

```python
DATETIME_SIZE = 11   # Date/time above photo
CAPTION_SIZE = 10    # Caption text
LINE_SPACING = 1.4   # Space between caption lines
```

**Recommended ranges:**
- Datetime: 10-13pt
- Caption: 9-11pt
- Line spacing: 1.2-1.6

---

**Different fonts:**

Replace Roboto with any TrueType font:

```python
# Register your font
pdfmetrics.registerFont(TTFont('MyFont', 'MyFont-Regular.ttf'))

# Then use throughout
c.setFont("MyFont", 12)
```

Make sure to replace in:
- `create_full_photobook.py` (dedication, captions, colophon)
- `create_cover.py` (title, subtitle, spine)

---

## Troubleshooting

### Script 1: csv_to_json.py

**Problem:** "CSV file not found"  
**Solution:** Check filename spelling, verify file is in same folder

**Problem:** "Could not find filename column"  
**Solution:** CSV needs headers. Column names should include "filename" or "file"

**Problem:** "Could not parse datetime"  
**Solution:** Script will use raw string. Still works, just less formatted

---

### Script 2: extract_images.py

**Problem:** "JSON file not found"  
**Solution:** Run `csv_to_json.py` first

**Problem:** "All images missing"  
**Solution:** Check source folder path. Try: `ls WhatsApp_Export/*.jpg | wc -l`

**Problem:** "Some images missing"  
**Solution:** Check filenames match exactly (case-sensitive). Some photos might not be in export

---

### Script 3: create_full_photobook.py

**Problem:** "X images not found"  
**Solution:** 
- Run `extract_images.py` first
- Check `BookImages/` folder exists
- Verify filenames in JSON match files exactly

**Problem:** Font not loading (displays Helvetica instead)  
**Solution:**
- Check font files in same folder: `Roboto-Regular.ttf`, `Roboto-Light.ttf`, `Roboto-Bold.ttf`
- Add error checking:
```python
try:
    pdfmetrics.registerFont(TTFont('Roboto', 'Roboto-Regular.ttf'))
    print("✅ Font loaded")
except Exception as e:
    print(f"❌ Error: {e}")
```

**Problem:** "TabError: inconsistent use of tabs and spaces"  
**Solution:**
- Python requires consistent indentation
- Use **spaces only** (not tabs)
- Each indent level = 4 spaces
- Use a code editor (VS Code, Sublime Text)

**Problem:** Script takes forever  
**Solution:**
- Expected: 3-5 minutes for 332 pages
- If longer: check disk space, image resolution
- Try with smaller subset first (10 photos)

**Problem:** "Wrong page count"  
**Solution:**
- Formula: `(total_photos - 2) + 8 = total_pages`
- Must be divisible by 4
- Add or remove photos to fix

---

### Script 4: create_cover.py

**Problem:** "Cover image not found"  
**Solution:** Check image filename in script, verify it's in `BookImages/`

**Problem:** Text color wrong  
**Solution:** Auto-detected based on background brightness. To override, edit `text_color()` function

---

### General Issues

**Problem:** PDF too large (300+ MB)  
**Solution:**
- Reduce image resolution before processing
- Compress images: `convert image.jpg -quality 85 -resize 1600x1200 image.jpg`
- Blurb accepts up to 500 MB

**Problem:** Colors look wrong when printed  
**Solution:**
- Keep RGB mode (don't convert to CMYK - Blurb handles this)
- Printed colors always differ from screen
- Order a proof copy first to check colors

**Problem:** Can't overwrite PDF  
**Solution:** Close the PDF file in Preview/Acrobat before running script again

---

## 📊 Quick Reference

### File Workflow
```
CSV file (20-50 KB)
    ↓
JSON file (100-200 KB)
    ↓
BookImages/ (50-100 MB, 326 photos)
    ↓
Interior PDF (150-200 MB, 332 pages)
    +
Cover PDF (1-2 MB)
    ↓
Upload to Blurb
```

### Script Commands
```bash
# 1. Convert CSV to JSON
python3 csv_to_json.py input.csv output.json

# 2. Extract only needed images
python3 extract_images.py data.json WhatsApp_Export/ BookImages/

# 3. Generate interior (3-5 minutes)
python3 create_full_photobook.py

# 4. Generate cover (5-10 seconds)
python3 create_cover.py
```

### Photo Requirements
- **Minimum resolution:** 1600×1200 pixels
- **Format:** JPG
- **Aspect ratio:** 4:3 recommended
- **Color space:** RGB (Blurb converts to CMYK)

### Page Count Formula
`(total_photos - 2) + 8 = total_pages`

Must be divisible by 4 for printing.

---

## 💡 Best Practices

1. **Test incrementally** - Start with 10 photos, then scale up
2. **Backup before changes** - Commit to Git before editing
3. **Close PDFs** - Can't regenerate if file is open
4. **Spell-check captions** - Errors are permanent once printed
5. **Preview thoroughly** - Check random pages in Blurb's preview tool
6. **Order proof first** - Get cheap softcover to verify before final order
7. **Use code editor** - VS Code or Sublime Text for editing Python
8. **Keep filenames exact** - Must match JSON exactly (case-sensitive)

---

## 🎯 Complete Checklist

Before uploading to Blurb:

- [ ] All 4 scripts run successfully
- [ ] Interior PDF generated (332 pages)
- [ ] Cover PDF generated
- [ ] Dedication text customized
- [ ] Colophon credits updated
- [ ] Cover title/subtitle updated
- [ ] All captions spell-checked
- [ ] Fonts loading correctly
- [ ] Page count divisible by 4
- [ ] Spot-checked random pages
- [ ] Both PDFs previewed

---

*For the visual workflow diagram, see [WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md)*
