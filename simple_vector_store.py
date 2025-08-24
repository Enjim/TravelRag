import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import pickle
import os

class SimpleVectorStore:
    """Simple vector store using scikit-learn for document retrieval (FAISS alternative)."""
    
    def __init__(self, model_name: str = "all-mpnet-base-v2"):
        """Initialize the vector store with a sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        self.embeddings = None
        self.documents = []
        self.dimension = self.model.get_sentence_embedding_dimension()
    
    def add_documents(self, documents: List[Dict]):
        """Add documents to the vector store."""
        if not documents:
            print("❌ No documents to add!")
            return
        
        self.documents = documents
        
        # Create embeddings for all documents
        print("🔄 Creating embeddings...")
        texts = [doc['content'] for doc in documents]
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        
        print(f"✅ Added {len(documents)} documents to vector store")
        print(f"📊 Embeddings shape: {self.embeddings.shape}")
    
    def search(self, query: str, top_k: int = 3) -> List[Tuple[Dict, float]]:
        """Search for similar documents using cosine similarity."""
        if self.embeddings is None:
            print("❌ Vector store is empty! Add documents first.")
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Calculate cosine similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Return results with documents and scores
        results = []
        for idx in top_indices:
            if idx < len(self.documents):
                results.append((self.documents[idx], float(similarities[idx])))
        
        return results
    
    def save(self, filepath: str):
        """Save the vector store to disk."""
        if self.embeddings is None:
            print("❌ Nothing to save - vector store is empty!")
            return
        
        # Save embeddings and documents
        data = {
            'embeddings': self.embeddings,
            'documents': self.documents
        }
        
        with open(f"{filepath}.pkl", 'wb') as f:
            pickle.dump(data, f)
        
        print(f"✅ Vector store saved to {filepath}.pkl")
    
    def load(self, filepath: str):
        """Load the vector store from disk."""
        try:
            with open(f"{filepath}.pkl", 'rb') as f:
                data = pickle.load(f)
            
            self.embeddings = data['embeddings']
            self.documents = data['documents']
            
            print(f"✅ Vector store loaded from {filepath}.pkl")
            print(f"📊 Loaded {len(self.documents)} documents")
            
        except Exception as e:
            print(f"❌ Error loading vector store: {str(e)}")

def create_vector_store(documents: List[Dict], model_name: str = "all-mpnet-base-v2") -> SimpleVectorStore:
    """Helper function to create and populate a vector store."""
    vector_store = SimpleVectorStore(model_name)
    vector_store.add_documents(documents)
    return vector_store

if __name__ == "__main__":
    # Test the vector store
    from text_processor import process_travel_documents
    
    print("🧪 Testing simple vector store...")
    
    # Process some sample documents
    docs = process_travel_documents()
    
    if docs:
        # Create vector store
        vs = create_vector_store(docs[:5])  # Just use first 5 docs for testing
        
        # Test search
        query = "What are the best places to visit in Paris?"
        results = vs.search(query, top_k=2)
        
        print(f"\n🔍 Search results for: '{query}'")
        for i, (doc, score) in enumerate(results):
            print(f"\n{i+1}. {doc['title']} (Score: {score:.3f})")
            print(f"   Content: {doc['content'][:150]}...")
