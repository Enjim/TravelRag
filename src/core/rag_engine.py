from typing import List, Dict, Tuple
from src.core.vector_store import SimpleVectorStore
from src import config

class TravelRAGEngine:
    """Main RAG engine for travel questions."""
    
    def __init__(self, vector_store: SimpleVectorStore):
        """Initialize the RAG engine with a vector store."""
        self.vector_store = vector_store
        
        # Check if API key is set
        if config.OPENAI_API_KEY == "your-api-key-here":
            print("⚠️  Warning: Please set your OpenAI API key in config.py")
    
    def retrieve_relevant_chunks(self, query: str, top_k: int = None) -> List[Tuple[Dict, float]]:
        """Retrieve relevant document chunks for a query."""
        if top_k is None:
            top_k = config.TOP_K_CHUNKS
        
        return self.vector_store.search(query, top_k)
    
    def generate_answer(self, query: str, relevant_chunks: List[Tuple[Dict, float]]) -> str:
        """Generate an answer using OpenAI's GPT API."""
        
        if not relevant_chunks:
            return "I couldn't find any relevant information to answer your question."
        
        # Prepare context from retrieved chunks
        context_parts = []
        for doc, score in relevant_chunks:
            context_parts.append(f"Source: {doc['title']}\nContent: {doc['content']}\n")
        
        context = "\n".join(context_parts)
        
        # Create the prompt
        prompt = f"""You are a helpful travel assistant. Answer the user's question based on the provided context. 
        If the context doesn't contain enough information to fully answer the question, say so.
        
        Context:
        {context}
        
        User Question: {query}
        
        Answer:"""
        
        try:
            # Call OpenAI API (new v1.0+ format)
            from openai import OpenAI
            client = OpenAI(api_key=config.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can change this to gpt-4 if you prefer
                messages=[
                    {"role": "system", "content": "You are a helpful travel assistant. Answer questions based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def answer_question(self, query: str) -> Dict:
        """Main method to answer a travel question using RAG."""
        
        print(f"Searching for relevant information...")
        
        # Retrieve relevant chunks
        relevant_chunks = self.retrieve_relevant_chunks(query)
        
        if not relevant_chunks:
            return {
                "answer": "I couldn't find any relevant information to answer your question.",
                "sources": [],
                "query": query
            }
        
        print(f"Found {len(relevant_chunks)} relevant sources")
        
        # Generate answer
        print("Generating answer...")
        answer = self.generate_answer(query, relevant_chunks)
        
        # Prepare sources for display
        sources = []
        for doc, score in relevant_chunks:
            sources.append({
                "title": doc['title'],
                "content": doc['content'],  # Show full content without truncation
                "score": f"{score:.3f}",
                "source_file": doc['source_file']
            })
        
        return {
            "answer": answer,
            "sources": sources,
            "query": query
        }

def create_rag_engine(vector_store: SimpleVectorStore) -> TravelRAGEngine:
    """Helper function to create a RAG engine."""
    return TravelRAGEngine(vector_store)

if __name__ == "__main__":
    # Test the RAG engine
    from text_processor import process_travel_documents
    from vector_store import create_vector_store
    
    print("Testing RAG engine...")
    
    # Check if we have data
    docs = process_travel_documents()
    
    if docs:
        # Create vector store
        vs = create_vector_store(docs[:5])  # Just use first 5 docs for testing
        
        # Create RAG engine
        rag = create_rag_engine(vs)
        
        # Test a question
        test_question = "What are some travel tips for beginners?"
        result = rag.answer_question(test_question)
        
        print(f"\nQuestion: {result['query']}")
        print(f"Answer: {result['answer']}")
        print(f"\nSources:")
        for i, source in enumerate(result['sources']):
            print(f"   {i+1}. {source['title']} (Score: {source['score']})")
            print(f"      {source['content']}")
    else:
        print("ERROR: No documents found. Run data_collector.py first!")
