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
    """Send a chat message and get a response with RAG - only answers from documents"""
    try:
        # Check if we have any documents at all
        all_docs = document_service.list_documents()
        if not all_docs:
            return ChatResponse(
                response="I can only answer questions based on the documents provided. No documents have been uploaded yet. Please upload documents first in the Documents tab.",
                conversation_id=message.conversation_id or "conv_0",
                sources=[]
            )
        
        # Get relevant documents using RAG
        relevant_docs = rag_service.get_relevant_documents(message.message, top_k=RAG_TOP_K)
        
        # Check if we have relevant context
        if not relevant_docs:
            # No relevant documents found - refuse to answer
            return ChatResponse(
                response="I can only answer questions based on the documents provided. The information needed to answer this question is not available in the provided documents. Please ask questions related to the uploaded documents.",
                conversation_id=message.conversation_id or "conv_0",
                sources=[]
            )
        
        # Build context from documents
        context = "\n\n".join([f"[From {doc['source']}]:\n{doc['content']}" for doc in relevant_docs])
        
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
async def upload_document(file: UploadFile = File(...), force_reprocess: bool = False):
    """Upload and process a document - adds to the expanding document database"""
    try:
        # Save file
        file_path = DOCUMENTS_DIR / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Check if document already exists
        if document_service.document_exists(file_path) and not force_reprocess:
            existing_doc = document_service.embeddings_index[document_service._get_document_id(file_path)]
            return {
                "message": "Document already exists in database",
                "filename": file.filename,
                "chunks": existing_doc["chunks"],
                "document_id": document_service._get_document_id(file_path),
                "already_exists": True
            }
        
        # Process and index document (adds to expanding context pool)
        result = await document_service.process_document(file_path, force_reprocess=force_reprocess)
        
        # Get updated stats
        stats = document_service.get_document_stats()
        
        return {
            "message": result.get("message", "Document processed and added to database"),
            "filename": file.filename,
            "chunks": result["chunks"],
            "document_id": result["document_id"],
            "already_exists": result.get("already_exists", False),
            "database_stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents")
async def list_documents():
    """List all processed documents in the database"""
    documents = document_service.list_documents()
    stats = document_service.get_document_stats()
    return {
        "documents": documents,
        "stats": stats
    }


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

