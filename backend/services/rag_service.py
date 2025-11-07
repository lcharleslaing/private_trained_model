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
        """Retrieve relevant document chunks based on query with similarity filtering - OPTIMIZED"""
        # Get query embedding
        query_embedding = self.document_service.embedding_model.encode([query])[0]
        query_embedding_np = np.array(query_embedding)
        
        # Get all chunks with embeddings (uses cache if available)
        all_chunks = self.document_service.get_all_chunks_cached()
        
        if not all_chunks:
            return []
        
        # OPTIMIZATION: Vectorized similarity calculation using numpy
        # Stack all embeddings into a matrix for batch computation
        embeddings_matrix = np.array([chunk["embedding"] for chunk in all_chunks])
        
        # Calculate cosine similarities for all chunks at once (much faster)
        # Normalize query embedding
        query_norm = np.linalg.norm(query_embedding_np)
        if query_norm == 0:
            return []
        
        # Normalize all embeddings
        embeddings_norms = np.linalg.norm(embeddings_matrix, axis=1, keepdims=True)
        embeddings_norms[embeddings_norms == 0] = 1  # Avoid division by zero
        
        # Calculate dot products and normalize
        dot_products = np.dot(embeddings_matrix, query_embedding_np)
        similarities_array = dot_products / (embeddings_norms.flatten() * query_norm)
        
        # Filter by threshold and get top_k indices
        above_threshold = similarities_array >= self.similarity_threshold
        if not np.any(above_threshold):
            return []
        
        # Get top_k indices
        top_indices = np.argsort(similarities_array[above_threshold])[-top_k:][::-1]
        # Map back to original indices
        threshold_indices = np.where(above_threshold)[0]
        selected_indices = threshold_indices[top_indices]
        
        # Format results
        results = []
        for idx in selected_indices:
            chunk = all_chunks[idx]
            results.append({
                "content": chunk.get("content", ""),
                "source": chunk["source"],
                "similarity": float(similarities_array[idx]),
                "chunk_id": chunk["chunk_id"]
            })
        
        return results
    
    def has_relevant_context(self, query: str, top_k: int = 3) -> bool:
        """Check if there are any relevant documents for the query"""
        relevant_docs = self.get_relevant_documents(query, top_k)
        return len(relevant_docs) > 0

