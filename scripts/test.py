#!/usr/bin/env python3
"""
Super Simple TravelRag Test - Shows exactly what happens step by step
"""

import os
from text_processor import process_travel_documents
from vector_store import create_vector_store
from rag_engine import create_rag_engine

def simple_test():
    """Test the entire RAG system step by step."""
    
    print("SIMPLE TRAVELRAG TEST")
    print("=" * 40)
    
    # Step 1: Check if we have data
    print("\n1. CHECKING DATA...")
    if not os.path.exists("travel_data"):
        print("ERROR: No travel_data folder found!")
        return
    
    files = [f for f in os.listdir("travel_data") if f.endswith('.txt')]
    print(f"SUCCESS: Found {len(files)} text files")
    
    # Step 2: Process documents
    print("\n2. PROCESSING DOCUMENTS...")
    docs = process_travel_documents() # Here the txt files become chunks of text
    if not docs:
        print("ERROR: No documents processed!")
        return
    
    print(f"SUCCESS: Created {len(docs)} chunks")
    
    # Step 3: Create vector store (use fewer docs for faster testing)
    print("\n3. CREATING VECTOR STORE...")
    # Just use the first 100 docs for faster testing
    vs = create_vector_store(docs[:400]) # here the chunks become vectors
    print(f"SUCCESS: Vector store ready with {len(vs.documents)} documents")
    
    # Step 4: Test search
    print("\n4. TESTING SEARCH...")
    test_query = "What food should I try in Brazil?"
    results = vs.search(test_query, top_k=3)
    print(f"SUCCESS: Found {len(results)} results for '{test_query}'")
    
    # Show what we found
    for i, (doc, score) in enumerate(results):
        print(f"   Source {i+1}: {doc['title']} (Score: {score:.3f})")
        print(f"   Content: {doc['content'][:100]}...")
    
    # Step 5: Test RAG (with error handling)
    print("\n5. TESTING RAG...")
    try:
        rag = create_rag_engine(vs)
        result = rag.answer_question(test_query)
        
        print(f"\nQUESTION: {result['query']}")
        print(f"ANSWER: {result['answer']}")
        print(f"SOURCES: {len(result['sources'])} found")
        
    except Exception as e:
        print(f"ERROR: RAG Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
    
    print("\nTEST COMPLETE!")

if __name__ == "__main__":
    simple_test()