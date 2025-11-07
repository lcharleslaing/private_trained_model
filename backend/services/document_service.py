from pathlib import Path
import hashlib
import json
from typing import List, Dict, Optional
import datetime
import PyPDF2
import docx
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os
from dotenv import load_dotenv

load_dotenv()


class DocumentService:
    def __init__(self, documents_dir: Path = Path("documents"), embeddings_dir: Path = Path("embeddings")):
        self.documents_dir = documents_dir
        self.embeddings_dir = embeddings_dir
        self.embeddings_dir.mkdir(exist_ok=True)
        
        # Get embedding model from environment
        embedding_model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        
        # Initialize embedding model (runs locally, no internet needed after first download)
        self.embedding_model = SentenceTransformer(embedding_model_name)
        
        # Load existing embeddings
        self.embeddings_index: Dict[str, List[Dict]] = {}
        self._load_embeddings()
    
    def _load_embeddings(self):
        """Load existing embeddings from disk"""
        index_file = self.embeddings_dir / "index.json"
        if index_file.exists():
            with open(index_file, "r") as f:
                self.embeddings_index = json.load(f)
    
    def _save_embeddings(self):
        """Save embeddings index to disk"""
        index_file = self.embeddings_dir / "index.json"
        with open(index_file, "w") as f:
            json.dump(self.embeddings_index, f, indent=2)
    
    def _get_document_id(self, file_path: Path) -> str:
        """Generate a unique document ID based on file content"""
        # Use file content hash for better duplicate detection
        try:
            with open(file_path, "rb") as f:
                file_content = f.read()
            return hashlib.md5(file_content).hexdigest()
        except:
            # Fallback to filename + mtime if can't read
            content = f"{file_path.name}_{file_path.stat().st_mtime}"
            return hashlib.md5(content.encode()).hexdigest()
    
    def document_exists(self, file_path: Path) -> bool:
        """Check if a document with the same content already exists"""
        doc_id = self._get_document_id(file_path)
        return doc_id in self.embeddings_index
    
    def _extract_text_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text
    
    def _extract_text_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    def _extract_text_from_txt(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")
    
    def _extract_text(self, file_path: Path) -> str:
        """Extract text from various file formats"""
        suffix = file_path.suffix.lower()
        
        if suffix == ".pdf":
            return self._extract_text_from_pdf(file_path)
        elif suffix in [".docx", ".doc"]:
            return self._extract_text_from_docx(file_path)
        elif suffix == ".txt":
            return self._extract_text_from_txt(file_path)
        else:
            raise Exception(f"Unsupported file format: {suffix}")
    
    def _chunk_text(self, text: str, chunk_size: Optional[int] = None, overlap: Optional[int] = None) -> List[str]:
        """Split text into overlapping chunks"""
        # Get chunk settings from environment
        if chunk_size is None:
            chunk_size = int(os.getenv("CHUNK_SIZE", "500"))
        if overlap is None:
            overlap = int(os.getenv("CHUNK_OVERLAP", "50"))
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    async def process_document(self, file_path: Path, force_reprocess: bool = False) -> Dict:
        """Process a document: extract text, chunk it, and create embeddings
        
        Args:
            file_path: Path to the document file
            force_reprocess: If True, reprocess even if document already exists
        """
        # Generate document ID
        document_id = self._get_document_id(file_path)
        
        # Check if document already exists
        if document_id in self.embeddings_index and not force_reprocess:
            existing_doc = self.embeddings_index[document_id]
            return {
                "document_id": document_id,
                "chunks": existing_doc["chunks"],
                "chunks_data": [],
                "message": "Document already exists in database",
                "already_exists": True
            }
        
        # Extract text
        text = self._extract_text(file_path)
        
        if not text.strip():
            raise Exception("Document appears to be empty")
        
        # Chunk the text
        chunks = self._chunk_text(text)
        
        # Create embeddings for each chunk
        embeddings = self.embedding_model.encode(chunks, show_progress_bar=False)
        
        # Store chunks and embeddings
        document_chunks = []
        chunks_metadata = {}
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = f"{document_id}_chunk_{i}"
            chunk_data = {
                "chunk_id": chunk_id,
                "content": chunk,
                "document_id": document_id,
                "source": file_path.name,
                "chunk_index": i
            }
            document_chunks.append(chunk_data)
            
            # Store chunk metadata
            chunks_metadata[chunk_id] = {
                "content": chunk,
                "document_id": document_id,
                "source": file_path.name,
                "chunk_index": i
            }
            
            # Store embedding
            embedding_file = self.embeddings_dir / f"{chunk_id}.pkl"
            with open(embedding_file, "wb") as f:
                pickle.dump(embedding, f)
        
        # Store chunks metadata
        chunks_file = self.embeddings_dir / f"{document_id}_chunks.json"
        with open(chunks_file, "w", encoding="utf-8") as f:
            json.dump(chunks_metadata, f, indent=2, ensure_ascii=False)
        
        # Update index with metadata
        self.embeddings_index[document_id] = {
            "filename": file_path.name,
            "chunks": len(document_chunks),
            "chunk_ids": [chunk["chunk_id"] for chunk in document_chunks],
            "uploaded_at": datetime.datetime.now().isoformat(),
            "file_size": file_path.stat().st_size,
            "file_path": str(file_path)
        }
        
        # Save index
        self._save_embeddings()
        
        return {
            "document_id": document_id,
            "chunks": len(document_chunks),
            "chunks_data": document_chunks,
            "already_exists": False,
            "message": "Document processed and added to database"
        }
    
    def list_documents(self) -> List[Dict]:
        """List all processed documents with metadata"""
        documents = []
        for doc_id, doc_info in self.embeddings_index.items():
            doc_data = {
                "document_id": doc_id,
                "filename": doc_info["filename"],
                "chunks": doc_info["chunks"],
                "uploaded_at": doc_info.get("uploaded_at", "Unknown"),
                "file_size": doc_info.get("file_size", 0)
            }
            documents.append(doc_data)
        # Sort by upload date (newest first)
        documents.sort(key=lambda x: x.get("uploaded_at", ""), reverse=True)
        return documents
    
    def get_document_stats(self) -> Dict:
        """Get statistics about the document database"""
        total_docs = len(self.embeddings_index)
        total_chunks = sum(doc_info.get("chunks", 0) for doc_info in self.embeddings_index.values())
        total_size = sum(doc_info.get("file_size", 0) for doc_info in self.embeddings_index.values())
        
        return {
            "total_documents": total_docs,
            "total_chunks": total_chunks,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }
    
    def delete_document(self, document_id: str):
        """Delete a document and its embeddings"""
        if document_id not in self.embeddings_index:
            raise Exception("Document not found")
        
        # Delete embedding files
        chunk_ids = self.embeddings_index[document_id]["chunk_ids"]
        for chunk_id in chunk_ids:
            embedding_file = self.embeddings_dir / f"{chunk_id}.pkl"
            if embedding_file.exists():
                embedding_file.unlink()
        
        # Delete chunks metadata file
        chunks_file = self.embeddings_dir / f"{document_id}_chunks.json"
        if chunks_file.exists():
            chunks_file.unlink()
        
        # Remove from index
        del self.embeddings_index[document_id]
        self._save_embeddings()
    
    def get_all_chunks(self) -> List[Dict]:
        """Get all document chunks with their embeddings"""
        all_chunks = []
        for doc_id, doc_info in self.embeddings_index.items():
            # Load chunks metadata for this document
            chunks_file = self.embeddings_dir / f"{doc_id}_chunks.json"
            chunks_metadata = {}
            if chunks_file.exists():
                with open(chunks_file, "r", encoding="utf-8") as f:
                    chunks_metadata = json.load(f)
            
            for chunk_id in doc_info["chunk_ids"]:
                embedding_file = self.embeddings_dir / f"{chunk_id}.pkl"
                if embedding_file.exists():
                    with open(embedding_file, "rb") as f:
                        embedding = pickle.load(f)
                    
                    # Get chunk metadata
                    chunk_meta = chunks_metadata.get(chunk_id, {})
                    
                    all_chunks.append({
                        "chunk_id": chunk_id,
                        "document_id": doc_id,
                        "source": doc_info["filename"],
                        "content": chunk_meta.get("content", ""),
                        "embedding": embedding
                    })
        return all_chunks
    
    async def reindex_all(self) -> Dict:
        """Reindex all documents in the documents directory"""
        count = 0
        for file_path in self.documents_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in [".pdf", ".docx", ".doc", ".txt"]:
                try:
                    await self.process_document(file_path)
                    count += 1
                except Exception as e:
                    print(f"Error processing {file_path.name}: {str(e)}")
        return {"count": count}

