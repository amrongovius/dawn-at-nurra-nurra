# Dawn at Nurra Nurra

*A 332-page photo book documenting Robert Mrongovius's final 13 months at Nurra Nurra, South Australia, through 326 daily dawn photographs shared via WhatsApp.*

---

## 📖 About This Project

For 20 years, my father Robert revegetated a property on the Narrung Peninsula on Ngarrindjeri Country in South Australia. During his final year there (July 2024 - August 2025), he shared 330 dawn photos with our family via WhatsApp—each one capturing the ever-changing beauty of sunrise over the land he had nurtured.

This repository documents the complete process of transforming those WhatsApp messages into a professionally designed, Blurb-printed photo book.

### Why This Matters

It's a tribute to:
- 20 years of environmental dedication
- Daily connection through WhatsApp
- The quiet beauty of Australian dawn
- Preserving family memories in a meaningful way

---

## 🌅 The Book

**Format:** Standard Landscape 10×8" (25.4×20.3 cm)  
**Pages:** 332  
**Photos:** 326 dawn photographs (July 23, 2024 → August 17, 2025)  
**Captions:** 289 photos with captions in Robert's own words  
**Cover:** Matte soft cover  
**Typography:** Roboto (matching WhatsApp's typeface)  
**Printer:** Blurb

---

## 📂 Repository Contents

### `/scripts/`
Complete pipeline from WhatsApp export to printed book:

1. **`csv_to_json.py`** - Convert CSV with captions to JSON format
2. **`extract_images.py`** - Extract only needed photos from WhatsApp backup
3. **`create_full_photobook.py`** - Generate 332-page interior PDF
4. **`create_cover.py`** - Generate wraparound cover PDF

### `/data/`
- **`dawn_photos_book.json`** - Structured photo metadata with captions, timestamps, and filenames

### `/docs/`
- **`CUSTOMIZATION_GUIDE.md`** - Complete instructions for generating and customizing the book

---

## 🔄 Complete Workflow

```
WhatsApp Export (1000s of photos)
         ↓
    Manual Work:
    - Create CSV with photo list
    - Add captions from messages
         ↓
1. csv_to_json.py
    → Converts CSV to JSON
         ↓
2. extract_images.py
    → Copies only needed 326 photos
         ↓
3. create_full_photobook.py
    → Generates 332-page interior PDF
         ↓
4. create_cover.py
    → Generates cover PDF
         ↓
    Upload to Blurb → Order Book!
```

---

## 🚀 Quick Start

See **[CUSTOMIZATION_GUIDE.md](docs/CUSTOMIZATION_GUIDE.md)** for complete step-by-step instructions.

**Basic usage:**
```bash
# 1. Convert your caption CSV to JSON
python3 csv_to_json.py dawn_photos_2024_2025_COMPACT.csv dawn_photos_book.json

# 2. Extract only the photos you need
python3 extract_images.py dawn_photos_book.json WhatsApp_Export/ BookImages/

# 3. Generate interior PDF (332 pages)
python3 create_full_photobook.py

# 4. Generate cover PDF
python3 create_cover.py
```

---

## 🎨 Design Philosophy

### Typography: Roboto
Robert used Android, so he saw these photos in Roboto (WhatsApp's Android font). Using Roboto maintains visual continuity with his original messages—a subtle but meaningful connection.

### Dynamic Backgrounds
Each page's background is extracted from its photo's top-left pixel. This creates an immersive experience where the book's color shifts with each dawn, just as the sky did.

### Page Structure
- **First photo alone:** Strong opening
- **Middle photos in spreads:** Maximum visual impact
- **Last photo alone:** Meaningful conclusion, parallel to opening
- **Blank pages:** Breathing space, respectful pacing

---

## 📊 Technical Specifications

### Book Interior
- **PDF size (with bleed):** 24.447 × 20.955 cm (9.625 × 8.25 inches)
- **Trim size:** 24.13 × 20.321 cm (9.5 × 8 inches)
- **Bleed:** 0.317 cm all edges
- **Safe margins:** 0.635 cm (outside), 1.27 cm (binding)
- **Image size:** 7 × 5.25 inches
- **Resolution:** 200+ DPI

### Cover
- **PDF size:** 50.799 × 20.955 cm
- **Spine width:** 1.905 cm
- **Auto-detected text color** (black/white based on background brightness)

### Typography
- **Font:** Roboto (Regular, Bold, Light)
- **Sizes:** Title 18pt, Datetime 11pt, Captions 10pt
- **Color:** #F5F5F5 (soft white)

---

## 📖 Page Structure (332 pages)

### Opening (3 pages)
1. Dedication (Right)
2. Blank (Left)
3. Photo 1 alone (Right)

### Main Section (324 pages)
- Pages 4-327: Photos 2-325 in spreads (162 spreads, 2 photos each)

### Closing (5 pages)
1. Blank (Left)
2. Photo 326 alone (Right) - Last sunrise
3. Blank (Left)
4. Colophon (Right) - Credits
5. Blank (Left)

**Total: 332 pages** (divisible by 4 for printing)

---

## 🛠️ Technical Stack

- **Python 3** - Core language
- **ReportLab** - PDF generation
- **Pillow (PIL)** - Image processing
- **Roboto Font** - Typography (Google Fonts)

---

## 🌏 Location

**Narrung, South Australia**  
Ngarrindjeri Country  
Coordinates: -35.5559, 139.2498  
On the Coorong, where Lake Alexandrina meets the Southern Ocean

---

## 💡 What I Learned

### Technical
- PDF generation with precise print specifications
- Color space management (RGB for Blurb)
- Custom font embedding
- Dynamic content positioning
- Python indentation sensitivity! 😄
- Complete pipeline automation

### Design
- Less is more (simple layouts work best)
- Typography matters (Roboto over Helvetica)
- Context creates meaning (WhatsApp connection)
- Breathing space enhances content
- Details show love

### Personal
- The value of patience (289 captions!)
- Technology can preserve emotion
- Code can be an act of care
- Small daily acts compound into beauty

---

## 📝 License

This is a personal family project. The scripts and documentation are shared for educational purposes.

**Photos:** © Robert Mrongovius, 2024-2025  
**Collation & Design:** Alice Mrongovius, 2025

See [LICENSE.md](LICENSE.md) for details.

---

## 🙏 Acknowledgments

- **Robert Mrongovius** - For 20 years of dedication to the land, and for sharing these daily moments
- **Family WhatsApp Group** - For being the original audience
- **Ngarrindjeri People** - Traditional custodians of the land
- **Claude (Anthropic)** - For assistance with script development and design refinement
- **Blurb** - For making professional book printing accessible

---

## 📬 Connect

**GitHub:** [@amrongovius](https://github.com/amrongovius)  
**LinkedIn:** [Alice Mrongovius](https://linkedin.com/in/amrongovius)  
**Instagram:** [@amrongovius](https://instagram.com/amrongovius)

---

## 🌅 Final Thought

This book started as 330 WhatsApp messages and became a permanent record of dawn at Narrung. It's a reminder that:
- Small daily acts (sending a photo) compound into something beautiful
- Technology can bridge distance
- The ordinary becomes extraordinary when attended to with care
- Twenty years of work deserves to be celebrated

If you're working on a similar project—whether it's WhatsApp messages, emails, or any digital archive—I hope this repository helps you turn ephemeral moments into something lasting.

---

*Made with ☕, Python, and love in Berlin • November 2025*
