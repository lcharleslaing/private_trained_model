# Quick Setup Guide

## Step 1: Install Ollama

1. Download Ollama from https://ollama.ai
2. Install and start Ollama
3. Pull a model:
   ```bash
   ollama pull llama3.2
   ```

## Step 2: Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Step 3: Frontend Setup

```bash
cd frontend
npm install
```

## Step 4: Run the Application

### Terminal 1 - Backend:
```bash
cd backend
# Activate venv if not already
python main.py
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

## Step 5: Access the Application

Open your browser to: http://localhost:5173

## First Time Notes

- The embedding model will download on first use (requires internet once)
- Upload documents in the "Documents" tab
- Start chatting in the "Chat" tab
- All processing happens locally - no internet needed after initial setup!

