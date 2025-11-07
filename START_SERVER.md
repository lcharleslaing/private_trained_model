# How to Start the Server

## Quick Start

### Option 1: Using the Startup Scripts (Recommended)

**Windows:**
```bash
# Start backend
.\start_backend.bat

# In a new terminal, start frontend
.\start_frontend.bat
```

**macOS/Linux:**
```bash
# Start backend
./start_backend.sh

# In a new terminal, start frontend
./start_frontend.sh
```

### Option 2: Manual Start

#### Step 1: Set Up Environment (First Time Only)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` if needed (defaults work for most setups)

#### Step 2: Install Dependencies (First Time Only)

**Backend:**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

#### Step 3: Ensure Ollama is Running

Make sure Ollama is installed and running:
```bash
ollama list
```

If Ollama isn't running, start it:
```bash
ollama serve
```

#### Step 4: Start the Backend Server

```bash
cd backend

# Activate virtual environment if not already active
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start the server
python main.py
```

The backend will start on `http://localhost:8000` (or your configured port).

#### Step 5: Start the Frontend (New Terminal)

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173` (or your configured port).

## Access the Application

Open your browser to: **http://localhost:5173**

## Environment Variables

All configuration is done through the `.env` file. Key variables:

- `OLLAMA_BASE_URL` - Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL` - Model to use (default: llama3.2)
- `BACKEND_PORT` - Backend server port (default: 8000)
- `FRONTEND_PORT` - Frontend dev server port (default: 5173)
- `EMBEDDING_MODEL` - Embedding model name (default: all-MiniLM-L6-v2)
- `RAG_TOP_K` - Number of document chunks to retrieve (default: 3)

See `.env.example` for all available options.

## Troubleshooting

### Backend won't start
- Check if port 8000 is already in use
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Frontend won't start
- Check if port 5173 is already in use
- Ensure dependencies are installed: `npm install`
- Check if DaisyUI is installed: `npm install -D daisyui`

### Ollama connection errors
- Verify Ollama is running: `ollama list`
- Check `OLLAMA_BASE_URL` in `.env` matches your Ollama setup
- Ensure the model is pulled: `ollama pull llama3.2`

### Port conflicts
- Change ports in `.env` file
- Update `CORS_ORIGINS` if using different frontend port

