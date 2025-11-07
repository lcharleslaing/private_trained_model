# Handling Images and PDFs with Drawings/Images

## ✅ OCR + Vision Model Support Now Available!

The system now includes **automatic OCR (Optical Character Recognition)** AND **Vision Model** support for:
- **Direct image files** (JPG, PNG, GIF, BMP, TIFF, WEBP)
- **PDFs with drawings/images** (scanned documents, technical drawings)

## How It Works Now

### For Direct Image Files (JPG, PNG, GIF, etc.):

1. **OCR Processing**: Automatically runs OCR using EasyOCR to extract visible text
2. **Vision Model Processing**: Automatically runs Vision Model (LLaVA) to understand and describe visual content
3. **Combined Results**: Both OCR text and vision descriptions are indexed and made searchable

### For PDFs with Drawings/Images:

1. **Standard Text Extraction**: First tries to extract text normally from PDF
2. **OCR + Vision Fallback**: If little text is found (< 50 chars), automatically:
   - Converts PDF pages to images
   - Runs OCR on each page using EasyOCR (extracts visible text)
   - Runs Vision Model (LLaVA) on each page (understands visual content)
   - Extracts text from images/drawings AND describes visual elements
   - Combines all results with any existing text

### What Happens with Images:

- ✅ **Photos with text**: OCR extracts text, Vision model describes the scene
- ✅ **Screenshots**: OCR extracts UI text, Vision model describes interface elements
- ✅ **Technical drawings**: OCR extracts labels/dimensions, Vision model describes shapes and relationships
- ✅ **Scanned documents**: OCR extracts all text, Vision model provides context
- ✅ **Charts/Diagrams**: OCR extracts labels, Vision model describes data visualization

### What Happens with Drawing PDFs:

- ✅ **Text-based PDFs**: Extracts all text normally
- ✅ **PDFs with text labels**: Extracts text labels + runs OCR + Vision on images
- ✅ **Scanned/Image-based PDFs**: Automatically runs OCR + Vision to extract text and understand visuals
- ✅ **Technical drawings**: Extracts text from labels AND describes visual content (shapes, relationships, layout)
- ✅ **Mixed documents**: Combines text extraction + OCR + Vision descriptions

### Example Scenarios:

**Upload a JPG/PNG image:**
- ✅ **OCR extracts**: All visible text in the image
- ✅ **Vision Model describes**: Visual content, objects, layout, context
- ✅ **Searchable**: You can ask "What's in this image?" or "What text is visible?"
- ✅ **Comprehensive**: Both text and visual understanding are indexed

**Upload a PDF of a technical drawing:**
- ✅ **Extracts**: Text labels like "Part A", "Dimension: 5mm", "Title: Assembly Drawing"
- ✅ **OCR extracts**: All visible text from the drawing, dimensions, notes, annotations
- ✅ **Vision Model describes**: Visual content, shapes, relationships between parts, layout, context
- ✅ **Searchable**: You can now ask questions about BOTH text content AND visual understanding
- ✅ **Comprehensive**: Gets both text (OCR) and visual understanding (Vision Model)

### What This Means:

- The system will **automatically detect** image-based PDFs
- It will **run both OCR and Vision Model** without any manual intervention
- Creates **comprehensive chunks** with extracted text AND visual descriptions
- When you ask questions, it can answer based on **text AND visual understanding**
- Questions about drawing content, relationships, and visual elements will work

## Setup Required

To enable OCR + Vision support, you need:

1. **Vision Model** installed via Ollama:
   ```bash
   ollama pull llava
   ```

2. **Poppler** installed (for PDF to image conversion):
   - Windows: https://github.com/oschwartz10612/poppler-windows/releases/
   - macOS: `brew install poppler`
   - Linux: `sudo apt-get install poppler-utils`

3. **Python packages** (installed via requirements.txt):
   - `easyocr` - OCR engine
   - `pdf2image` - PDF to image conversion
   - `Pillow` - Image processing

4. **Configuration** in `.env`:
   ```env
   ENABLE_OCR=true
   ENABLE_VISION=true
   OLLAMA_VISION_MODEL=llava
   ```

See [OCR_SETUP.md](OCR_SETUP.md) and [VISION_MODEL_SETUP.md](VISION_MODEL_SETUP.md) for detailed setup instructions.

## Performance

- **First OCR run**: Slower (downloads EasyOCR models ~100MB, one-time)
- **First Vision run**: Slower (if model not installed, downloads ~4-7GB, one-time)
- **Subsequent runs**: 
  - OCR: ~5-15 seconds per page
  - Vision: ~10-30 seconds per page (depends on hardware)
- **Automatic**: No manual steps needed
- **Offline**: Works offline after initial model downloads

## Current Capabilities Summary

| Document Type | Works? | What Gets Indexed |
|--------------|--------|-------------------|
| **Image Files** (JPG, PNG, GIF, etc.) | ✅ Yes | OCR extracted text + Vision descriptions |
| Text PDFs | ✅ Yes | All text content |
| PDFs with text labels | ✅ Yes | Text labels + OCR text + Vision descriptions |
| Scanned drawings (PDF) | ✅ Yes | OCR extracted text + Vision descriptions |
| Image-based PDFs | ✅ Yes | OCR extracted text + Vision descriptions |
| Technical drawings (PDF) | ✅ Yes | Text labels + OCR text + Vision descriptions (shapes, relationships) |
| Handwritten text | ⚠️ Partial | If legible, OCR can extract |

## Limitations

- **Complex layouts**: May miss some details in very complex diagrams
- **Handwriting**: Works if very legible, accuracy varies
- **Processing time**: Vision model is slower than OCR (but provides better understanding)
- **Memory**: Vision models require more RAM (8GB+ recommended)
- **Languages**: Currently configured for English (can add more in code)

## Recommendation

✅ **OCR + Vision Model are now enabled by default** - just upload your drawings and the system will automatically:
- Extract all visible text (OCR)
- Understand and describe visual content (Vision Model)
- Make everything searchable!

For best results:
- Ensure drawings have clear, readable text
- Higher resolution PDFs work better
- Text labels, annotations, AND visual content will be fully searchable
- Install vision model: `ollama pull llava` (see [VISION_MODEL_SETUP.md](VISION_MODEL_SETUP.md))

