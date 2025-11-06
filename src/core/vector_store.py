import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import pickle
import os

class SimpleVectorStore:
    """Simple vector store using FAISS for document retrieval."""
    
    def __init__(self, model_name: str = "all-mpnet-base-v2"):
        """Initialize the vector store with a sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.dimension = self.model.get_sentence_embedding_dimension()
    
    def add_documents(self, documents: List[Dict]):
        """Add documents to the vector store."""
        if not documents:
            print("ERROR: No documents to add!")
            return
        
        self.documents = documents
        
        # Create embeddings for all documents
        print("Creating embeddings...")
        texts = [doc['content'] for doc in documents]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Initialize FAISS index
        # This is the vector store
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity  
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add to index
        self.index.add(embeddings.astype('float32'))
        
        print(f"SUCCESS: Added {len(documents)} documents to vector store")
        print(f"Index size: {self.index.ntotal} vectors")
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """Search for similar documents."""
        if self.index is None:
            print("ERROR: Vector store is empty! Add documents first.")
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        # Return results with documents and scores
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.documents):
                results.append((self.documents[idx], float(score)))
        
        return results
    
    def save(self, filepath: str):
        """Save the vector store to disk."""
        if self.index is None:
            print("ERROR: Nothing to save - vector store is empty!")
            return
        
        # Save FAISS index
        faiss.write_index(self.index, f"{filepath}.faiss")
        
        # Save documents
        with open(f"{filepath}.pkl", 'wb') as f:
            pickle.dump(self.documents, f)
        
        print(f"SUCCESS: Vector store saved to {filepath}")
    
    def load(self, filepath: str):
        """Load the vector store from disk."""
        try:
            # Load FAISS index
            self.index = faiss.read_index(f"{filepath}.faiss")
            
            # Load documents
            with open(f"{filepath}.pkl", 'rb') as f:
                self.documents = pickle.load(f)
            
            print(f"SUCCESS: Vector store loaded from {filepath}")
            print(f"Loaded {len(self.documents)} documents")
            
        except Exception as e:
            print(f"ERROR: Error loading vector store: {str(e)}")

def create_vector_store(documents: List[Dict], model_name: str = "all-mpnet-base-v2") -> SimpleVectorStore:
    """Helper function to create and populate a vector store."""
    vector_store = SimpleVectorStore(model_name)
    vector_store.add_documents(documents)
    return vector_store

# Test function
if __name__ == "__main__":
    from text_processor import process_travel_documents
    
    print("Testing vector store...")
    
    # Process some sample documents
    docs = process_travel_documents()
    if not docs:
        print("ERROR: No documents found. Run data_collector.py first!")
    else:
        # Create vector store
        vs = create_vector_store(docs[:10])  # Just use first 10 for testing
        
        # Test search
        query = "What are the best places to visit in Barcelona?"
        results = vs.search(query, top_k=2)
        
        print(f"\nSearch results for: '{query}'")
        for i, (doc, score) in enumerate(results):
            print(f"\n{i+1}. {doc['title']} (Score: {score:.3f})")
            print(f"   Content: {doc['content'][:150]}...")
