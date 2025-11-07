# Direct Image File Support

## Supported Image Formats

The system now supports direct image file uploads:

- ✅ **JPG/JPEG** - Most common photo format
- ✅ **PNG** - Screenshots, diagrams, transparent images
- ✅ **GIF** - Animated or static images
- ✅ **BMP** - Windows bitmap format
- ✅ **TIFF** - High-quality scanned documents
- ✅ **WEBP** - Modern web image format

## How It Works

When you upload an image file, the system automatically:

1. **OCR Processing** (if `ENABLE_OCR=true`):
   - Extracts all visible text from the image
   - Works on photos, screenshots, scanned documents, drawings
   - Example: "Extracted text: 'Meeting Notes', 'Date: 2024-01-15'"

2. **Vision Model Processing** (if `ENABLE_VISION=true`):
   - Understands and describes visual content
   - Identifies objects, scenes, layout, relationships
   - Example: "This image shows a technical diagram with three connected components labeled A, B, and C. Component A appears to be a rectangular box at the top, connected to component B below it..."

3. **Combined Indexing**:
   - Both OCR text and vision descriptions are stored
   - Made searchable through the RAG system
   - You can ask questions about both text AND visual content

## Usage Examples

### Upload an Image

1. Go to the "Documents" tab
2. Click "Choose File" or drag and drop
3. Select your image file (JPG, PNG, etc.)
4. Wait for processing (OCR + Vision model)
5. Image is now searchable!

### Ask Questions About Images

**About Text in Images:**
- "What text is visible in the uploaded image?"
- "What does the label say on component A?"
- "What are the dimensions shown in the drawing?"

**About Visual Content:**
- "What's in this image?"
- "Describe the layout of the diagram"
- "What objects are visible?"
- "What is the relationship between the components?"

**Combined Questions:**
- "What does the text say and what does the image show?"
- "Describe both the visual content and any text labels"

## Setup Requirements

### 1. Enable OCR (for text extraction)

In your `.env` file:
```env
ENABLE_OCR=true
```

**First run**: EasyOCR will download models (~100MB, one-time, requires internet)

### 2. Enable Vision Model (for visual understanding)

In your `.env` file:
```env
ENABLE_VISION=true
OLLAMA_VISION_MODEL=llava
```

**Install vision model**:
```bash
ollama pull llava
```

This downloads the model (~4-7GB, one-time, requires internet)

### 3. Python Packages

Already included in `requirements.txt`:
- `easyocr` - OCR engine
- `Pillow` - Image processing

## What Gets Extracted

### Example: Technical Drawing Image

**OCR Output:**
```
[OCR Extracted Text]:
Part A
Dimension: 5mm
Title: Assembly Drawing
Component B
```

**Vision Model Output:**
```
[Vision Model Description]:
This image shows a technical engineering diagram with multiple labeled components. 
The diagram appears to be a mechanical assembly drawing with three main parts: 
Part A (top left, rectangular), Component B (center, circular), and an unlabeled 
component (bottom right, triangular). The components are connected by lines 
indicating relationships or connections. The drawing includes dimension annotations 
and appears to be a professional technical illustration.
```

**Result**: Both are indexed and searchable!

## Performance

- **First OCR run**: Slower (~30-60 seconds, downloads models)
- **Subsequent OCR**: ~5-15 seconds per image
- **First Vision run**: Slower (~60-120 seconds, downloads model if not installed)
- **Subsequent Vision**: ~10-30 seconds per image (depends on hardware)
- **Combined**: ~15-45 seconds total per image (after initial setup)

## Use Cases

### 1. Screenshots
- Upload UI screenshots
- OCR extracts button labels, text
- Vision model describes interface layout
- Ask: "What buttons are visible?" or "Describe the interface"

### 2. Technical Drawings
- Upload CAD drawings, schematics
- OCR extracts labels, dimensions
- Vision model describes shapes, relationships
- Ask: "What components are connected?" or "What are the dimensions?"

### 3. Scanned Documents
- Upload scanned PDFs or images
- OCR extracts all text
- Vision model provides context
- Ask: "What does this document say?" or "What type of document is this?"

### 4. Photos with Text
- Upload photos of whiteboards, signs, labels
- OCR extracts visible text
- Vision model describes scene
- Ask: "What text is in the image?" or "What does the sign say?"

### 5. Charts and Diagrams
- Upload data visualizations, flowcharts
- OCR extracts labels, axis labels
- Vision model describes data, relationships
- Ask: "What does this chart show?" or "What are the data trends?"

## Limitations

- **Handwriting**: Works if very legible, accuracy varies
- **Complex layouts**: May miss some details in very complex diagrams
- **Languages**: Currently configured for English (can add more in code)
- **Processing time**: Vision model is slower than OCR (but provides better understanding)
- **Memory**: Vision models require more RAM (8GB+ recommended)
- **Large images**: Very high-resolution images may take longer to process

## Best Practices

1. **Clear Images**: Higher resolution and clearer images work better
2. **Text Legibility**: Ensure text is readable for best OCR results
3. **Enable Both**: Use both OCR and Vision for comprehensive understanding
4. **Batch Upload**: You can upload multiple images at once
5. **Organize**: Name your image files descriptively for easier management

## Troubleshooting

### OCR Not Working
- Check `ENABLE_OCR=true` in `.env`
- First run downloads models (requires internet)
- Check console for error messages

### Vision Model Not Working
- Check `ENABLE_VISION=true` in `.env`
- Install model: `ollama pull llava`
- Check if Ollama is running: `ollama list`

### Slow Processing
- Normal for first run (model downloads)
- Vision model is slower than OCR
- Consider processing images in batches

### No Text Extracted
- Image may not contain text
- Text may be too small or unclear
- Try higher resolution image

## Comparison: Images vs PDFs with Images

| Feature | Direct Image Files | PDFs with Images |
|---------|-------------------|------------------|
| OCR | ✅ Yes | ✅ Yes (if little text) |
| Vision Model | ✅ Yes | ✅ Yes (if little text) |
| Text Extraction | ✅ OCR only | ✅ Text + OCR |
| Multi-page | ❌ Single image | ✅ Multiple pages |
| Processing | Faster (single image) | Slower (per page) |

**Recommendation**: 
- Use **direct image files** for single images, screenshots, photos
- Use **PDFs** for multi-page documents, scanned books, reports

