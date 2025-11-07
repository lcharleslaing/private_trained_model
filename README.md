# Private GPT-OSS Chat Interface

A private, offline-capable chat interface that uses local LLM (via Ollama) and can read from your own set of documents using Retrieval Augmented Generation (RAG).

## Features

- 🤖 **Local LLM Integration**: Uses Ollama to run GPT-OSS models completely offline
- 📄 **Document Processing**: Upload and process PDF, DOCX, and TXT files
- 🔍 **RAG (Retrieval Augmented Generation)**: Automatically retrieves relevant document chunks to provide context-aware responses
- 🔒 **100% Private**: All processing happens locally, no data leaves your machine
- 💬 **Modern Chat Interface**: Beautiful UI built with React, Tailwind CSS, and DaisyUI
- 📊 **Document Management**: Upload, view, and delete documents through the web interface

## Prerequisites

1. **Python 3.8+** installed
2. **Node.js 18+** and npm installed
3. **Ollama** installed and running locally
   - Download from: https://ollama.ai
   - After installation, pull a model: `ollama pull llama3.2` (or another model of your choice)

## Installation

### 1. Install Ollama and Pull a Model

```bash
# Download and install Ollama from https://ollama.ai
# Then pull a model (example with llama3.2):
ollama pull llama3.2

# Or use other models like:
# ollama pull mistral
# ollama pull codellama
```

### 2. Set Up Backend

```bash
cd backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Note: DaisyUI needs to be installed separately
npm install -D daisyui@latest
```

## Running the Application

### Quick Start

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Start the servers:**

   **Option A: Using startup scripts (easiest)**
   - Windows: Run `start_backend.bat` and `start_frontend.bat` in separate terminals
   - macOS/Linux: Run `./start_backend.sh` and `./start_frontend.sh` in separate terminals

   **Option B: Manual start**
   - See [START_SERVER.md](START_SERVER.md) for detailed instructions

3. **Access the application:** Open `http://localhost:5173` in your browser

### Detailed Instructions

See [START_SERVER.md](START_SERVER.md) for complete setup and troubleshooting guide.

## Usage

1. **Upload Documents**: 
   - Go to the "Documents" tab
   - Upload PDF, DOCX, or TXT files
   - Documents will be processed and indexed automatically

2. **Chat**:
   - Go to the "Chat" tab
   - Type your questions
   - The system will automatically retrieve relevant document chunks and use them to provide context-aware responses

3. **Manage Documents**:
   - View all uploaded documents
   - Delete documents you no longer need
   - Reindex all documents if needed

## Project Structure

```
private_trained_model/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── services/
│   │   ├── ollama_service.py   # Ollama integration
│   │   ├── document_service.py # Document processing & embeddings
│   │   └── rag_service.py      # RAG retrieval logic
│   ├── documents/              # Uploaded documents (created automatically)
│   ├── embeddings/             # Stored embeddings (created automatically)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx
│   │   │   └── DocumentManager.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
└── README.md
```

## Configuration

All configuration is done through the `.env` file. Copy `.env.example` to `.env` and edit as needed:

### Key Configuration Options

- **Ollama Settings:**
  - `OLLAMA_BASE_URL` - Ollama server URL (default: http://localhost:11434)
  - `OLLAMA_MODEL` - Model to use (default: llama3.2)

- **Server Settings:**
  - `BACKEND_PORT` - Backend server port (default: 8000)
  - `FRONTEND_PORT` - Frontend dev server port (default: 5173)

- **Document Processing:**
  - `EMBEDDING_MODEL` - Embedding model (default: all-MiniLM-L6-v2)
  - `CHUNK_SIZE` - Text chunk size (default: 500)
  - `CHUNK_OVERLAP` - Overlap between chunks (default: 50)

- **RAG Settings:**
  - `RAG_TOP_K` - Number of document chunks to retrieve (default: 3)
  - `SIMILARITY_THRESHOLD` - Minimum similarity score (0.0-1.0) to consider a document relevant (default: 0.3, lower = more strict)

### Example: Changing the Model

Edit `.env`:
```env
OLLAMA_MODEL=mistral
```

### Example: Using a Different Embedding Model

Edit `.env`:
```env
EMBEDDING_MODEL=all-mpnet-base-v2
```

Other good embedding model options:
- `all-mpnet-base-v2` (better quality, slower)
- `paraphrase-MiniLM-L6-v2` (similar to default)

### Strict Mode: Document-Only Answers

The system is configured to **ONLY answer questions based on your uploaded documents**. It will refuse to answer questions that aren't covered in your documents.

**How it works:**
- If no documents are uploaded: System refuses to answer
- If question isn't in documents: System refuses to answer
- If documents are relevant: System answers using only the document content

**Adjusting Strictness:**

The `SIMILARITY_THRESHOLD` controls how strict the system is:
- **Lower values (0.2-0.3)**: More strict - only very relevant documents are used
- **Higher values (0.4-0.6)**: More lenient - allows less relevant documents

Example: To make it more strict, edit `.env`:
```env
SIMILARITY_THRESHOLD=0.25
```

To make it more lenient:
```env
SIMILARITY_THRESHOLD=0.4
```

## Troubleshooting

### Ollama Connection Issues

- Ensure Ollama is running: `ollama list` should show your models
- Check if Ollama is accessible: `curl http://localhost:11434/api/tags`
- Verify the model is pulled: `ollama list`

### Document Processing Errors

- Ensure documents are in supported formats (PDF, DOCX, DOC, TXT)
- Check file permissions
- For PDFs, ensure they're not password-protected or corrupted

### Frontend Connection Issues

- Verify backend is running on port 8000
- Check CORS settings in `backend/main.py` if accessing from different ports
- Check browser console for errors

## Offline Usage

Once set up, this application works completely offline:

1. **Ollama models** are downloaded locally
2. **Embedding models** are downloaded on first use (requires internet once)
3. **All processing** happens on your machine
4. **No API keys** or external services required

After the initial setup and model downloads, you can disconnect from the internet and use the application fully offline.

## License

This project is provided as-is for private use.

## Notes

- The first time you run the application, sentence-transformers will download the embedding model (requires internet)
- Document processing may take time for large files
- Ollama models require sufficient RAM (8GB+ recommended for most models)
- For better performance, use GPU-accelerated Ollama if available

# private_trained_model
