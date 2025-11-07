import numpy as np
from typing import List, Dict
from services.document_service import DocumentService


class RAGService:
    def __init__(self, document_service: DocumentService):
        self.document_service = document_service
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def get_relevant_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant document chunks based on query"""
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
        
        # Sort by similarity and get top_k
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        top_results = similarities[:top_k]
        
        # Format results
        results = []
        for item in top_results:
            chunk = item["chunk"]
            results.append({
                "content": chunk.get("content", ""),
                "source": chunk["source"],
                "similarity": item["similarity"],
                "chunk_id": chunk["chunk_id"]
            })
        
        return results

