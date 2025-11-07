# Quick Setup Guide

## Step 1: Install Ollama

1. Download Ollama from https://ollama.ai
2. Install and start Ollama
3. Pull a model:
   ```bash
   ollama pull llama3.2
   ```

## Step 2: Install Vision Model (for understanding drawings)

```bash
# Install LLaVA vision model via Ollama
ollama pull llava

# This downloads the model (requires internet, one-time, ~4-7GB)
```

## Step 3: Install Poppler (for OCR support)

**Windows:**
- Download from: https://github.com/oschwartz10612/poppler-windows/releases/
- Extract and add `bin` folder to PATH
- Or: `choco install poppler`

**macOS:**
```bash
brew install poppler
```

**Linux:**
```bash
sudo apt-get install poppler-utils  # Ubuntu/Debian
# or
sudo yum install poppler-utils      # CentOS/RHEL
```

## Step 4: Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**Note:** First OCR run will download EasyOCR models (~100MB, one-time, requires internet)

## Step 5: Frontend Setup

```bash
cd frontend
npm install
npm install -D daisyui@latest
```

## Step 6: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env if needed (defaults work for most setups)
```

## Step 7: Run the Application

### Terminal 1 - Backend:
```bash
cd backend
# Activate venv if not already
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # macOS/Linux
python main.py
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

## Step 8: Access the Application

Open your browser to: **http://localhost:5173**

## First Time Notes

- The embedding model will download on first use (requires internet once)
- EasyOCR models will download on first OCR use (requires internet once)
- Vision model (llava) should already be installed via Step 2
- Upload documents in the "Documents" tab
- Start chatting in the "Chat" tab
- OCR automatically extracts text from drawings/scanned documents
- Vision model automatically understands visual content in drawings
- All processing happens locally - no internet needed after initial setup!

## Features

- ✅ **Text-based documents**: PDF, Word (DOCX, DOC), Excel (XLSX, XLS), TXT files
- ✅ **Image files**: JPG, PNG, GIF, BMP, TIFF, WEBP with OCR + Vision model
- ✅ **Excel support**: Extracts data from all sheets, preserves structure
- ✅ **Word support**: Extracts text and tables from Word documents
- ✅ **Drawings/Scanned PDFs**: Automatic OCR + Vision model extraction
- ✅ **Direct images**: OCR extracts text, Vision model describes visual content
- ✅ **Visual understanding**: Vision model describes drawings and visual content
- ✅ **Offline operation**: Works completely offline after setup
- ✅ **Document-only answers**: Only answers from your documents

