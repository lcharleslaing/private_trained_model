import numpy as np
import os
from typing import List, Dict, Optional
from services.document_service import DocumentService
from dotenv import load_dotenv

load_dotenv()


class RAGService:
    def __init__(self, document_service: DocumentService, similarity_threshold: Optional[float] = None):
        self.document_service = document_service
        # Get similarity threshold from environment (default 0.3)
        # Lower threshold = more strict (only very relevant docs)
        # Higher threshold = more lenient (allows less relevant docs)
        self.similarity_threshold = similarity_threshold or float(os.getenv("SIMILARITY_THRESHOLD", "0.3"))
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def get_relevant_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant document chunks based on query with similarity filtering"""
        # Get query embedding
        query_embedding = self.document_service.embedding_model.encode([query])[0]
        
        # Get all chunks with embeddings
        all_chunks = self.document_service.get_all_chunks()
        
        if not all_chunks:
            return []
        
        # Calculate similarities
        similarities = []
        for chunk in all_chunks:
            similarity = self._cosine_similarity(query_embedding, chunk["embedding"])
            similarities.append({
                "chunk": chunk,
                "similarity": similarity
            })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Filter by similarity threshold and get top_k
        filtered_results = [
            item for item in similarities 
            if item["similarity"] >= self.similarity_threshold
        ][:top_k]
        
        # Format results
        results = []
        for item in filtered_results:
            chunk = item["chunk"]
            results.append({
                "content": chunk.get("content", ""),
                "source": chunk["source"],
                "similarity": item["similarity"],
                "chunk_id": chunk["chunk_id"]
            })
        
        return results
    
    def has_relevant_context(self, query: str, top_k: int = 3) -> bool:
        """Check if there are any relevant documents for the query"""
        relevant_docs = self.get_relevant_documents(query, top_k)
        return len(relevant_docs) > 0

