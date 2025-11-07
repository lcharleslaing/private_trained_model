# Vision Model Setup for Understanding Drawings

## Overview

The system now includes **vision model support** using Ollama's open-source vision models (like LLaVA) to understand and describe visual content in:
- **Direct image files** (JPG, PNG, GIF, BMP, TIFF, WEBP)
- PDFs with drawings/images
- Scanned documents
- Technical drawings

## What Vision Models Do

Unlike OCR (which only extracts text), vision models can:
- ✅ **Understand visual content**: Describe what's shown in drawings
- ✅ **Identify relationships**: Understand how parts relate to each other
- ✅ **Describe shapes and layouts**: Explain geometric elements
- ✅ **Context understanding**: Provide context about what the drawing shows
- ✅ **Combined with OCR**: Works alongside OCR for comprehensive understanding

## Supported Models

Ollama supports several open-source vision models:

1. **llava** (Recommended) - LLaVA (Large Language and Vision Assistant)
   - Good balance of speed and accuracy
   - Works well with technical drawings
   - Install: `ollama pull llava`

2. **bakllava** - Alternative LLaVA variant
   - Install: `ollama pull bakllava`

3. **llava-phi3** - LLaVA with Phi-3
   - Smaller, faster model
   - Install: `ollama pull llava-phi3`

## Installation

### Step 1: Install Vision Model

```bash
# Recommended: Install llava
ollama pull llava

# This will download the model (requires internet, one-time)
# Model size: ~4-7GB depending on variant
```

### Step 2: Verify Installation

```bash
ollama list
# Should show: llava (or your chosen model)
```

### Step 3: Configure

In your `.env` file:
```env
ENABLE_VISION=true
OLLAMA_VISION_MODEL=llava
```

## How It Works

### For Direct Image Files (JPG, PNG, GIF, etc.):
1. **OCR**: Automatically runs OCR to extract visible text
2. **Vision Model**: Runs vision model to understand and describe visual content
3. **Combined Results**: Both OCR text and vision descriptions are indexed
4. **Searchable**: You can ask questions about both text and visual content

### For PDFs with Drawings:
1. **Text Extraction**: Tries to extract text normally
2. **OCR**: If little text, runs OCR to extract visible text
3. **Vision Model**: Also runs vision model to understand visual content
4. **Combined Results**: Both OCR text and vision descriptions are indexed
5. **Searchable**: You can ask questions about both text and visual content

### Example Processing:

**For Image Files:**
```
Image File (JPG/PNG/etc.)
  ↓
┌─────────────────┬─────────────────┐
│   OCR Process   │  Vision Process  │
│  (extracts text)│ (understands vis)│
└─────────────────┴─────────────────┘
  ↓
Combined: Text + Descriptions
  ↓
Indexed and Searchable
```

**For PDFs:**
```
PDF with Technical Drawing
  ↓
Extract text → Little text found
  ↓
Convert to images
  ↓
┌─────────────────┬─────────────────┐
│   OCR Process   │  Vision Process  │
│  (extracts text)│ (understands vis)│
└─────────────────┴─────────────────┘
  ↓
Combined: Text + Descriptions
  ↓
Indexed and Searchable
```

## Usage

### For Image Files (JPG, PNG, GIF, etc.):
Just upload your image files! The system will:
1. Automatically run OCR for text extraction
2. Automatically run vision model for visual understanding
3. Combine results for comprehensive indexing

### For PDFs:
Just upload your PDFs as normal! The system will:
1. Automatically detect image-based PDFs
2. Run OCR for text extraction (if little text found)
3. Run vision model for visual understanding (if little text found)
4. Combine results for comprehensive indexing

### What You'll See

**For Image Files:**
```
Running OCR on image: photo.jpg
OCR extracted 1234 characters from image.
Running vision model on image: photo.jpg
Vision model generated 5678 characters of description.
```

**For PDFs:**
```
PDF 'drawing.pdf' has little text. Processing images/drawings...
Running OCR on images...
OCR extracted 1234 characters from images.
Running vision model to understand drawings...
Vision model generated descriptions for 3 pages.
Vision model generated 5678 characters of descriptions.
```

## Performance

- **First run**: Slower (downloads model if not installed)
- **Processing time**: ~10-30 seconds per page (depends on model and hardware)
- **Memory**: Vision models require more RAM (8GB+ recommended)
- **GPU**: Optional but significantly faster if available

## Configuration Options

### Change Vision Model

Edit `.env`:
```env
OLLAMA_VISION_MODEL=bakllava  # or llava-phi3, etc.
```

Then pull the new model:
```bash
ollama pull bakllava
```

### Disable Vision Model

Edit `.env`:
```env
ENABLE_VISION=false
```

The system will still use OCR, just not vision understanding.

## Example Use Cases

### Technical Drawings
- **Question**: "What parts are shown in the assembly drawing?"
- **Vision Model**: Describes all visible components and their relationships

### Schematics
- **Question**: "How are the components connected?"
- **Vision Model**: Explains the wiring/connection layout

### Blueprints
- **Question**: "What are the dimensions shown?"
- **Vision Model**: Identifies and describes all measurements

### Diagrams
- **Question**: "What does this diagram illustrate?"
- **Vision Model**: Provides context and explanation of the diagram

## Limitations

- **Processing time**: Slower than text-only extraction
- **Memory requirements**: Needs more RAM for vision models
- **Accuracy**: Depends on image quality and model capabilities
- **Complex layouts**: May miss some details in very complex drawings

## Troubleshooting

### Vision model not available
- Check model is installed: `ollama list`
- Install model: `ollama pull llava`
- Verify model name in `.env` matches installed model

### Slow processing
- Normal for vision models (10-30s per page)
- Consider using smaller model: `llava-phi3`
- Enable GPU if available (automatic if GPU detected)

### Out of memory
- Vision models need more RAM
- Try smaller model: `llava-phi3`
- Process fewer pages at once

### Vision model errors
- Check Ollama is running: `ollama list`
- Verify model name is correct
- Check console for specific error messages

## Best Practices

1. **Use llava** for best balance of quality and speed
2. **Combine with OCR** for comprehensive understanding
3. **Higher resolution PDFs** work better
4. **Clear, readable drawings** produce better descriptions
5. **GPU acceleration** significantly improves speed (if available)

## Comparison: OCR vs Vision

| Feature | OCR | Vision Model |
|---------|-----|--------------|
| Extracts text | ✅ Yes | ✅ Yes (via description) |
| Understands shapes | ❌ No | ✅ Yes |
| Describes relationships | ❌ No | ✅ Yes |
| Context understanding | ❌ No | ✅ Yes |
| Speed | Fast | Slower |
| Resource usage | Low | Higher |

**Recommendation**: Use both! OCR for text, Vision for understanding.

