from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from services.ollama_service import OllamaService
from services.document_service import DocumentService
from services.rag_service import RAGService

app = FastAPI(title="Private GPT-OSS Chat API")

# Get configuration from environment variables
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "3"))

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services with environment variables
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
ollama_service = OllamaService(base_url=ollama_base_url, model=ollama_model)

documents_dir = Path(os.getenv("DOCUMENTS_DIR", "documents"))
embeddings_dir = Path(os.getenv("EMBEDDINGS_DIR", "embeddings"))
document_service = DocumentService(
    documents_dir=documents_dir,
    embeddings_dir=embeddings_dir
)
rag_service = RAGService(document_service)

# Ensure documents directory exists
DOCUMENTS_DIR = documents_dir
DOCUMENTS_DIR.mkdir(exist_ok=True)


class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: Optional[List[str]] = []


@app.get("/")
async def root():
    return {"message": "Private GPT-OSS Chat API", "status": "online"}


@app.get("/health")
async def health():
    return {"status": "healthy", "ollama_available": ollama_service.check_connection()}


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Send a chat message and get a response with RAG"""
    try:
        # Get relevant documents using RAG
        relevant_docs = rag_service.get_relevant_documents(message.message, top_k=RAG_TOP_K)
        
        # Build context from documents
        context = "\n\n".join([doc["content"] for doc in relevant_docs])
        
        # Generate response using Ollama with context
        response = await ollama_service.chat(
            user_message=message.message,
            context=context,
            conversation_id=message.conversation_id
        )
        
        # Extract sources
        sources = [doc["source"] for doc in relevant_docs] if relevant_docs else []
        
        return ChatResponse(
            response=response["message"],
            conversation_id=response["conversation_id"],
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Save file
        file_path = DOCUMENTS_DIR / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process and index document
        result = await document_service.process_document(file_path)
        
        return {
            "message": "Document processed successfully",
            "filename": file.filename,
            "chunks": result["chunks"],
            "document_id": result["document_id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents")
async def list_documents():
    """List all processed documents"""
    documents = document_service.list_documents()
    return {"documents": documents}


@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document"""
    try:
        document_service.delete_document(document_id)
        return {"message": "Document deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/reindex")
async def reindex_documents():
    """Reindex all documents"""
    try:
        result = await document_service.reindex_all()
        return {"message": "Documents reindexed", "count": result["count"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host=BACKEND_HOST, port=BACKEND_PORT)

