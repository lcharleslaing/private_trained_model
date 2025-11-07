# OCR Setup for Drawings and Scanned Documents

## Overview

The system now includes **OCR (Optical Character Recognition)** support to extract text from:
- **Direct image files** (JPG, PNG, GIF, BMP, TIFF, WEBP)
- Technical drawings (PDF or images)
- Scanned PDFs
- Image-based documents
- Handwritten text (if legible)

## How It Works

### For Direct Image Files (JPG, PNG, etc.):
1. **OCR Processing**: Automatically runs OCR on the image
2. **Text Extraction**: Extracts all visible text from the image

### For PDFs:
1. **Standard Text Extraction**: First tries to extract text normally from PDF
2. **OCR Fallback**: If little text is found (< 50 chars), automatically:
   - Converts PDF pages to images
   - Runs OCR on each page
   - Extracts text from images/drawings
   - Combines with any existing text

## Installation

### Windows

1. **Install Poppler** (required for PDF to image conversion, not needed for direct image files):
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases/
   - Extract and add `bin` folder to your PATH
   - Or use: `choco install poppler` (if you have Chocolatey)
   - **Note**: Poppler is only needed for PDF processing. Direct image files (JPG, PNG, etc.) don't require Poppler.

2. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **First Run**: EasyOCR will download models automatically (one-time, ~100MB)

### macOS

1. **Install Poppler**:
   ```bash
   brew install poppler
   ```

2. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Linux

1. **Install Poppler**:
   ```bash
   sudo apt-get install poppler-utils  # Ubuntu/Debian
   # or
   sudo yum install poppler-utils      # CentOS/RHEL
   ```

2. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## Configuration

In your `.env` file:

```env
# Enable/disable OCR (default: true)
ENABLE_OCR=true
```

## Usage

### For Image Files (JPG, PNG, GIF, etc.):
Just upload your image files! The system will:
1. Automatically run OCR on the image
2. Extract all visible text
3. You'll see messages like: `"OCR extracted 1234 characters from image."`

### For PDFs:
Just upload your PDFs as normal! The system will:
1. Try standard text extraction first
2. If little text found, automatically run OCR
3. You'll see messages like:
   - `"PDF 'drawing.pdf' has little text. Attempting OCR on images/drawings..."`
   - `"OCR extracted 1234 characters from images."`

## Performance

- **First OCR run**: Slower (downloads models, ~30-60 seconds)
- **Subsequent runs**: Faster (~5-15 seconds per page)
- **Processing time**: Depends on PDF size and image quality
- **CPU usage**: OCR is CPU-intensive but runs offline

## Supported Formats

- ✅ **Direct image files**: JPG, PNG, GIF, BMP, TIFF, WEBP
- ✅ PDFs with embedded images
- ✅ Scanned PDFs
- ✅ Technical drawings with text labels (PDF or images)
- ✅ Mixed text/image PDFs

## Limitations

- **Handwriting**: Works if very legible, but accuracy varies
- **Complex layouts**: May miss some text in complex diagrams
- **Languages**: Currently configured for English (can add more in code)
- **Speed**: OCR is slower than text extraction (but automatic)

## Troubleshooting

### "OCR processing failed" error:
- Check that Poppler is installed and in PATH
- Verify `pdf2image` is installed: `pip install pdf2image`
- Try setting `ENABLE_OCR=false` to disable OCR

### OCR not working:
- Ensure `ENABLE_OCR=true` in `.env`
- Check that EasyOCR installed: `pip list | grep easyocr`
- First run downloads models (requires internet once)

### Slow performance:
- Normal for first run (model download)
- Consider reducing DPI in code (currently 200) for faster processing
- OCR is CPU-intensive - be patient with large documents

## Advanced Configuration

To change OCR settings, edit `backend/services/document_service.py`:

```python
# Change DPI (lower = faster, less quality)
images = convert_from_path(str(file_path), dpi=150)  # Default: 200

# Add more languages
self._ocr_reader = easyocr.Reader(['en', 'es', 'fr'], gpu=False)

# Enable GPU (if available)
self._ocr_reader = easyocr.Reader(['en'], gpu=True)
```

