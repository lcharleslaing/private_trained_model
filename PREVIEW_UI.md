# Preview the UI Without Full Setup

You can preview the chat interface without setting up Ollama or downloading models.

## Quick Start - Frontend Only

### Windows:
```bash
start_frontend_only.bat
```

### macOS/Linux:
```bash
./start_frontend_only.sh
```

Or manually:
```bash
cd frontend
npm install  # First time only
npm run dev
```

Then open: **http://localhost:5173**

## What You'll See

✅ **Working:**
- Full UI interface loads
- Document management tab
- Chat interface layout
- All styling and components

⚠️ **Not Working (until backend/Ollama setup):**
- Chat messages (will show connection errors)
- Document upload (will fail)
- Health status indicators (will show as offline)

## Full Setup Later

When you're ready to test with Ollama:

1. **Install Ollama** from https://ollama.ai
2. **Install Poppler** (for OCR support):
   - Windows: https://github.com/oschwartz10612/poppler-windows/releases/
   - macOS: `brew install poppler`
   - Linux: `sudo apt-get install poppler-utils`
3. **Pull models:**
   ```bash
   ollama pull llama3.2
   ollama pull llava  # For vision model (optional but recommended)
   ```
4. **Set up environment:**
   ```bash
   cp .env.example .env
   ```
5. **Start backend:**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or: source venv/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   python main.py
   ```
6. **Frontend is already running** - just refresh the browser!

**Note:** First run will download embedding and OCR models (requires internet once)

## Testing the UI

Even without the backend, you can:
- Navigate between Chat and Documents tabs
- See the interface layout
- Check responsive design
- Review the UI components

The interface will show connection errors when you try to use features, but you can see how everything looks and works!

